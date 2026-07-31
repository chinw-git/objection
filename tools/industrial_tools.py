"""
tools/industrial_tools.py

CrewAI tool wrappers around the existing, tested classification pipeline.
Each tool wraps a plain Python function — no logic duplicated here.
"""

from crewai.tools import tool
from agents.pta_research_agent import research_case
from agents.industrial_similar_case_recommender_agent import recommend_from_precedent
from agents.industrial_rfi_recommender_agent import recommend_next_steps
from agents.industrial_classifier_agent_complexity import classify_case


@tool("PTA Research Tool")
def pta_research_tool(case_text: str, dev: str) -> dict:
    """Retrieves relevant rubric section and PTA provisions for a case."""
    return research_case(case_text=case_text, dev=dev)


@tool("Precedent Retrieval Tool")
def precedent_tool(explanatory_note: str, assigned_category: str) -> dict:
    """Retrieves similar past cases matching the assigned category."""
    return recommend_from_precedent(explanatory_note, assigned_category)


@tool("RFI Recommendation Tool")
def rfi_tool(explanatory_note: str, assigned_category: str, dev: str = "") -> dict:
    """Recommends next-step actions for the valuer based on the classification."""
    return recommend_next_steps(explanatory_note, assigned_category, dev)


from industrial_pipeline import run_pipeline

@tool("Full PTA Classification Pipeline")
def full_classification_tool(explanatory_note: str, file_upload_count: int, dev: str) -> dict:
    return run_pipeline(explanatory_note, file_upload_count, dev)