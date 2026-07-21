from crewai import Task


def create_retrieval_task(agent):

    return Task(

        description="""
Retrieve historical objections similar to the following objection:

{objection}

Instructions:

- Use the Property Objection Retrieval Tool.
- Retrieve the most relevant historical objection cases.
- Return the retrieved cases exactly as provided.
- Do not analyse the objection.
- Do not infer the Primary Bucket.
- Do not infer complexity.
- Do not infer urgency.
- Do not recommend any actions.
""",

        expected_output="""
A JSON object containing the retrieved historical objection cases returned by the retrieval tool.
""",

        agent=agent

    )