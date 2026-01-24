"""
Evaluation runner for RAG experiments.

Orchestrates:
- Loading evaluation datasets
- Running retrieval and generation
- Scoring with LLM-as-judge
- Logging to Langfuse
"""

import time
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from langfuse import Langfuse

from backend.app.core.config import settings
from backend.app.evaluation.judge import EvaluationScores, LLMJudge
from backend.app.rag.retriever import QdrantRetriever, RetrievalResult

# Type alias for retrievers (QdrantRetriever or HybridRetriever)
# Both have compatible search() methods returning list[RetrievalResult]
from typing import Protocol


class RetrieverProtocol(Protocol):
    """Protocol for retrievers compatible with evaluation."""

    def search(
        self,
        query: str,
        top_k: int | None = None,
        score_threshold: float | None = None,
        filter_product: str | None = None,
    ) -> list[RetrievalResult]: ...


@dataclass
class EvaluationQuestion:
    """A question from the evaluation dataset."""

    id: str
    question: str
    expected_answer: str
    category: str = "general"
    product: str = ""


@dataclass
class EvaluationResult:
    """Result of evaluating a single question."""

    question_id: str
    question: str
    expected_answer: str
    generated_answer: str
    retrieved_context: str
    scores: EvaluationScores
    retrieval_latency_ms: float
    generation_latency_ms: float
    total_latency_ms: float
    num_chunks_retrieved: int
    metadata: dict = field(default_factory=dict)

    # Token usage and cost tracking (populated when using AnswerGenerator)
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "question_id": self.question_id,
            "question": self.question,
            "expected_answer": self.expected_answer,
            "generated_answer": self.generated_answer,
            "retrieved_context": self.retrieved_context[:500] + "..."
            if len(self.retrieved_context) > 500
            else self.retrieved_context,
            "scores": self.scores.to_dict(),
            "retrieval_latency_ms": self.retrieval_latency_ms,
            "generation_latency_ms": self.generation_latency_ms,
            "total_latency_ms": self.total_latency_ms,
            "num_chunks_retrieved": self.num_chunks_retrieved,
            "metadata": self.metadata,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cost_usd": self.cost_usd,
        }


