"""
LLM-as-judge evaluation for RAG quality assessment.

Evaluates:
- Correctness: Is the answer accurate given the expected answer?
- Faithfulness: Is the answer grounded in the retrieved context?
- Relevance: Are the retrieved documents relevant to the question?
"""

import json
import time
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langfuse import observe

from backend.app.core.config import settings

# Retry configuration for transient API errors
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


@dataclass
class EvaluationScores:
    """Scores from LLM-as-judge evaluation."""

    correctness: float  # 0-1: Is the answer correct?
    faithfulness: float  # 0-1: Is the answer grounded in context?
    relevance: float  # 0-1: Is the context relevant to the question?

    correctness_reasoning: str = ""
    faithfulness_reasoning: str = ""
    relevance_reasoning: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "correctness": self.correctness,
            "faithfulness": self.faithfulness,
            "relevance": self.relevance,
            "correctness_reasoning": self.correctness_reasoning,
            "faithfulness_reasoning": self.faithfulness_reasoning,
            "relevance_reasoning": self.relevance_reasoning,
        }


class LLMJudge:
    """
    LLM-based evaluation judge.

    Uses a fast, capable model (Gemini Flash via OpenRouter) to score
    RAG responses on multiple dimensions.
    """

    def __init__(self, model: str | None = None, temperature: float = 0.0):
        """
        Initialize the LLM judge.

        Args:
            model: Model to use for judging (defaults to settings.judge_model)
            temperature: Temperature for generation (0 for deterministic)
        """
        self.model = model or settings.judge_model

        # Use OpenRouter with OpenAI-compatible API
        self._llm = ChatOpenAI(
            api_key=settings.openrouter_api_key,
            model=self.model,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=1000,
        )

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
        # If all retries failed, return a neutral response
        print(f"  [Warning] All retries failed: {last_error}")
        return '{"score": 0.5, "reasoning": "API error during evaluation"}'

    @observe(name="judge_correctness")
    def judge_correctness(
        self,
        question: str,
        answer: str,
        expected_answer: str,
    ) -> tuple[float, str]:
        """
        Judge if the answer is correct given the expected answer.

        Returns:
            Tuple of (score 0-1, reasoning)
        """
        prompt = f"""You are evaluating the correctness of an answer to a question.

Question: {question}

Expected Answer: {expected_answer}

Generated Answer: {answer}

Evaluate if the generated answer is correct compared to the expected answer.
Consider:
- Does it contain the same key information?
- Are there any factual errors or contradictions?
- Is the core meaning preserved even if wording differs?

Respond with a JSON object:
{{
    "score": <float between 0 and 1>,
    "reasoning": "<brief explanation>"
}}

Score guide:
- 1.0: Perfect or near-perfect match
- 0.7-0.9: Mostly correct with minor differences
- 0.4-0.6: Partially correct
- 0.1-0.3: Mostly incorrect
- 0.0: Completely wrong or contradictory"""

        content = self._invoke_with_retry(prompt)
        return self._parse_score_response(content)

    @observe(name="judge_faithfulness")
    def judge_faithfulness(
        self,
        question: str,
        answer: str,
        context: str,
    ) -> tuple[float, str]:
        """
        Judge if the answer is faithful to (grounded in) the context.

        Returns:
            Tuple of (score 0-1, reasoning)
        """
        prompt = f"""You are evaluating if an answer is faithful to the provided context.

Question: {question}

Context (retrieved documents):
{context}

Generated Answer: {answer}

Evaluate if the answer is grounded in the context:
- Is every claim in the answer supported by the context?
- Does the answer avoid adding information not in the context?
- Does it correctly use the information from the context?

Respond with a JSON object:
{{
    "score": <float between 0 and 1>,
    "reasoning": "<brief explanation>"
}}

Score guide:
- 1.0: Fully grounded in context
- 0.7-0.9: Mostly grounded with minor extrapolations
- 0.4-0.6: Partially grounded, some unsupported claims
- 0.1-0.3: Mostly not grounded
- 0.0: Completely hallucinated"""

        content = self._invoke_with_retry(prompt)
        return self._parse_score_response(content)

    @observe(name="judge_relevance")
    def judge_relevance(
        self,
        question: str,
        context: str,
    ) -> tuple[float, str]:
        """
        Judge if the retrieved context is relevant to the question.

        Returns:
            Tuple of (score 0-1, reasoning)
        """
        prompt = f"""You are evaluating if retrieved documents are relevant to a question.

Question: {question}

Retrieved Context:
{context}

Evaluate the relevance of the context:
- Does the context contain information needed to answer the question?
- Is the context focused or does it contain mostly irrelevant information?
- Would this context help someone answer the question?

Respond with a JSON object:
{{
    "score": <float between 0 and 1>,
    "reasoning": "<brief explanation>"
}}

Score guide:
- 1.0: Highly relevant, contains all needed information
- 0.7-0.9: Mostly relevant, contains key information
- 0.4-0.6: Partially relevant, some useful information
- 0.1-0.3: Mostly irrelevant
- 0.0: Completely irrelevant"""

        content = self._invoke_with_retry(prompt)
        return self._parse_score_response(content)

    @observe(name="evaluate_all")
    def evaluate(
        self,
        question: str,
        answer: str,
        context: str,
        expected_answer: str,
    ) -> EvaluationScores:
        """
        Run all evaluations and return combined scores.

        Args:
            question: The question asked
            answer: The generated answer
            context: The retrieved context
            expected_answer: The expected/ground truth answer

        Returns:
            EvaluationScores with all metrics
        """
        correctness_score, correctness_reason = self.judge_correctness(
            question, answer, expected_answer
        )
        faithfulness_score, faithfulness_reason = self.judge_faithfulness(
            question, answer, context
        )
        relevance_score, relevance_reason = self.judge_relevance(question, context)

        return EvaluationScores(
            correctness=correctness_score,
            faithfulness=faithfulness_score,
            relevance=relevance_score,
            correctness_reasoning=correctness_reason,
            faithfulness_reasoning=faithfulness_reason,
            relevance_reasoning=relevance_reason,
        )

    def _parse_score_response(self, content: str | list) -> tuple[float, str]:
        """Parse the LLM response to extract score and reasoning."""
        try:
            # Handle different response formats
            if isinstance(content, list):
                # Some models return a list of content blocks
                text = str(content[0]) if content else ""
            else:
                text = str(content)

            # Try to find JSON in the response
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
            score = float(data.get("score", 0.5))
            reasoning = str(data.get("reasoning", ""))

            # Clamp score to valid range
            score = max(0.0, min(1.0, score))

            return score, reasoning

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # If parsing fails, return a neutral score
            return 0.5, f"Failed to parse response: {e}"
