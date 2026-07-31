"""
agents/industrial_similar_case_recommender_agent.py

Given a new case's grounds of objection and its freshly assigned category,
retrieves matched precedent cases and produces a supporting recommendation.
"""

from dotenv import load_dotenv
from openai import OpenAI

from retrievers.industrial_pastcases_reviewer import retrieve_similar_cases

load_dotenv()
client = OpenAI()

RECOMMENDER_SYSTEM_PROMPT = """You are reviewing precedent cases that were classified under the same
category as a new case. Confirm whether the precedent supports this classification, and note anything
unusual if the new case differs meaningfully from these examples despite sharing a category."""


def recommend_from_precedent(grounds_of_objection: str, assigned_category: str, top_k: int = 5) -> dict:
    similar_cases = retrieve_similar_cases(
        grounds_of_objection,
        category_filter=assigned_category,
        top_k=top_k,
    )

    if not similar_cases:
        return {
            "similar_cases": [],
            "recommendation": f"No precedent found for category '{assigned_category}' matching this case's semantics.",
        }

    cases_summary = "\n\n".join(
        f"Case {i+1} (distance={c['distance']}):\n"
        f"  Note: {c['explanatory_note']}\n"
        f"  Reason: {c['reason']}"
        for i, c in enumerate(similar_cases)
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": RECOMMENDER_SYSTEM_PROMPT},
            {"role": "user", "content": f"New case:\n{grounds_of_objection}\n\nAssigned category: {assigned_category}\n\nPrecedent cases in this same category:\n{cases_summary}"},
        ],
        temperature=0,
    )

    return {
        "similar_cases": similar_cases,
        "recommendation": response.choices[0].message.content.strip(),
    }


if __name__ == "__main__":
    result = recommend_from_precedent(
        grounds_of_objection="AV is too high compared to neighbouring units, no other reason given.",
        assigned_category="Easy - Disallow",
    )
    print("\n--- Similar cases ---")
    for c in result["similar_cases"]:
        print(f"[{c['category']}] (dist={c['distance']}) {c['explanatory_note'][:80]}...")
    print(f"\n--- Recommendation ---\n{result['recommendation']}")