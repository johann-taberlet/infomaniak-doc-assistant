"""
Answer generation for RAG using configurable LLM.

Generates answers from retrieved context with token usage tracking
for cost analysis across different models.
"""

import time
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langfuse import observe

from backend.app.core.config import settings


@dataclass
class GenerationUsage:
    """Token usage from a generation call."""

    input_tokens: int
    output_tokens: int
    latency_ms: float

    def calculate_cost(self, model: str) -> float:
        """Calculate cost in USD based on model pricing."""
        from backend.app.core.config import MODEL_PRICING

        pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
        input_cost = (self.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (self.output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost


class AnswerGenerator:
    """
    Generate answers from retrieved context using configurable LLM.

    Supports multiple models via OpenRouter with token tracking
    for cost analysis during evaluation.
    """

    def __init__(self, model: str | None = None, temperature: float = 0.7):
        """
        Initialize the answer generator.

        Args:
            model: OpenRouter model ID (defaults to settings.generation_model)
            temperature: Generation temperature (0-1)
        """
        self.model = model or settings.generation_model
        self.temperature = temperature
        self.last_usage: GenerationUsage | None = None

        self._llm = ChatOpenAI(
            api_key=settings.openrouter_api_key,
            model=self.model,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=500,
        )

    @observe(name="generate_answer")
    def generate(self, question: str, context: str) -> str:
        """
        Generate answer from question and context.

        Args:
            question: The user's question
            context: Retrieved documentation context

        Returns:
            Generated answer string
        """
        prompt = self._build_prompt(question, context)

        start_time = time.perf_counter()
        response = self._llm.invoke(prompt)
        latency_ms = (time.perf_counter() - start_time) * 1000

        # Extract token usage from response metadata
        input_tokens = 0
        output_tokens = 0
        if hasattr(response, "response_metadata"):
            usage = response.response_metadata.get("token_usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)

        self.last_usage = GenerationUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
        )

        # Handle different response content types
        content = response.content
        if isinstance(content, list):
            # Some models return content blocks
            content = "".join(str(block) for block in content)

        return str(content)

    def _build_prompt(self, question: str, context: str) -> str:
        """Build the generation prompt."""
        return f"""You are an assistant for Infomaniak kSuite documentation (kDrive, kMeet, kChat).

Important instructions:
- The documentation is in English
- Answer ONLY based on the provided documentation
- If the documentation doesn't contain the answer, say "I don't have information about that in the documentation."
- Be concise and accurate
- Answer in the same language as the user's question

Documentation:
{context}

Question: {question}

Answer:"""

    def get_model_short_name(self) -> str:
        """Get a short display name for the model."""
        # "mistralai/mistral-nemo" -> "mistral-nemo"
        # "qwen/qwen3-8b" -> "qwen3-8b"
        return self.model.split("/")[-1] if "/" in self.model else self.model
