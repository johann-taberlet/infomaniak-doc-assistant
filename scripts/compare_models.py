#!/usr/bin/env python3
"""
Compare LLM models for RAG answer generation.

Orchestrates a two-phase evaluation:
1. Mini-eval (10 questions) on all candidate models
2. Full eval (all questions) on top 1-2 models based on mini-eval results

Usage:
    uv run python scripts/compare_models.py \\
        --collection infomaniak_full_doc_no_images \\
        --mini-eval-size 10

    uv run python scripts/compare_models.py \\
        --collection infomaniak_full_doc_no_images \\
        --models mistralai/mistral-nemo qwen/qwen3-8b \\
        --mini-eval-size 10 \\
        --skip-full-eval
"""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.core.config import MODEL_PRICING, settings
from backend.app.evaluation.runner import EvaluationRunner
from backend.app.rag.generator import AnswerGenerator


# Default models to compare
DEFAULT_MODELS = [
    "mistralai/mistral-nemo",
    "qwen/qwen3-8b",
    "z-ai/glm-4.7-flash",
]


@dataclass
class ModelResult:
    """Aggregated results for a single model."""

    model: str
    avg_correctness: float
    avg_faithfulness: float
    avg_relevance: float
    avg_latency_ms: float
    total_cost_usd: float
    num_questions: int

    @property
    def quality_score(self) -> float:
        """Combined quality score (weighted average)."""
        return 0.5 * self.avg_correctness + 0.3 * self.avg_faithfulness + 0.2 * self.avg_relevance

    def short_name(self) -> str:
        """Get short model name for display."""
        return self.model.split("/")[-1] if "/" in self.model else self.model


def run_evaluation_for_model(
    model: str,
    collection: str,
    dataset_path: str,
    max_questions: int | None,
    experiment_tag: str,
) -> ModelResult:
    """
    Run evaluation for a single model.

    Args:
        model: OpenRouter model ID
        collection: Qdrant collection name
        dataset_path: Path to evaluation dataset YAML
        max_questions: Maximum questions to evaluate (None for all)
        experiment_tag: Tag for Langfuse experiment tracking

    Returns:
        ModelResult with aggregated scores
    """
    print(f"\n{'=' * 60}")
    print(f"Evaluating: {model}")
    print(f"{'=' * 60}")

    # Initialize components
    generator = AnswerGenerator(model=model)
    experiment_tags = {
        "experiment": experiment_tag,
        "model": model,
        "collection": collection,
        "timestamp": datetime.now().isoformat(),
    }

    runner = EvaluationRunner(
        collection_name=collection,
        experiment_tags=experiment_tags,
    )

    # Load questions
    questions = runner.load_dataset(dataset_path)
    if max_questions:
        # Strategic selection: mix of categories
        direct = [q for q in questions if q.category == "direct"][:5]
        multi_doc = [q for q in questions if q.category == "multi_doc"][:3]
        out_of_scope = [q for q in questions if q.category == "out_of_scope"][:2]
        questions = direct + multi_doc + out_of_scope
        print(
            f"  Selected {len(questions)} questions: "
            f"{len(direct)} direct, {len(multi_doc)} multi_doc, {len(out_of_scope)} out_of_scope"
        )

    # Run evaluation
    results = []
    for i, question in enumerate(questions):
        print(f"\n  [{i + 1}/{len(questions)}] {question.id[:30]}...")

        def generate_fn(q: str, ctx: str) -> str:
            return generator.generate(q, ctx)

        # Use Langfuse tracing if enabled (pass generator for token tracking)
        if runner.langfuse:
            result = runner._evaluate_with_langfuse(question, generate_fn, generator=generator)
        else:
            result = runner.evaluate_question(question, generate_fn)
            # Capture token usage (only needed when not using Langfuse)
            if generator.last_usage:
                result.input_tokens = generator.last_usage.input_tokens
                result.output_tokens = generator.last_usage.output_tokens
                result.cost_usd = generator.last_usage.calculate_cost(model)

        results.append(result)
        print(
            f"    C={result.scores.correctness:.2f} "
            f"F={result.scores.faithfulness:.2f} "
            f"R={result.scores.relevance:.2f} "
            f"${result.cost_usd:.6f}"
        )

    # Compute aggregates
    aggregate = runner.compute_aggregate_scores(results)

    # Flush Langfuse
    if runner.langfuse:
        runner.langfuse.flush()

    return ModelResult(
        model=model,
        avg_correctness=aggregate["avg_correctness"],
        avg_faithfulness=aggregate["avg_faithfulness"],
        avg_relevance=aggregate["avg_relevance"],
        avg_latency_ms=aggregate["avg_total_latency_ms"],
        total_cost_usd=aggregate["total_cost_usd"],
        num_questions=aggregate["num_questions"],
    )


