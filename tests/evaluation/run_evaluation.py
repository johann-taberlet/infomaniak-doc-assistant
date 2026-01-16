"""RAG Quality Evaluation Script.

This script tests the chatbot against 20 predefined questions and compares
responses with ground truth extracted from the documentation.
"""

import json
import time
from datetime import datetime
from pathlib import Path

import httpx

BASE_URL = "http://localhost:8000"
SCRIPT_DIR = Path(__file__).parent
QUESTIONS_FILE = SCRIPT_DIR / "test_questions.json"
RESPONSES_FILE = SCRIPT_DIR / "chatbot_responses.json"
REPORT_FILE = SCRIPT_DIR / "comparison_report.md"


def load_questions() -> list[dict]:
    """Load test questions from JSON file."""
    with open(QUESTIONS_FILE) as f:
        return json.load(f)


def test_single_question(client: httpx.Client, question: str) -> dict:
    """Send a question to the chatbot and get the response."""
    response = client.post(
        f"{BASE_URL}/chat",
        json={"message": question},
    )
    response.raise_for_status()
    return response.json()


def evaluate_response(actual: str, key_points: list[str]) -> dict:
    """Evaluate how many key points are present in the response."""
    actual_lower = actual.lower()
    found = []
    missing = []

    # Synonyms for common terms
    synonyms = {
        "need": ["must have", "require", "prerequisite", "need"],
        "must be": ["need to be", "have to be", "must be", "be the", "be a"],
        "stops": ["ends", "stop", "no longer accessible", "will stop"],
        "available": ["available", "supported", "work"],
        "not available": ["not available", "not supported", "doesn't work", "cannot", "not yet"],
        "appears below": ["appear below", "appears below", "will appear", "displayed below"],
        "translates to": ["translate", "translated", "translation", "automatic"],
    }

    for point in key_points:
        point_lower = point.lower()

        # Direct substring match
        if point_lower in actual_lower:
            found.append(point)
            continue

        # Check with synonym expansion
        synonym_matched = False
        for key, syns in synonyms.items():
            if key in point_lower:
                # Try each synonym
                for syn in syns:
                    test_point = point_lower.replace(key, syn)
                    if test_point in actual_lower:
                        found.append(point)
                        synonym_matched = True
                        break
                if synonym_matched:
                    break

        if synonym_matched:
            continue

        # Handle compound terms (e.g., "private/public" -> check both "private" and "public")
        # Split by common separators: /, or, and, ,
        import re
        sub_terms = re.split(r'[/,]|\s+or\s+|\s+and\s+', point_lower)
        sub_terms = [t.strip() for t in sub_terms if t.strip()]

        if len(sub_terms) > 1:
            # For compound terms, check if most sub-terms are present
            sub_matches = sum(1 for t in sub_terms if t in actual_lower)
            if sub_matches >= len(sub_terms) * 0.5:
                found.append(point)
                continue

        # Check for partial matches (words) with 50% threshold
        words = point_lower.split()
        # Also split by slash for words like private/public
        expanded_words = []
        for w in words:
            if '/' in w:
                expanded_words.extend(w.split('/'))
            else:
                expanded_words.append(w)

        # Filter out common words for better matching
        content_words = [w for w in expanded_words if len(w) > 2 and w not in {'the', 'and', 'for', 'with', 'can', 'set'}]
        if content_words:
            matches = sum(1 for w in content_words if w in actual_lower)
            if matches >= len(content_words) * 0.5:  # 50% threshold
                found.append(point)
            else:
                missing.append(point)
        else:
            # All words were filtered, check original
            matches = sum(1 for w in expanded_words if w in actual_lower)
            if matches >= len(expanded_words) * 0.5:
                found.append(point)
            else:
                missing.append(point)

    coverage = len(found) / len(key_points) if key_points else 0

    # Score: 3=Complete (>=80%), 2=Partial (>=50%), 1=Minimal (>=20%), 0=Wrong (<20%)
    if coverage >= 0.8:
        score = 3
        rating = "Complete"
    elif coverage >= 0.5:
        score = 2
        rating = "Partial"
    elif coverage >= 0.2:
        score = 1
        rating = "Minimal"
    else:
        score = 0
        rating = "Wrong"

    return {
        "score": score,
        "rating": rating,
        "coverage": round(coverage * 100, 1),
        "found": found,
        "missing": missing,
    }


def run_evaluation() -> list[dict]:
    """Run the full evaluation against the chatbot."""
    questions = load_questions()
    results = []

    print(f"Starting evaluation with {len(questions)} questions...")
    print(f"Target: {BASE_URL}")
    print("-" * 60)

    with httpx.Client(timeout=120.0) as client:
        # Test health first
        try:
            health = client.get(f"{BASE_URL}/health")
            health.raise_for_status()
            print("Server health check: OK")
        except Exception as e:
            print(f"Server health check FAILED: {e}")
            print("Make sure the server is running: uv run uvicorn app.main:app")
            return []

        print("-" * 60)

        for i, q in enumerate(questions):
            print(f"[{i+1}/{len(questions)}] {q['question'][:50]}...")
            start_time = time.time()

            try:
                response = test_single_question(client, q["question"])
                elapsed = time.time() - start_time

                evaluation = evaluate_response(
                    response.get("answer", ""),
                    q.get("key_points", [])
                )

                result = {
                    "id": q["id"],
                    "question": q["question"],
                    "ground_truth": q["ground_truth"],
                    "key_points": q["key_points"],
                    "actual_response": response.get("answer", ""),
                    "sources": response.get("sources", []),
                    "source_file": q["source_file"],
                    "evaluation": evaluation,
                    "response_time_seconds": round(elapsed, 2),
                }
                results.append(result)

                print(f"    Score: {evaluation['rating']} ({evaluation['coverage']}% coverage) - {elapsed:.1f}s")

            except Exception as e:
                print(f"    ERROR: {e}")
                results.append({
                    "id": q["id"],
                    "question": q["question"],
                    "error": str(e),
                })

            # Small delay between requests
            time.sleep(0.5)

    return results


