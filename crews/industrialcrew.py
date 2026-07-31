"""
industrialcrew.py

CrewAI setup wrapping the deterministic classification pipeline as a single tool.
Kept intentionally simple: one Agent, one Task, one Tool — the pipeline's internal
logic stays deterministic (tested via tests/test_industrial.py), CrewAI here just
provides the orchestration wrapper required for project integration.
"""

from crewai import Agent, Task, Crew, Process
from tools.industrial_tools import full_classification_tool

classifier_agent = Agent(
    role="PTA Complexity Classifier",
    goal="Classify property tax objection cases into the correct complexity category, "
         "grounded in PTA legal research, precedent, and produce concrete next steps.",
    backstory=(
        "An experienced IRAS valuer who applies the Property Tax Act rubric consistently, "
        "cites legal grounds precisely, checks decisions against historical precedent, "
        "and gives valuers clear, actionable next steps."
    ),
    tools=[full_classification_tool],
    verbose=True,
)


def run_crew(explanatory_note: str, file_upload_count: int, dev: str) -> dict:
    task = Task(
        description=(
            f"Classify this property tax objection case:\n"
            f"ExplanatoryNote: {explanatory_note}\n"
            f"FileUploadCount: {file_upload_count}\n"
            f"DEV: {dev}\n"
            f"Use the Full PTA Classification Pipeline tool to produce the result."
        ),
        expected_output="A JSON object with category, reason, precedent cases, and next steps.",
        agent=classifier_agent,
    )

    crew = Crew(
        agents=[classifier_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    return crew.kickoff()


if __name__ == "__main__":
    result = run_crew(
        explanatory_note="AV is too high compared to neighbouring units, no other reason given.",
        file_upload_count=0,
        dev="Non-strata",
    )
    print(result)