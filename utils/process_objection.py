import json

from objection_crew import create_obj_assessment_crew
from tools.retrieve_past_obj import retrieve_similar_cases


def process_objection(
    objection: str,
    model: str,
    temperature: float,
):
    """
    Run the complete objection assessment pipeline
    for a single objection.
    """

    # --------------------------------
    # Run Crew
    # --------------------------------

    crew = create_obj_assessment_crew(
        model=model,
        temperature=temperature,
    )

    result = crew.kickoff(
        inputs={
            "objection": objection,
        }
    )

    result_json = json.loads(result.raw)
    
    classification = result_json["classification"]
    recommendation = result_json["recommendation"]

    # -----------------------------
    # Retrieve similar past cases
    # -----------------------------
    similar_cases = retrieve_similar_cases(objection)

    return {
        "grounds_of_objection": objection,
        "classification": classification,
        "recommendation": recommendation,
        "similar_cases": similar_cases,
    }