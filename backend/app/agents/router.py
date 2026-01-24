"""
Intent Router for classifying user queries.

Classifies queries as:
- RAG: Documentation questions → use retrieval pipeline
- Action: Requests to execute something → route to agent executor
"""

import json
import time
from dataclasses import dataclass, field
from enum import Enum

from langchain_openai import ChatOpenAI
from langfuse import observe

from backend.app.core.config import settings

# Retry configuration for transient API errors
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


class IntentType(str, Enum):
    """Types of user intents."""

    RAG = "rag"
    ACTION = "action"


@dataclass
class SkillInfo:
    """Metadata about an available skill."""

    name: str
    description: str
    trigger_phrases: list[str] = field(default_factory=list)


@dataclass
class Intent:
    """Classification result for a user query."""

    type: IntentType
    confidence: float  # 0.0-1.0
    skill: str | None = None  # For actions: "start-meeting", etc.
    reasoning: str = ""

    def is_action(self) -> bool:
        """Check if this is a high-confidence action intent."""
        return (
            self.type == IntentType.ACTION
            and self.confidence >= settings.router_confidence_threshold
        )


# Default skills for kSuite
DEFAULT_SKILLS: list[SkillInfo] = [
    SkillInfo(
        name="start-meeting",
        description="Start a video meeting with participants",
        trigger_phrases=["start a meeting", "create a call", "video call"],
    ),
    SkillInfo(
        name="share-file",
        description="Share a file or folder with others",
        trigger_phrases=["share file", "give access", "share folder"],
    ),
    SkillInfo(
        name="send-message",
        description="Send a message to a contact or channel",
        trigger_phrases=["send message", "message someone", "notify"],
    ),
]


def get_available_skills() -> list[SkillInfo]:
    """Get list of available skills (hardcoded for Phase A1)."""
    return DEFAULT_SKILLS


class IntentRouter:
    """
    LLM-based intent classifier.

    Uses a fast model to classify user queries as RAG (documentation lookup)
    or Action (execute a skill).
    """

    def __init__(self, model: str | None = None, temperature: float = 0.0):
        """
        Initialize the intent router.

        Args:
            model: Model to use for classification (defaults to settings.router_model)
            temperature: Temperature for generation (0 for deterministic)
        """
        self.model = model or settings.router_model

        # Use OpenRouter with OpenAI-compatible API
        self._llm = ChatOpenAI(
            api_key=settings.openrouter_api_key,
            model=self.model,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=200,
        )

    def _build_prompt(
        self,
        query: str,
        available_skills: list[SkillInfo],
        history: list[dict] | None = None,
    ) -> str:
        """Build the classification prompt."""
        # Format skills section
        skills_section = "\n".join(
            f"- {skill.name}: {skill.description}" for skill in available_skills
        )

        # Format history if provided
        history_section = ""
        if history:
            history_lines = []
            for msg in history[-3:]:  # Last 3 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")[:200]  # Truncate long messages
                history_lines.append(f"{role}: {content}")
            if history_lines:
                history_section = f"\n## Recent Conversation\n" + "\n".join(history_lines)

        return f"""You are an intent classifier for a kSuite documentation assistant.

Classify the user's query into one of two categories:
1. **rag**: Questions about how things work, documentation lookups, explanations
2. **action**: Requests to DO something, execute an action, perform a task

## Available Skills
{skills_section}

## Examples

Query: "How do I share a file?"
{{"type": "rag", "confidence": 0.95, "skill": null, "reasoning": "Asking for instructions on how to do something"}}

Query: "What is kMeet?"
{{"type": "rag", "confidence": 0.98, "skill": null, "reasoning": "Asking for information about a product"}}

Query: "Start a meeting with John"
{{"type": "action", "confidence": 0.92, "skill": "start-meeting", "reasoning": "Imperative command to start a meeting"}}

Query: "Share budget.xlsx with Sarah"
{{"type": "action", "confidence": 0.90, "skill": "share-file", "reasoning": "Request to share a specific file"}}

Query: "Send a message to the team"
{{"type": "action", "confidence": 0.88, "skill": "send-message", "reasoning": "Request to send a message"}}

Query: "Can I use kDrive offline?"
{{"type": "rag", "confidence": 0.95, "skill": null, "reasoning": "Question about feature availability"}}
{history_section}
## Query to Classify
Query: "{query}"

Respond with ONLY a JSON object (no markdown, no explanation):
{{"type": "<rag|action>", "confidence": <0.0-1.0>, "skill": "<skill-name|null>", "reasoning": "<brief explanation>"}}"""

    def _invoke_with_retry(self, prompt: str) -> str:
        """Invoke LLM with retry logic for transient errors."""
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                response = self._llm.invoke(prompt)
                return response.content
            except Exception as e:
                last_error = e
                if attempt < MAX_RETRIES - 1:
                    print(f"  [Retry {attempt + 1}/{MAX_RETRIES}] API error: {e}")
                    time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
        # If all retries failed, return a fallback response
        print(f"  [Warning] All retries failed: {last_error}")
        return '{"type": "rag", "confidence": 0.5, "skill": null, "reasoning": "API error, defaulting to RAG"}'

    def _parse_response(self, content: str | list) -> Intent:
        """Parse the LLM response to extract intent."""
        try:
            # Handle different response formats
            if isinstance(content, list):
                text = str(content[0]) if content else ""
            else:
                text = str(content)

            # Handle markdown code blocks
            if "```json" in text:
                json_start = text.find("```json") + 7
                json_end = text.find("```", json_start)
                text = text[json_start:json_end].strip()
            elif "```" in text:
                json_start = text.find("```") + 3
                json_end = text.find("```", json_start)
                text = text[json_start:json_end].strip()

            # Parse JSON
            data = json.loads(text)

            # Extract and validate fields
            intent_type_str = data.get("type", "rag").lower()
            intent_type = IntentType.ACTION if intent_type_str == "action" else IntentType.RAG

            confidence = float(data.get("confidence", 0.5))
            confidence = max(0.0, min(1.0, confidence))  # Clamp to valid range

            skill = data.get("skill")
            if skill == "null" or skill == "":
                skill = None

            reasoning = str(data.get("reasoning", ""))

            return Intent(
                type=intent_type,
                confidence=confidence,
                skill=skill,
                reasoning=reasoning,
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # If parsing fails, default to RAG
            return Intent(
                type=IntentType.RAG,
                confidence=0.5,
                skill=None,
                reasoning=f"Parse error, defaulting to RAG: {e}",
            )

    @observe(name="classify_intent")
    def classify(
        self,
        query: str,
        available_skills: list[SkillInfo] | None = None,
        history: list[dict] | None = None,
    ) -> Intent:
        """
        Classify a user query as RAG or Action.

        Args:
            query: The user's query to classify
            available_skills: List of available skills (defaults to DEFAULT_SKILLS)
            history: Recent conversation history for context

        Returns:
            Intent with type, confidence, optional skill, and reasoning
        """
        # Handle empty query
        if not query or not query.strip():
            return Intent(
                type=IntentType.RAG,
                confidence=1.0,
                skill=None,
                reasoning="Empty query, defaulting to RAG",
            )

        skills = available_skills or DEFAULT_SKILLS
        prompt = self._build_prompt(query, skills, history)
        content = self._invoke_with_retry(prompt)
        return self._parse_response(content)
