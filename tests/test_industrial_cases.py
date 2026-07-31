"""Hand-labeled test cases — expand this as you get real examples from Freya/Jayden."""

TEST_CASES = [
    {
        "explanatory_note": "AV is too high, no other reason given.",
        "file_upload_count": 0,
        "dev": "Non-strata",
        "expected": "Easy - Disallow",
    },
    {
        "explanatory_note": "Unit has been vacant since March, requesting AV adjustment for vacancy.",
        "file_upload_count": 1,
        "dev": "Non-strata",
        "expected": "Easy - RFI (minimal)",
    },
    {
        "explanatory_note": "This is a strata-titled industrial unit, requesting review.",
        "file_upload_count": 0,
        "dev": "Strata",
        "expected": "Medium - Strata Owners",
    },
    # Add more as Freya/Jayden flag real edge cases
]


def run_accuracy_check():
    from agents.industrial_classifier_agent_complexity import classify_case

    correct = 0
    for i, case in enumerate(TEST_CASES):
        result = classify_case(
            explanatory_note=case["explanatory_note"],
            file_upload_count=case["file_upload_count"],
            dev=case["dev"],
        )
        match = result["category"] == case["expected"]
        correct += match
        status = "✓" if match else "✗"
        print(f"{status} Case {i}: expected={case['expected']!r} got={result['category']!r}")
        if not match:
            print(f"   reason given: {result['reason']}")

    print(f"\nAccuracy: {correct}/{len(TEST_CASES)}")


if __name__ == "__main__":
    run_accuracy_check()