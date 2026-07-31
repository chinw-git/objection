"""
agents/industrial_rfi_recommender_agent.py

Given a classified case, recommends concrete next-step actions for the valuer —
specifically, what information/documents to request from the taxpayer (RFI),
or the appropriate action if no RFI is needed.
"""

import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

RFI_SYSTEM_PROMPT = """You are advising a property tax valuer on next steps for a case
that has already been classified. Based on the grounds of objection and the assigned
category, recommend SPECIFIC, ACTIONABLE next steps.

If the category is "Easy - Disallow": the next step is always to find comparables
and disallow. State this exactly: next_steps should include "Find comparables" and
"Disallow the objection". Briefly note what comparables to look for (e.g. similar units
in the same development/area) based on the grounds stated.

If the category involves RFI (minimal or extensive): list the SPECIFIC documents or
information to request from the taxpayer. Be concrete — name the actual document type
(e.g. "tenancy agreement showing contracted rent for the assessment period", not just
"more information"). Do not pad with generic advice like "review the case carefully."

If the category is "Medium - Strata Owners": note any strata-specific documentation
needed (e.g. MCST records, share value schedules) in addition to any substantive RFI.

If the category is "Difficult": recommend escalation to a senior valuer or specialist,
and name what kind of expertise is needed (e.g. engineering assessment, legal opinion
on PTA interpretation).

Respond ONLY with valid JSON:
{
  "rfi_needed": true | false,
  "next_steps": ["specific action 1", "specific action 2", ...],
  "escalation_needed": true | false,
  "escalation_reason": "reason if escalation_needed is true, else empty string"
}
"""


def recommend_next_steps(explanatory_note: str, assigned_category: str, dev: str = "") -> dict:
    """
    Given a case's grounds of objection and its assigned complexity category,
    returns concrete next-step recommendations for the valuer.
    """
    user_message = f"""Grounds of objection: {explanatory_note}
Assigned category: {assigned_category}
DEV: {dev}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": RFI_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    result = recommend_next_steps(
        explanatory_note="AV is too high compared to neighbouring units, no other reason given.",
        assigned_category="Easy - Disallow",
        dev="Non-strata",
    )
    print(f"RFI needed: {result['rfi_needed']}")
    print("Next steps:")
    for step in result["next_steps"]:
        print(f"  - {step}")
    if result["escalation_needed"]:
        print(f"Escalation: {result['escalation_reason']}")