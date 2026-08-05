from crewai import Agent

#--------------------------------
# creates an agent that recommends the next course of action(s) for a property objection
#--------------------------------
def create_recommender_agent(llm):
    
    return Agent(
            role="Property Tax Recommendation Specialist",

            goal="""
            Recommend the appropriate next course of action(s) for the valuation officer
            based on the determined complexity category.
            """,

            backstory="""
            You are an experienced property tax valuation officer.

            Your responsibility is NOT to determine complexity.

            Your responsibility is to recommend the next actions after complexity has
            already been determined.

            Your recommendations must be consistent with the Property Tax Act and the
            objection.
            """,

            llm=llm,
            verbose=True,
        )