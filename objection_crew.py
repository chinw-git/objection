from crewai import Crew, Process
from langchain_openai import ChatOpenAI

from agents.legislation_agent import create_legislation_agent
from agents.classifier_agent import create_classifier_agent
from agents.recommender_agent import create_recommender_agent

from tasks.legislation_task import create_legislation_task
from tasks.classifier_task import create_classifier_task
from tasks.recommender_task import create_recommender_task

# ------------------------------------
# Create the objection assessment crew
# ------------------------------------

def create_obj_assessment_crew(model, temperature):
    #create llm model
    llm = ChatOpenAI(model=model, temperature=temperature)

    #create agents
    legislation_agent = create_legislation_agent(llm)
    classifier_agent = create_classifier_agent(llm)
    recommender_agent = create_recommender_agent(llm)

    #create tasks
    legislation_task = create_legislation_task(legislation_agent)
    classifier_task = create_classifier_task(classifier_agent, legislation_task)
    recommender_task = create_recommender_task(recommender_agent, classifier_task)

    objection_crew = Crew(
        agents=[
            legislation_agent,
            classifier_agent,
            recommender_agent,
        ],

        tasks=[
            legislation_task,
            classifier_task,
            recommender_task,
        ],

        process=Process.sequential,

        verbose=True,
    )

    return objection_crew