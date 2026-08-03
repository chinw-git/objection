from crewai import Crew, Process

from agents.legislation_agent import legislation_agent
from agents.classifier_agent import classifier_agent
from agents.recommender_agent import recommender_agent

from tasks.legislation_task import legislation_task
from tasks.classifier_task import classifier_task
from tasks.recommender_task import recommender_task

# ------------------------------------
# Create the objection assessment crew
# ------------------------------------

def create_obj_assessment_crew():
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