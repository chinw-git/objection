from crewai import Task


def create_assessment_task(agent, retrieval_task):

    return Task(

        description="""
You are a senior valuation officer assessing a new property objection.

You have been given:

1. The current objection.
2. Historical objection cases retrieved from the Retrieval Agent.

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
- Use the retrieved cases as supporting evidence.
- Do not invent historical precedents.
- Do not predict complexity.
- Do not predict urgency.
- Do not recommend any actions.
- If multiple buckets appear relevant, choose the single best bucket.
- Explain why you selected that bucket.
""",

        expected_output="""
Return your answer as JSON.

{
    "primary_bucket": "<one valid bucket>",
    "reasoning": "<why this bucket was selected>",
    "supporting_case_ids": [
        "<case_ids>"
    ]
}
""",

        agent=agent,

        context=[retrieval_task]

    )