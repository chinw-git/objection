from crewai import Task

def create_legislation_task(legislation_agent):
    return Task(

            description="""
            Analyse the following property tax objection.

            Objection:
            {objection}

            Instructions:
            Use the retrieval tool to obtain the relevant Property Tax Act
            sections. When using the "Retrieve Property Tax Act" tool:

            - Pass ONLY the objection text as the value of the `query` argument.
            - The `query` argument must be a plain string.
            - Do NOT pass a JSON object or dictionary.

            Return the following information:

            1. Relevant section numbers.
            2. Relevant legislation.
            3. Explanation of why each section applies.

            Do not determine complexity.
            """,

            expected_output="""
            Return ONLY valid JSON.

            {
            "relevant_pta_sections":[
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