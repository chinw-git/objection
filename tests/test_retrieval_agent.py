from crewai import Task
from agents.retrieval_agent import create_retrieval_agent


def main():

    agent = create_retrieval_agent()

    task = Task(
        description="""
Retrieve similar historical objections for:

"The tenant claims that comparable rental evidence is outdated."

Return only the retrieved cases.
""",
        expected_output="Retrieved historical cases.",
        agent=agent,
    )

    result = task.execute_sync()

    print("\nResult")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()