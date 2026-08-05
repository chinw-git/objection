from crewai import Agent

#get PTA retrieval tool
from tools.retrieve_PTA import retrieve_legislation

#--------------------------------
# creates an agent that identifies the most relevant sections of the Property Tax Act
# that apply to the user's objection
#--------------------------------
def create_legislation_agent(llm):
    
    return Agent(
            role="Property Tax Legislation Expert",

            goal="""
            Identify the most relevant sections of the Property Tax Act
            that apply to the user's objection.
            """,

            backstory="""
            You are an experienced property tax officer with expert
            knowledge of the Property Tax Act.

            Your responsibility is ONLY to identify and explain the
            relevant legislation.

            Do NOT determine the objection complexity.

            Do NOT make recommendations.
            """,

            tools=[retrieve_legislation],

            llm=llm,
            verbose=True,
        )