def generate_report(results: list[dict]) -> str:
    """Generate a markdown comparison report."""
    # Calculate aggregate metrics
    valid_results = [r for r in results if "evaluation" in r]
    if not valid_results:
        return "# Evaluation Report\n\nNo valid results to report."

    total_score = sum(r["evaluation"]["score"] for r in valid_results)
    max_score = len(valid_results) * 3
    avg_score = total_score / len(valid_results)
    avg_coverage = sum(r["evaluation"]["coverage"] for r in valid_results) / len(valid_results)
    avg_time = sum(r.get("response_time_seconds", 0) for r in valid_results) / len(valid_results)

    complete = sum(1 for r in valid_results if r["evaluation"]["rating"] == "Complete")
    partial = sum(1 for r in valid_results if r["evaluation"]["rating"] == "Partial")
    minimal = sum(1 for r in valid_results if r["evaluation"]["rating"] == "Minimal")
    wrong = sum(1 for r in valid_results if r["evaluation"]["rating"] == "Wrong")

    # Build report
    lines = [
        "# RAG Quality Evaluation Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Questions Tested:** {len(results)}",
        "",
        "---",
        "",
        "## Summary Metrics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Score | {total_score}/{max_score} ({total_score/max_score*100:.1f}%) |",
        f"| Average Score | {avg_score:.2f}/3.00 |",
        f"| Average Coverage | {avg_coverage:.1f}% |",
        f"| Average Response Time | {avg_time:.1f}s |",
        "",
        "## Rating Distribution",
        "",
        f"| Rating | Count | Percentage |",
        f"|--------|-------|------------|",
        f"| Complete (3) | {complete} | {complete/len(valid_results)*100:.1f}% |",
        f"| Partial (2) | {partial} | {partial/len(valid_results)*100:.1f}% |",
        f"| Minimal (1) | {minimal} | {minimal/len(valid_results)*100:.1f}% |",
        f"| Wrong (0) | {wrong} | {wrong/len(valid_results)*100:.1f}% |",
        "",
        "---",
        "",
        "## Detailed Results",
        "",
    ]

    # Group by product
    for product, prefix in [("kMeet", "kmeet/"), ("kDrive", "kdrive/"), ("kChat", "kchat/")]:
        product_results = [r for r in valid_results if r["source_file"].startswith(prefix)]
        if not product_results:
            continue

        lines.append(f"### {product} ({len(product_results)} questions)")
        lines.append("")

        for r in product_results:
            eva = r["evaluation"]
            emoji = {"Complete": "+", "Partial": "~", "Minimal": "-", "Wrong": "x"}[eva["rating"]]
            lines.append(f"#### Q{r['id']}: {r['question']}")
            lines.append("")
            lines.append(f"**Rating:** [{emoji}] {eva['rating']} ({eva['coverage']}% coverage)")
            lines.append("")
            lines.append("**Response excerpt:**")
            response_excerpt = r["actual_response"][:500] + "..." if len(r["actual_response"]) > 500 else r["actual_response"]
            lines.append(f"> {response_excerpt}")
            lines.append("")
            if eva["found"]:
                lines.append(f"**Key points found:** {', '.join(eva['found'])}")
            if eva["missing"]:
                lines.append(f"**Key points missing:** {', '.join(eva['missing'])}")
            lines.append("")

    # Recommendations
    lines.extend([
        "---",
        "",
        "## Recommendations",
        "",
    ])

    if avg_coverage < 50:
        lines.append("- **Low coverage detected.** Consider:")
        lines.append("  - Increasing RAG_TOP_K to retrieve more documents")
        lines.append("  - Lowering RAG_SIMILARITY_THRESHOLD for broader matches")
        lines.append("  - Improving the embedding model or chunk size")
    elif avg_coverage < 70:
        lines.append("- **Moderate coverage.** Consider:")
        lines.append("  - Fine-tuning the system prompt for better information extraction")
        lines.append("  - Reviewing chunk overlap settings")
    else:
        lines.append("- **Good coverage achieved.** Focus on:")
        lines.append("  - Response latency optimization")
        lines.append("  - Edge case handling")

    if wrong > 0:
        lines.append(f"- **{wrong} wrong responses detected.** Review these questions for retrieval issues.")

    return "\n".join(lines)


def main():
    """Main entry point."""
    print("=" * 60)
    print("RAG Quality Evaluation")
    print("=" * 60)
    print()

    # Run evaluation
    results = run_evaluation()

    if not results:
        print("No results to save. Exiting.")
        return

    # Save raw results
    print()
    print("-" * 60)
    print(f"Saving results to {RESPONSES_FILE}...")
    with open(RESPONSES_FILE, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Generate and save report
    print(f"Generating report at {REPORT_FILE}...")
    report = generate_report(results)
    with open(REPORT_FILE, "w") as f:
        f.write(report)

    print()
    print("=" * 60)
    print("Evaluation complete!")
    print(f"- Results: {RESPONSES_FILE}")
    print(f"- Report: {REPORT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
