from crews.objection_assessment_crew import (
    create_objection_assessment_crew
)


def main():

    crew = create_objection_assessment_crew()

    objection = """
$93,231 (Annual Base Rent) / 12 months x 11 months = $85,400
 
Based on 2 years signed lease and at least 2 months vacancy for each lease renewal for obtaining new tenants ie., 11 months of annualised based rent.
"""

    result = crew.kickoff(

        inputs={
            "objection": objection
        }

    )

    print("\n")
    print("=" * 80)
    print("FINAL RESULT")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    main()