def print_comparison_table(results: list[ModelResult], title: str) -> None:
    """Print a formatted comparison table."""
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"{'=' * 80}")

    # Header
    print(
        f"{'Model':<20} | {'Correct':>8} | {'Faithful':>8} | "
        f"{'Relevant':>8} | {'Latency':>8} | {'Cost':>10} | {'Quality':>7}"
    )
    print("-" * 80)

    # Sort by quality score
    sorted_results = sorted(results, key=lambda r: r.quality_score, reverse=True)

    for r in sorted_results:
        print(
            f"{r.short_name():<20} | {r.avg_correctness:>8.3f} | {r.avg_faithfulness:>8.3f} | "
            f"{r.avg_relevance:>8.3f} | {r.avg_latency_ms:>6.0f}ms | "
            f"${r.total_cost_usd:>9.6f} | {r.quality_score:>7.3f}"
        )

    print("-" * 80)


def select_winners(results: list[ModelResult], top_n: int = 2) -> list[str]:
    """
    Select top models for full evaluation.

    Selection criteria:
    - Primary: Quality score (weighted average of correctness, faithfulness, relevance)
    - Tie-breaker: Lower cost

    Args:
        results: List of ModelResult from mini-eval
        top_n: Number of models to select

    Returns:
        List of model IDs for full evaluation
    """
    # Sort by quality score (descending), then by cost (ascending)
    sorted_results = sorted(results, key=lambda r: (-r.quality_score, r.total_cost_usd))

    winners = [r.model for r in sorted_results[:top_n]]

    print(f"\nWinners for full evaluation: {', '.join(winners)}")

    return winners


