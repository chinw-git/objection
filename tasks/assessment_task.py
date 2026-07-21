from crewai import Task


def create_assessment_task(agent, retrieval_task):

    return Task(

        description="""
You are a senior valuation officer assessing a new property objection.

You have been provided with:

1. The current objection.
2. Historical objection cases retrieved by the Retrieval Agent.

Current Objection

-------------------------

{objection}

-------------------------

Your objective is to determine the SINGLE most appropriate
Primary Bucket for this objection.

You MUST choose ONE AND ONLY ONE of the following buckets:

- Multi-Unit Lease / Apportionment
- Comparable Evidence / PSF Benchmark
- Actual / Net Rental Basis
- Vacancy / Leasing Difficulty
- Weak Market / Poor Location Conditions
- Use Issues
- Insufficient Text / Attachment-Dependent
- Hardship / Compassion Appeal
- Physical / Locational Disamenity
- Invalid Objection
- Owner Occupy

Instructions

- Carefully compare the objection with the retrieved historical cases.
- Base your decision ONLY on the information provided.
- Do not invent historical precedents.
- Do not predict complexity.
- Do not predict urgency.
- Do not recommend any actions.
- If multiple buckets appear relevant, choose the single best bucket.
- Clearly explain your reasoning.
- Include EVERY retrieved historical case in your output so that reviewers can understand what evidence was available during your assessment.
""",

        expected_output="""
Return your answer as JSON.

{
    "primary_bucket": "<one valid bucket>",

    "reasoning": "<clear explanation of why this bucket was selected>",

    "supporting_cases": [
        {
            "grounds_of_objection": "<retrieved grounds of objection>",
            "primary_bucket": "<retrieved case primary bucket>",
            "complexity": "<retrieved complexity if available>",
            "urgency": "<retrieved urgency if available>"
        }
    ]
}
""",

        agent=agent,

        context=[retrieval_task]

    )