class EvaluationRunner:
    """
    Orchestrates RAG evaluation experiments.

    Loads questions, runs retrieval, generates answers, and scores them.
    All traces are logged to Langfuse for A/B comparison.
    """

    def __init__(
        self,
        collection_name: str,
        experiment_tags: dict[str, str] | None = None,
        retriever: RetrieverProtocol | None = None,
    ):
        """
        Initialize evaluation runner.

        Args:
            collection_name: Qdrant collection to evaluate
            experiment_tags: Tags for Langfuse experiment tracking
            retriever: Custom retriever (QdrantRetriever or HybridRetriever).
                      If None, creates a QdrantRetriever for the collection.
        """
        self.collection_name = collection_name
        self.experiment_tags = experiment_tags or {}

        # Initialize components - use provided retriever or create default
        self.retriever: RetrieverProtocol = retriever or QdrantRetriever(collection_name=collection_name)
        self.judge = LLMJudge()

        # Initialize Langfuse if enabled
        self.langfuse: Langfuse | None = None
        if settings.langfuse_enabled:
            self.langfuse = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host,
            )

    def load_dataset(self, dataset_path: str | Path) -> list[EvaluationQuestion]:
        """
        Load evaluation questions from YAML file.

        Args:
            dataset_path: Path to YAML file with questions

        Returns:
            List of evaluation questions
        """
        path = Path(dataset_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        with open(path) as f:
            data = yaml.safe_load(f)

        questions = []
        for q in data.get("questions", []):
            questions.append(
                EvaluationQuestion(
                    id=q["id"],
                    question=q["question"],
                    expected_answer=q["expected_answer"],
                    category=q.get("category", "general"),
                    product=q.get("product", ""),
                )
            )

        return questions

    def evaluate_question(
        self,
        question: EvaluationQuestion,
        generate_answer_fn: Any | None = None,
    ) -> EvaluationResult:
        """
        Evaluate a single question.

        Args:
            question: The evaluation question
            generate_answer_fn: Optional function to generate answers.
                               If None, uses context concatenation as "answer".

        Returns:
            Evaluation result with scores
        """
        total_start = time.perf_counter()

        # 1. Retrieve relevant chunks
        retrieval_start = time.perf_counter()
        results = self.retriever.search(
            query=question.question,
            filter_product=question.product if question.product else None,
        )
        retrieval_latency = (time.perf_counter() - retrieval_start) * 1000

        # Build context from retrieved chunks
        context = self._build_context(results)

        # 2. Generate answer
        generation_start = time.perf_counter()
        if generate_answer_fn:
            generated_answer = generate_answer_fn(question.question, context)
        else:
            # Default: use context as answer (for retrieval-only evaluation)
            generated_answer = self._extract_answer_from_context(
                question.question, context
            )
        generation_latency = (time.perf_counter() - generation_start) * 1000

        total_latency = (time.perf_counter() - total_start) * 1000

        # 3. Score with LLM judge
        scores = self.judge.evaluate(
            question=question.question,
            answer=generated_answer,
            context=context,
            expected_answer=question.expected_answer,
        )

        return EvaluationResult(
            question_id=question.id,
            question=question.question,
            expected_answer=question.expected_answer,
            generated_answer=generated_answer,
            retrieved_context=context,
            scores=scores,
            retrieval_latency_ms=retrieval_latency,
            generation_latency_ms=generation_latency,
            total_latency_ms=total_latency,
            num_chunks_retrieved=len(results),
            metadata={
                "category": question.category,
                "product": question.product,
                "collection": self.collection_name,
                **self.experiment_tags,
            },
        )

    def run_evaluation(
        self,
        dataset_path: str | Path,
        generate_answer_fn: Any | None = None,
        max_questions: int | None = None,
    ) -> list[EvaluationResult]:
        """
        Run evaluation on all questions in the dataset.

        Args:
            dataset_path: Path to evaluation dataset YAML
            generate_answer_fn: Optional function to generate answers
            max_questions: Maximum number of questions to evaluate (for testing)

        Returns:
            List of evaluation results
        """
        questions = self.load_dataset(dataset_path)

        if max_questions:
            questions = questions[:max_questions]

        results = []
        for i, question in enumerate(questions):
            print(f"Evaluating question {i + 1}/{len(questions)}: {question.id}")

            # Run evaluation with Langfuse tracing if enabled
            if self.langfuse:
                result = self._evaluate_with_langfuse(question, generate_answer_fn)
            else:
                result = self.evaluate_question(question, generate_answer_fn)

            results.append(result)

            # Print progress
            print(
                f"  Correctness: {result.scores.correctness:.2f}, "
                f"Faithfulness: {result.scores.faithfulness:.2f}, "
                f"Relevance: {result.scores.relevance:.2f}"
            )

        # Flush Langfuse
        if self.langfuse:
            self.langfuse.flush()

        return results

    def _evaluate_with_langfuse(
        self,
        question: EvaluationQuestion,
        generate_answer_fn: Any | None = None,
        generator: Any | None = None,
    ) -> EvaluationResult:
        """
        Run evaluation with Langfuse tracing using context manager.

        Uses the recommended start_as_current_span API for proper tracing.

        Args:
            question: The evaluation question
            generate_answer_fn: Optional function to generate answers
            generator: Optional AnswerGenerator instance for token tracking
        """
        assert self.langfuse is not None

        # Build tags for filtering in Langfuse
        tags = [
            f"collection:{self.collection_name}",
            f"category:{question.category}",
            *[f"{k}:{v}" for k, v in self.experiment_tags.items()],
        ]
        if question.product:
            tags.append(f"product:{question.product}")

        # Use context manager for automatic span management
        with self.langfuse.start_as_current_span(
            name=f"eval_{question.id}",
            input={"question": question.question, "expected_answer": question.expected_answer},
            metadata={
                "experiment": "rag_evaluation",
                "question_id": question.id,
                "category": question.category,
                "product": question.product,
                "collection": self.collection_name,
                **self.experiment_tags,
            },
        ) as span:
            # Update trace with tags
            span.update_trace(
                name=f"RAG Eval: {question.id}",
                tags=tags,
            )

            # Run the actual evaluation
            result = self.evaluate_question(question, generate_answer_fn)

            # Capture token usage from generator if provided
            if generator and hasattr(generator, "last_usage") and generator.last_usage:
                result.input_tokens = generator.last_usage.input_tokens
                result.output_tokens = generator.last_usage.output_tokens
                if hasattr(generator, "model"):
                    result.cost_usd = generator.last_usage.calculate_cost(generator.model)

            # Update span with output including token usage
            output_data = {
                "generated_answer": result.generated_answer[:500],
                "num_chunks": result.num_chunks_retrieved,
            }
            if result.input_tokens > 0:
                output_data["input_tokens"] = result.input_tokens
                output_data["output_tokens"] = result.output_tokens
                output_data["cost_usd"] = result.cost_usd

            span.update(output=output_data)

            # Log usage to Langfuse if available
            if result.input_tokens > 0:
                span.update(
                    usage={
                        "input": result.input_tokens,
                        "output": result.output_tokens,
                    }
                )

            # Add scores to trace using score_trace (numeric scores 0-1)
            span.score_trace(
                name="correctness",
                value=result.scores.correctness,
                data_type="NUMERIC",
                comment=result.scores.correctness_reasoning[:200] if result.scores.correctness_reasoning else None,
            )
            span.score_trace(
                name="faithfulness",
                value=result.scores.faithfulness,
                data_type="NUMERIC",
                comment=result.scores.faithfulness_reasoning[:200] if result.scores.faithfulness_reasoning else None,
            )
            span.score_trace(
                name="relevance",
                value=result.scores.relevance,
                data_type="NUMERIC",
                comment=result.scores.relevance_reasoning[:200] if result.scores.relevance_reasoning else None,
            )

            # Add cost as a score for easy filtering/comparison
            if result.cost_usd > 0:
                span.score_trace(
                    name="cost_usd",
                    value=result.cost_usd,
                    data_type="NUMERIC",
                    comment=f"{result.input_tokens} in / {result.output_tokens} out",
                )

            # Log retrieval as a nested span
            with span.start_as_current_span(
                name="retrieval",
                metadata={"latency_ms": result.retrieval_latency_ms},
            ) as retrieval_span:
                retrieval_span.update(
                    input={"query": question.question},
                    output={"num_chunks": result.num_chunks_retrieved},
                )

            # Log generation as a nested span (if generator was used)
            if generator and result.input_tokens > 0:
                with span.start_as_current_span(
                    name="generation",
                    metadata={
                        "model": getattr(generator, "model", "unknown"),
                        "latency_ms": result.generation_latency_ms,
                    },
                ) as gen_span:
                    gen_span.update(
                        input={"context_length": len(result.retrieved_context)},
                        output={"answer_length": len(result.generated_answer)},
                        usage={
                            "input": result.input_tokens,
                            "output": result.output_tokens,
                        },
                    )

            # Log judge evaluation as a nested span
            with span.start_as_current_span(
                name="judge_evaluation",
                metadata={"latency_ms": result.generation_latency_ms if not generator else 0},
            ) as judge_span:
                judge_span.update(
                    input={"context_length": len(result.retrieved_context)},
                    output=result.scores.to_dict(),
                )

        return result

    def compute_aggregate_scores(
        self, results: list[EvaluationResult]
    ) -> dict[str, float]:
        """
        Compute aggregate scores across all results.

        Returns:
            Dictionary with average scores
        """
        if not results:
            return {}

        n = len(results)

        # Group by category for breakdown
        by_category: dict[str, list[EvaluationResult]] = {}
        for r in results:
            cat = r.metadata.get("category", "unknown")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(r)

        aggregate = {
            "avg_correctness": sum(r.scores.correctness for r in results) / n,
            "avg_faithfulness": sum(r.scores.faithfulness for r in results) / n,
            "avg_relevance": sum(r.scores.relevance for r in results) / n,
            "avg_retrieval_latency_ms": sum(r.retrieval_latency_ms for r in results) / n,
            "avg_generation_latency_ms": sum(r.generation_latency_ms for r in results) / n,
            "avg_total_latency_ms": sum(r.total_latency_ms for r in results) / n,
            "avg_chunks_retrieved": sum(r.num_chunks_retrieved for r in results) / n,
            "num_questions": n,
            # Token usage and cost
            "total_input_tokens": sum(r.input_tokens for r in results),
            "total_output_tokens": sum(r.output_tokens for r in results),
            "total_cost_usd": sum(r.cost_usd for r in results),
            "avg_input_tokens": sum(r.input_tokens for r in results) / n,
            "avg_output_tokens": sum(r.output_tokens for r in results) / n,
            "avg_cost_usd": sum(r.cost_usd for r in results) / n,
        }

        # Add per-category breakdown
        for cat, cat_results in by_category.items():
            cat_n = len(cat_results)
            aggregate[f"avg_correctness_{cat}"] = sum(r.scores.correctness for r in cat_results) / cat_n
            aggregate[f"avg_relevance_{cat}"] = sum(r.scores.relevance for r in cat_results) / cat_n
            aggregate[f"num_{cat}"] = cat_n

        return aggregate

    def _build_context(self, results: list[RetrievalResult]) -> str:
        """Build context string from retrieval results."""
        if not results:
            return ""

        context_parts = []
        for i, result in enumerate(results):
            # Use context window if available, otherwise use content
            content = result.context_window or result.content
            source = result.metadata.get("source_url", result.metadata.get("source", ""))
            title = result.metadata.get("title", "")

            context_parts.append(
                f"[Document {i + 1}] {title}\n"
                f"Source: {source}\n"
                f"Content: {content}\n"
            )

        return "\n---\n".join(context_parts)

    def _extract_answer_from_context(self, question: str, context: str) -> str:
        """
        Simple answer extraction from context.

        For retrieval-only evaluation, we use the first relevant chunk
        as the "answer" to evaluate retrieval quality.
        """
        # Unused parameter is intentional - could be used for smarter extraction
        _ = question
        # Just return the context as-is for retrieval evaluation
        # In a full RAG system, this would call an LLM
        return context[:2000] if context else "No relevant information found."