def main():
    parser = argparse.ArgumentParser(
        description="Compare LLM models for RAG answer generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="Qdrant collection to evaluate against",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_MODELS,
        help=f"Models to compare (default: {DEFAULT_MODELS})",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="backend/app/evaluation/datasets/rag_eval.yaml",
        help="Path to evaluation dataset YAML",
    )
    parser.add_argument(
        "--mini-eval-size",
        type=int,
        default=10,
        help="Number of questions for mini-eval (default: 10)",
    )
    parser.add_argument(
        "--skip-full-eval",
        action="store_true",
        help="Only run mini-eval, skip full evaluation",
    )
    parser.add_argument(
        "--full-eval-winners",
        type=int,
        default=2,
        help="Number of top models to run full eval on (default: 2)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/evaluations",
        help="Directory to save evaluation results",
    )

    args = parser.parse_args()

    print("=" * 80)
    print("LLM Model Comparison for RAG")
    print("=" * 80)
    print(f"Collection:      {args.collection}")
    print(f"Models:          {args.models}")
    print(f"Mini-eval size:  {args.mini_eval_size} questions")
    print(f"Full eval:       {'skipped' if args.skip_full_eval else f'top {args.full_eval_winners} models'}")
    print(f"Langfuse:        {'enabled' if settings.langfuse_enabled else 'disabled'}")
    print()

    # Check collection exists
    from backend.app.rag.retriever import QdrantRetriever

    retriever = QdrantRetriever(collection_name=args.collection)
    if not retriever.collection_exists():
        print(f"Error: Collection '{args.collection}' does not exist")
        sys.exit(1)

    info = retriever.get_collection_info()
    print(f"Collection info: {info.get('points_count', 'unknown')} vectors")

    # Phase 1: Mini-eval on all models
    print("\n" + "=" * 80)
    print("PHASE 1: Mini-Eval")
    print("=" * 80)

    mini_results = []
    for model in args.models:
        try:
            result = run_evaluation_for_model(
                model=model,
                collection=args.collection,
                dataset_path=args.dataset,
                max_questions=args.mini_eval_size,
                experiment_tag="phase2_mini_eval",
            )
            mini_results.append(result)
        except Exception as e:
            print(f"\nError evaluating {model}: {e}")
            continue

    if not mini_results:
        print("Error: No models completed evaluation")
        sys.exit(1)

    print_comparison_table(mini_results, f"Mini-Eval Results ({args.mini_eval_size} questions)")

    # Save mini-eval results
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mini_eval_file = output_dir / f"mini_eval_{timestamp}.json"

    mini_eval_data = {
        "timestamp": datetime.now().isoformat(),
        "collection": args.collection,
        "num_questions": args.mini_eval_size,
        "results": [
            {
                "model": r.model,
                "avg_correctness": r.avg_correctness,
                "avg_faithfulness": r.avg_faithfulness,
                "avg_relevance": r.avg_relevance,
                "avg_latency_ms": r.avg_latency_ms,
                "total_cost_usd": r.total_cost_usd,
                "quality_score": r.quality_score,
            }
            for r in mini_results
        ],
    }

    mini_eval_file.write_text(json.dumps(mini_eval_data, indent=2))
    print(f"\nMini-eval results saved to: {mini_eval_file}")

    # Phase 2: Full eval on winners
    if args.skip_full_eval:
        print("\nSkipping full evaluation (--skip-full-eval)")
        return

    winners = select_winners(mini_results, top_n=args.full_eval_winners)

    print("\n" + "=" * 80)
    print("PHASE 2: Full Evaluation")
    print("=" * 80)

    full_results = []
    for model in winners:
        try:
            result = run_evaluation_for_model(
                model=model,
                collection=args.collection,
                dataset_path=args.dataset,
                max_questions=None,  # Full eval
                experiment_tag="phase2_full_eval",
            )
            full_results.append(result)
        except Exception as e:
            print(f"\nError evaluating {model}: {e}")
            continue

    if full_results:
        print_comparison_table(full_results, "Full Eval Results (all questions)")

        # Save full-eval results
        full_eval_file = output_dir / f"full_eval_{timestamp}.json"

        full_eval_data = {
            "timestamp": datetime.now().isoformat(),
            "collection": args.collection,
            "results": [
                {
                    "model": r.model,
                    "avg_correctness": r.avg_correctness,
                    "avg_faithfulness": r.avg_faithfulness,
                    "avg_relevance": r.avg_relevance,
                    "avg_latency_ms": r.avg_latency_ms,
                    "total_cost_usd": r.total_cost_usd,
                    "num_questions": r.num_questions,
                    "quality_score": r.quality_score,
                }
                for r in full_results
            ],
        }

        full_eval_file.write_text(json.dumps(full_eval_data, indent=2))
        print(f"\nFull-eval results saved to: {full_eval_file}")

        # Print final recommendation
        best = sorted(full_results, key=lambda r: r.quality_score, reverse=True)[0]
        print("\n" + "=" * 80)
        print("RECOMMENDATION")
        print("=" * 80)
        print(f"Best model: {best.model}")
        print(f"  Quality score:  {best.quality_score:.3f}")
        print(f"  Correctness:    {best.avg_correctness:.3f}")
        print(f"  Faithfulness:   {best.avg_faithfulness:.3f}")
        print(f"  Relevance:      {best.avg_relevance:.3f}")
        print(f"  Avg latency:    {best.avg_latency_ms:.0f}ms")
        print(f"  Total cost:     ${best.total_cost_usd:.6f}")

        # Cost comparison
        cheapest = sorted(full_results, key=lambda r: r.total_cost_usd)[0]
        if cheapest.model != best.model:
            cost_diff = ((best.total_cost_usd - cheapest.total_cost_usd) / cheapest.total_cost_usd) * 100
            quality_diff = ((best.quality_score - cheapest.quality_score) / cheapest.quality_score) * 100
            print(f"\nNote: {best.short_name()} is {cost_diff:.1f}% more expensive than {cheapest.short_name()}")
            print(f"      but provides {quality_diff:.1f}% better quality")

    print("\nModel comparison complete!")


if __name__ == "__main__":
    main()
