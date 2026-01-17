"""Re-test the 5 failing queries after full ingestion."""

import json
import httpx

API_URL = "http://localhost:8000"

FAILING_QUERIES = [
    {
        "id": "Q5",
        "question": "How do I sign a PDF document in kDrive?",
        "key_terms": ["Edit button", "Signature icon", "draw", "type", "import image", "save"],
    },
    {
        "id": "Q13",
        "question": "How do I restore my entire kDrive to a previous state (rewind)?",
        "key_terms": ["Settings", "Restore", "Administrator", "date", "90 days", "3 months"],
    },
    {
        "id": "Q15",
        "question": "How do I set a reminder for a kChat message?",
        "key_terms": ["hover", "action menu", "three dots", "Remind", "notification"],
    },
    {
        "id": "Q7",
        "question": "How can I search for files within kDrive?",
        "key_terms": ["search bar", "CMD-F", "CTRL-F", "advanced search", "content search", "filter"],
    },
    {
        "id": "Q12",
        "question": "How do I manage deleted files and the trash in kDrive?",
        "key_terms": ["trash", "30 days", "365 days", "retention", "restore", "permanently delete"],
    },
]


def test_query(query_info: dict) -> dict:
    """Test a single query and check for key terms."""
    question = query_info["question"]
    key_terms = query_info["key_terms"]

    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            f"{API_URL}/chat",
            json={"message": question},
        )
        data = response.json()
        answer = data.get("answer", "")
        sources = data.get("sources", [])

    # Check which key terms are present
    answer_lower = answer.lower()
    found_terms = []
    missing_terms = []
    for term in key_terms:
        if term.lower() in answer_lower:
            found_terms.append(term)
        else:
            missing_terms.append(term)

    coverage = len(found_terms) / len(key_terms) * 100

    return {
        "id": query_info["id"],
        "question": question,
        "answer_preview": answer[:500] + "..." if len(answer) > 500 else answer,
        "sources": sources[:3],
        "found_terms": found_terms,
        "missing_terms": missing_terms,
        "coverage": coverage,
    }


def main():
    print("Re-testing 5 failing queries after full document ingestion")
    print("=" * 80)

    results = []
    for q in FAILING_QUERIES:
        print(f"\nTesting {q['id']}: {q['question'][:50]}...")
        result = test_query(q)
        results.append(result)

        status = "✓ PASS" if result["coverage"] >= 50 else "✗ FAIL"
        print(f"  {status} - Coverage: {result['coverage']:.0f}%")
        print(f"  Found: {result['found_terms']}")
        print(f"  Missing: {result['missing_terms']}")
        print(f"  Sources: {[s.split('/')[-1][:30] for s in result['sources']]}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total_pass = sum(1 for r in results if r["coverage"] >= 50)
    print(f"\nPassed: {total_pass}/5")

    for r in results:
        status = "✓" if r["coverage"] >= 50 else "✗"
        print(f"  {status} {r['id']}: {r['coverage']:.0f}% coverage")

    # Save full results
    with open("tests/evaluation/retest_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to tests/evaluation/retest_results.json")


if __name__ == "__main__":
    main()
