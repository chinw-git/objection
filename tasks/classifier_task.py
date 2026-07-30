from crewai import Task

from tasks.legislation_task import legislation_task
from agents.classifier_agent import classifier_agent
from utils.load_rubrics import load_rubrics

#load rubrics text file
rubrics = load_rubrics()

classifier_task = Task(

    description=f"""
    You are provided with

    1. The user's objection
    2. Relevant Property Tax Act sections retrieved by the previous legislation task
    3. The rubric containing the official criteria to determine complexity

    Rubric:

    {rubrics}


    Objection:

    {{objection}}

    Determine:

    1. The appropriate complexity category by applying the official complexity rubric. You MUST classify the objection into exactly ONE of the following categories:

    - EASY – DISALLOW
    - EASY – RFI (minimal)
    - MEDIUM – RFI (extensive)
    - DIFFICULT

    2. Identify the specific rubric criteria(s) that were triggered.

    3. Identify the relevant Property Tax Act sections that support your assessment.

    4. Explain how the objection satisfies the selected rubric category, citing both the rubric and the relevant Property Tax Act sections.

    Instructions:
    - Base your assessment only on the provided objection, the retrieved Property Tax Act sections, and the official rubric.
    - Do NOT use outside knowledge.
    - Do NOT use historical objection cases.
    - Do NOT create or infer additional complexity categories beyond the four listed above.
    """,

    expected_output="""
    Return ONLY a valid JSON object in the following format:

    {
    "complexity": "",
    "rubric_criteria": [
        ""
    ],
    "relevant_pta_sections": [
        {
        "section": "",
        "reason": ""
        }
    ],
    "reasoning": ""
    }

    Do not include markdown, code fences, or any additional text outside the JSON object.
    """,

    agent=classifier_agent,
    context=[legislation_task],
)