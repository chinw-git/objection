from crewai import Agent

#-------------------------------
# creates an agent that classifies the complexity of a property objection
#-------------------------------
def create_classifier_agent(llm):
    
    return Agent(
            role="Property Tax Complexity Assessor",

            goal="""
            Determine the complexity of the objection
            using the official complexity rubric.
            """,

            backstory="""
            You are responsible for determining objection complexity.

            You MUST use ONLY

            - the user's objection
            - the retrieved Property Tax Act sections from the previous legislation task
            - the official complexity rubric

            Do NOT use past objection cases.

            Do NOT rely on outside knowledge.
            """,

            llm=llm,
            verbose=True,
        )