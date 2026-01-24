#!/usr/bin/env python3
"""
Run RAG evaluation on a Qdrant collection.

This script loads an evaluation dataset, runs retrieval and scoring,
and logs results to Langfuse for A/B comparison.

Usage:
    uv run python scripts/evaluate.py --collection infomaniak_baseline
    uv run python scripts/evaluate.py --collection infomaniak_semantic --max-questions 10
    uv run python scripts/evaluate.py --collection infomaniak_baseline --tag experiment:v1

Examples:
    # Evaluate baseline collection (dense retrieval)
    uv run python scripts/evaluate.py --collection infomaniak_recursive_1500_no_images

    # Quick test with 5 questions
    uv run python scripts/evaluate.py --collection infomaniak_baseline --max-questions 5

    # Run with custom experiment tag
    uv run python scripts/evaluate.py \\
        --collection infomaniak_semantic_no_images \\
        --tag experiment:chunking_v1 \\
        --tag strategy:semantic

    # Run on specific product
    uv run python scripts/evaluate.py --collection infomaniak_baseline --product kmeet

    # Run with a specific generation model
    uv run python scripts/evaluate.py \\
        --collection infomaniak_full_doc_no_images \\
        --model qwen/qwen3-8b \\
        --max-questions 10

    # Hybrid retrieval evaluation
    uv run python scripts/evaluate.py \\
        --collection infomaniak_hybrid_full_doc_no_images \\
        --hybrid-collection \\
        --retrieval-mode hybrid \\
        --enable-normalization \\
        --model mistralai/mistral-nemo \\
        --tag config:normalized_bm25

    # HyDE + Dense retrieval
    uv run python scripts/evaluate.py \\
        --collection infomaniak_full_doc_no_images \\
        --enable-hyde \\
        --model mistralai/mistral-nemo \\
        --tag config:hyde_dense

    # HyDE + Hybrid (best expected config)
    uv run python scripts/evaluate.py \\
        --collection infomaniak_hybrid_full_doc_no_images \\
        --hybrid-collection \\
        --retrieval-mode hybrid \\
        --enable-hyde \\
        --enable-normalization \\
        --model mistralai/mistral-nemo \\
        --tag config:hyde_hybrid
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.core.config import settings
from backend.app.evaluation.runner import EvaluationRunner


def main():
    parser = argparse.ArgumentParser(
        description="Run RAG evaluation and log to Langfuse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="Qdrant collection name to evaluate",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="backend/app/evaluation/datasets/rag_eval.yaml",
        help="Path to evaluation dataset YAML (default: %(default)s)",
    )
    parser.add_argument(
        "--max-questions",
        type=int,
        default=None,
        help="Maximum number of questions to evaluate (for testing)",
    )
    parser.add_argument(
        "--tag",
        action="append",
        dest="tags",
        default=[],
        help="Experiment tags in key:value format (can be specified multiple times)",
    )
    parser.add_argument(
        "--product",
        type=str,
        default=None,
        choices=["kdrive", "kmeet", "kchat"],
        help="Filter evaluation to a specific product",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file for detailed results (JSON)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output for each question",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="LLM model for answer generation (e.g., qwen/qwen3-8b, mistralai/mistral-nemo)",
    )

    # Retrieval enhancement options
    parser.add_argument(
        "--retrieval-mode",
        type=str,
        default="dense",
        choices=["dense", "sparse", "hybrid"],
        help="Retrieval mode: dense (default), sparse (BM25), or hybrid (RRF fusion)",
    )
    parser.add_argument(
        "--hybrid-collection",
        action="store_true",
        help="Use HybridRetriever instead of QdrantRetriever (required for sparse/hybrid modes)",
    )
    parser.add_argument(
        "--enable-hyde",
        action="store_true",
        help="Enable HyDE (Hypothetical Document Embeddings) for query expansion",
    )
    parser.add_argument(
        "--enable-normalization",
        action="store_true",
        help="Enable BM25 vocabulary normalization for kSuite terms",
    )

    args = parser.parse_args()

    # Parse tags
    experiment_tags = {}
    for tag in args.tags:
        if ":" in tag:
            key, value = tag.split(":", 1)
            experiment_tags[key] = value
        else:
            experiment_tags[tag] = "true"

    # Add default tags
    experiment_tags.setdefault("collection", args.collection)
    experiment_tags.setdefault("timestamp", datetime.now().isoformat())
    if args.model:
        experiment_tags["model"] = args.model

    # Add retrieval config tags
    experiment_tags["retrieval_mode"] = args.retrieval_mode
    if args.enable_hyde:
        experiment_tags["hyde"] = "enabled"
    if args.enable_normalization:
        experiment_tags["normalization"] = "enabled"

    print("=" * 60)
    print("RAG Evaluation")
    print("=" * 60)
    print(f"Collection:      {args.collection}")
    print(f"Dataset:         {args.dataset}")
    print(f"Max questions:   {args.max_questions or 'all'}")
    print(f"Product filter:  {args.product or 'none'}")
    print(f"Model:           {args.model or 'none (retrieval only)'}")
    print(f"Retrieval mode:  {args.retrieval_mode}")
    print(f"Hybrid coll.:    {args.hybrid_collection}")
    print(f"HyDE:            {args.enable_hyde}")
    print(f"Normalization:   {args.enable_normalization}")
    print(f"Experiment tags: {experiment_tags}")
    print(f"Langfuse:        {'enabled' if settings.langfuse_enabled else 'disabled'}")
    print()

    # Initialize retriever based on configuration
    retriever = None
    if args.hybrid_collection:
        from backend.app.rag.hybrid_retriever import (
            HybridConfig,
            HybridRetriever,
            RetrievalMode,
        )

        # Map string mode to enum
        mode_map = {
            "dense": RetrievalMode.DENSE,
            "sparse": RetrievalMode.SPARSE,
            "hybrid": RetrievalMode.HYBRID,
        }

        config = HybridConfig(
            mode=mode_map[args.retrieval_mode],
            enable_hyde=args.enable_hyde,
            enable_normalization=args.enable_normalization,
        )
        retriever = HybridRetriever(collection_name=args.collection, config=config)
    else:
        from backend.app.rag.retriever import QdrantRetriever

        retriever = QdrantRetriever(collection_name=args.collection)

        # Warn if using advanced features without hybrid collection
        if args.retrieval_mode != "dense":
            print(f"Warning: --retrieval-mode {args.retrieval_mode} requires --hybrid-collection")
            print("Falling back to dense retrieval")
            experiment_tags["retrieval_mode"] = "dense"

    # Check if collection exists
    if not retriever.collection_exists():
        print(f"Error: Collection '{args.collection}' does not exist")
        if args.hybrid_collection:
            print("Run ingest_hybrid.py first to create the hybrid collection")
        else:
            print("Run ingest.py first to create the collection")
        sys.exit(1)

    info = retriever.get_collection_info()
    print(f"Collection info: {info.get('points_count', 'unknown')} vectors")
    print()

    # Initialize runner with configured retriever
    runner = EvaluationRunner(
        collection_name=args.collection,
        experiment_tags=experiment_tags,
        retriever=retriever,
    )

    # Initialize answer generator if model is specified
    generator = None
    if args.model:
        from backend.app.rag.generator import AnswerGenerator

        generator = AnswerGenerator(model=args.model)
        print(f"Initialized generator: {generator.get_model_short_name()}")
        print()

    # Load dataset and filter if needed
    print(f"Loading evaluation dataset from {args.dataset}...")
    questions = runner.load_dataset(args.dataset)

    if args.product:
        questions = [q for q in questions if q.product == args.product]
        print(f"  Filtered to {len(questions)} questions for product: {args.product}")
    else:
        print(f"  Loaded {len(questions)} questions")

    if args.max_questions:
        questions = questions[: args.max_questions]
        print(f"  Limited to {len(questions)} questions")

    print()

    # Run evaluation
    print("Running evaluation...")
    print("-" * 60)

    results = []
    for i, question in enumerate(questions):
        print(f"\n[{i + 1}/{len(questions)}] {question.id}: {question.question[:50]}...")

        # Create generate_answer_fn if generator is available
        generate_fn = None
        if generator:

            def generate_fn(q: str, ctx: str) -> str:
                return generator.generate(q, ctx)

        # Use Langfuse tracing if enabled (pass generator for token tracking)
        if runner.langfuse:
            result = runner._evaluate_with_langfuse(question, generate_fn, generator=generator)
        else:
            result = runner.evaluate_question(question, generate_fn)
            # Capture token usage from generator (only needed when not using Langfuse)
            if generator and generator.last_usage:
                result.input_tokens = generator.last_usage.input_tokens
                result.output_tokens = generator.last_usage.output_tokens
                result.cost_usd = generator.last_usage.calculate_cost(args.model)

        results.append(result)

        # Print scores
        print(f"  Correctness:  {result.scores.correctness:.2f}")
        print(f"  Faithfulness: {result.scores.faithfulness:.2f}")
        print(f"  Relevance:    {result.scores.relevance:.2f}")
        print(f"  Latency:      {result.total_latency_ms:.0f}ms")

        if generator and generator.last_usage:
            print(f"  Tokens:       {result.input_tokens} in / {result.output_tokens} out")
            print(f"  Cost:         ${result.cost_usd:.6f}")

        if args.verbose:
            print(f"  Context chunks: {result.num_chunks_retrieved}")
            print(f"  Answer preview: {result.generated_answer[:100]}...")

    print()
    print("-" * 60)

    # Compute aggregate scores
    aggregate = runner.compute_aggregate_scores(results)

    print("\nAggregate Scores")
    print("=" * 60)
    print(f"Questions evaluated: {aggregate['num_questions']}")
    print()
    print("Quality Metrics:")
    print(f"  Avg Correctness:  {aggregate['avg_correctness']:.3f}")
    print(f"  Avg Faithfulness: {aggregate['avg_faithfulness']:.3f}")
    print(f"  Avg Relevance:    {aggregate['avg_relevance']:.3f}")
    print()
    print("Performance Metrics:")
    print(f"  Avg Retrieval Latency:  {aggregate['avg_retrieval_latency_ms']:.0f}ms")
    print(f"  Avg Generation Latency: {aggregate['avg_generation_latency_ms']:.0f}ms")
    print(f"  Avg Total Latency:      {aggregate['avg_total_latency_ms']:.0f}ms")
    print(f"  Avg Chunks Retrieved:   {aggregate['avg_chunks_retrieved']:.1f}")

    # Print token/cost metrics if model was used
    if args.model and aggregate.get("total_input_tokens", 0) > 0:
        print()
        print("Cost Metrics:")
        print(f"  Total Input Tokens:  {aggregate['total_input_tokens']:,}")
        print(f"  Total Output Tokens: {aggregate['total_output_tokens']:,}")
        print(f"  Total Cost:          ${aggregate['total_cost_usd']:.6f}")
        print(f"  Avg Cost per Query:  ${aggregate['avg_cost_usd']:.6f}")

    # Always save detailed results to file
    # Use provided output path or auto-generate one
    if args.output:
        output_path = Path(args.output)
    else:
        # Auto-generate output path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_suffix = f"_{args.model.split('/')[-1]}" if args.model else ""
        output_filename = f"eval_{args.collection}{model_suffix}_{timestamp}.json"
        output_path = Path("data/evaluations") / output_filename

    output_data = {
        "collection": args.collection,
        "model": args.model,
        "dataset": args.dataset,
        "experiment_tags": experiment_tags,
        "aggregate_scores": aggregate,
        "results": [r.to_dict() for r in results],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"\nDetailed results saved to: {output_path}")

    # Flush Langfuse and print link if enabled
    if runner.langfuse:
        runner.langfuse.flush()
        print(f"\nView results in Langfuse: {settings.langfuse_host}")
        print(f"  Filter by tags: collection:{args.collection}")

    print("\nEvaluation complete!")


if __name__ == "__main__":
    main()
