from crewai import Agent

from tools.objection_rag_tool import ObjectionRAGTool


def create_retrieval_agent():

    return Agent(
        role="Property Objection Retrieval Specialist",

        goal="Retrieve historical objections similar to the current objection.",

        backstory="""
        You are an experienced property valuation officer.
        Your responsibility is ONLY to retrieve relevant historical
        objection cases using the retrieval tool.
        You must not analyse the objection or make recommendations.
        """,

        tools=[ObjectionRAGTool()],

        verbose=True
    )