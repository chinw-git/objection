from crewai import Crew

from agents.retrieval_agent import create_retrieval_agent
from agents.assessment_agent import create_assessment_agent

from tasks.retrieval_task import create_retrieval_task
from tasks.assessment_task import create_assessment_task


def create_objection_assessment_crew():

    retrieval_agent = create_retrieval_agent()

    assessment_agent = create_assessment_agent()

    retrieval_task = create_retrieval_task(
        retrieval_agent
    )

    assessment_task = create_assessment_task(
        assessment_agent,
        retrieval_task
    )

    return Crew(

        agents=[
            retrieval_agent,
            assessment_agent
        ],

        tasks=[
            retrieval_task,
            assessment_task
        ],

        verbose=True
    )