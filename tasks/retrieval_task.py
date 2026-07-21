from crewai import Task
from agents.retrieval_agent import retrieval_agent

retrieval_task = Task(

    description="""
Retrieve historical objections similar to:

{objection}

Return the retrieved cases exactly as provided.
Do not infer complexity.
Do not infer urgency.
Do not make recommendations.
""",

    expected_output="""
JSON containing retrieved historical cases.
""",

    agent=retrieval_agent
)