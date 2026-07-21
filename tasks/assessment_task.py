from crewai import Task


def create_assessment_task(agent, retrieval_task):

    return Task(

        description="""
You are assessing a new property objection.

Current objection:

{objection}

You have also been provided with historical objection cases retrieved
from the Retrieval Agent.

Your job is to determine:

1. Complexity (1-10)

2. Urgency
Choose one:
- Y
- N

3. Primary Bucket

Choose the most appropriate business category.

4. Recommendation

Choose ONE recommendation from:

- Auto approve
- Refer to Valuer
- Refer to Senior Valuer
- Request more information
- Site inspection required
- Legal review required
- Reject objection

Your decision must be supported by the retrieved historical objections.

Do NOT invent historical cases.

Do NOT ignore the retrieved precedents.

Explain your reasoning.
""",

        expected_output="""
Return your answer as JSON.

{
    "complexity": integer,
    "urgency": "Y or N",
    "primary_bucket": "...",
    "recommendation": "...",
    "reasoning": "...",
    "supporting_cases": [
        ...
    ]
}
""",

        agent=agent,

        context=[retrieval_task]
    )