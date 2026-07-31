"""
industrial_pipeline.py

Single entry point for the full classification pipeline. Both industrial_app.py
(Streamlit) and industrialcrew.py (CrewAI) call this directly, so there's one
place the actual pipeline logic lives.
"""

from agents.industrial_classifier_agent_complexity import classify_case


def run_pipeline(explanatory_note: str, file_upload_count: int, dev: str) -> dict:
    """
    Runs the full deterministic classification pipeline:
    PTA research -> classification -> precedent check -> next-step recommendation.
    """
    return classify_case(
        explanatory_note=explanatory_note,
        file_upload_count=file_upload_count,
        dev=dev,
    )


if __name__ == "__main__":
    result = run_pipeline(
        explanatory_note="AV is too high compared to neighbouring units, no other reason given.",
        file_upload_count=0,
        dev="Non-strata",
    )
    print(f"Category: {result['category']}")
    print(f"Reason: {result['reason']}")