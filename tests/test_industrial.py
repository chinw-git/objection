"""Run each component standalone to isolate failures before full pipeline test."""

# Layer 0: is vectordb even populated?
def test_vectordb_exists():
    import chromadb
    client = chromadb.PersistentClient(path="vectordb/")
    collections = client.list_collections()
    print("Collections found:", [c.name for c in collections])
    assert len(collections) > 0, "vectordb/ is empty — run pta_embedding_task first"



# Layer 1: rubric retrieval alone
def test_rubric_retrieval():
    from utils.industrial_context_loader import get_rubric_context
    result = get_rubric_context(query="AV too high no other reason")
    print("\n--- Rubric retrieval ---")
    print(result[:500])
    assert len(result) > 0


# Layer 2: research agent alone (2 LLM calls)
def test_research_agent():
    from agents.pta_research_agent import research_case
    result = research_case(case_text="AV is too high, no other reason given.", dev="Non-strata")
    print("\n--- Research agent output ---")
    for k, v in result.items():
        print(f"\n[{k}]\n{v[:300] if isinstance(v, str) else v}")
    assert "pta_explanation" in result


# Layer 3: full classifier pipeline (3 LLM calls)
def test_classifier_full():
    from agents.industrial_classifier_agent_complexity import classify_case
    result = classify_case(
        explanatory_note="AV is too high compared to neighbouring units, no other reason given.",
        file_upload_count=0,
        dev="Non-strata",
    )
    print("\n--- Final classification ---")
    print(f"Category: {result['category']}")
    print(f"Reason: {result['reason']}")
    assert result["category"] in [
        "Easy - Disallow", "Easy - RFI (minimal)",
        "Medium - RFI (extensive)", "Medium - Strata Owners", "Difficult"
    ]


if __name__ == "__main__":
    print("=== Layer 0: vectordb ===")
    test_vectordb_exists()

    print("\n=== Layer 1: rubric retrieval ===")
    test_rubric_retrieval()

    print("\n=== Layer 2: research agent ===")
    test_research_agent()

    print("\n=== Layer 3: full classifier ===")
    test_classifier_full()