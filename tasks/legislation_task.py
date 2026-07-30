from crewai import Task

from agents.legislation_agent import legislation_agent


legislation_task = Task(

    description="""
        Analyse the following property tax objection.

        Objection:
        {objection}

        Instructions:
        Use the retrieval tool to obtain the relevant Property Tax Act
        sections.

        Return the following information:

        1. Relevant section numbers.
        2. Relevant legislation.
        3. Explanation of why each section applies.

        Do not determine complexity.
        """,

        expected_output="""
        Return ONLY valid JSON.

        {
        "relevant_sections":[
            {
                "section":"",
                "content":"",
                "reason":""
            }
        ]
        }

        Do not include markdown.
        """,

    agent=legislation_agent,
)