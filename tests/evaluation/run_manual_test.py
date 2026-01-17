"""Run manual test questions against the API and log responses."""

import json
import time

import httpx

API_URL = "http://localhost:8000"
QUESTIONS_FILE = "tests/evaluation/manual_test_questions.json"
OUTPUT_FILE = "tests/evaluation/manual_test_responses.json"


def run_tests():
    """Run all manual test questions and save responses."""
    # Load questions
    with open(QUESTIONS_FILE) as f:
        questions = json.load(f)

    print(f"Running {len(questions)} questions against the API...")
    print("-" * 60)

    results = []

    with httpx.Client(timeout=120.0) as client:
        for i, q in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] {q['question'][:50]}...")

            start_time = time.time()

            try:
                response = client.post(
                    f"{API_URL}/chat",
                    json={"message": q["question"]},
                )
                response.raise_for_status()
                data = response.json()
                elapsed = time.time() - start_time

                result = {
                    "id": q["id"],
                    "question": q["question"],
                    "perfect_answer": q["perfect_answer"],
                    "source": q["source"],
                    "api_response": data.get("answer", ""),
                    "api_sources": data.get("sources", []),
                    "response_time": round(elapsed, 2),
                }
                print(f"    Done in {elapsed:.1f}s")

            except Exception as e:
                result = {
                    "id": q["id"],
                    "question": q["question"],
                    "perfect_answer": q["perfect_answer"],
                    "source": q["source"],
                    "api_response": f"ERROR: {str(e)}",
                    "api_sources": [],
                    "response_time": 0,
                }
                print(f"    ERROR: {e}")

            results.append(result)

    # Save results
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print("-" * 60)
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_tests()
