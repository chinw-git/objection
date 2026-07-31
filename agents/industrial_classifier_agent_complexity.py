"""
agents/industrial_classifier_agent_complexity.py

Classifies property tax objection cases against the PTA rubric,
then fetches matched precedent from past cases for supporting context.
"""

import json
from dotenv import load_dotenv
from openai import OpenAI

from agents.industrial_rfi_recommender_agent import recommend_next_steps
from agents.pta_research_agent import research_case
from agents.industrial_similar_case_recommender_agent import recommend_from_precedent

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT_TEMPLATE = """You are assessing taxpayer cases against the following Property Tax Act (PTA) rubric:
{RUBRIC}

Inputs:
- ExplanatoryNote
- FileUploadCount
- DEV

Classify into exactly ONE category.

1. Easy - Disallow
- No legal ground under the Act; claim cannot be cured by RFI.
- Indicators: no section 20(2) valuation ground stated; purely subjective/vague assertions (e.g. "AV is too high") without rent/sale/cost/receipts evidence; reliance on excluded/irrelevant factors; purely procedural/formal complaints with no substantive valuation content; time-barred or out-of-jurisdiction claims; non-compliant objection/appeal with no substantive content.
- Do NOT disallow simply because supporting evidence has not yet been provided if a valid section 20(2) valuation ground is stated.
- IMPORTANT: A statement that a unit is let out at a lower/different rent, or any assertion of actual rent received, IS a valid section 20(2)(a)(i) ground — even without a lease or receipt attached. This belongs in "Easy - RFI (minimal)" (request the lease/rent document), NOT Disallow. Reserve Disallow only for cases with no factual claim at all (e.g. "AV is too high" alone, with no rent, sale, cost, or other section 20(2) basis mentioned whatsoever).

2. Easy - RFI (minimal)
- Layman grounds; a single document or simple clarification suffices.
- Typical examples:
    • simple rent-based claims (actual rent, simple rent drop or discrepancy)
    • simple omission or mis-entry (wrong inclusion/omission of unit/area)
    • straightforward physical change (renovation, demolition/rebuild, cessation of use)
    • simple change of class/use (residential ↔ commercial, owner-occupation)
    • clerical/arithmetic error within time limits
- RFI burden is very low: one (at most two) standard documents; no iterative queries or expert input.

3. Medium - RFI (extensive)
Use only where assessment itself is technically complex and likely requires substantial officer effort, multiple documents or iterative clarification.
Typical indicators:
- complex rent or market comparables (multiple lettings, trends, partial schedules)
- transaction-price claims with incomplete information
- development cost-based claims requiring detailed cost schedules
- gross receipts/takings with partial data
- intermediate structural/valuation complexity (machinery, phased demolition/redevelopment)
- procedural/valuation errors mixing fact and law
Do NOT classify as Medium solely because:
- files were uploaded;
- the note is long;
- professional language is used;
- a tax agent or valuer is mentioned.

4. Difficult
Fully technical grounds; significant valuation judgement; extensive evidence and legal/valuation analysis.
Typical indicators:
- full valuation-method challenges (DCF, cap-rate, yield studies, professional valuation reports)
- major portfolio or multi-property claims
- complex gross-receipts cases involving advanced accounting/tax arguments
- detailed machinery/plant classification disputes
- appeals alleging explicit errors of law or mixed fact-law
- remission for poverty/"just and equitable" grounds
Do NOT classify as Difficult merely because many files were uploaded or the submission is lengthy.

Decision order:
1. No valid section 20(2) valuation ground, or time-barred/procedural-only? → Easy - Disallow
2. Straightforward factual verification with a single ground? → Easy - RFI (minimal)
3. Technical assessment requiring substantial analysis or multiple documents? → Medium - RFI (extensive)
4. Specialist valuation/legal/accounting complexity? → Difficult

Respond ONLY with valid JSON:
{{
  "category": "Easy - Disallow" | "Easy - RFI (minimal)" | "Medium - RFI (extensive)" | "Difficult",
  "reason": "One or two sentences explaining the decision."
}}
"""


def build_compiled_context(research: dict) -> str:
    return f"""Relevant rubric section:
{research['rubric_section']}

Relevant PTA provisions:
{research['pta_raw_text']}

Legal analysis:
{research['pta_explanation']}"""


def classify_case(explanatory_note: str, file_upload_count: int, dev: str) -> dict:
    from agents.industrial_rfi_recommender_agent import recommend_next_steps
    research = research_case(case_text=explanatory_note, dev=dev)
    compiled_context = build_compiled_context(research)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.replace("{RUBRIC}", compiled_context)

    user_message = f"""ExplanatoryNote: {explanatory_note}

FileUploadCount: {file_upload_count}
DEV: {dev}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)

    # Fetch matched precedent using the freshly assigned category
    precedent = recommend_from_precedent(
        grounds_of_objection=explanatory_note,
        assigned_category=result["category"],
    )
    result["precedent"] = precedent

    next_steps = recommend_next_steps(
        explanatory_note=explanatory_note,
        assigned_category=result["category"],
        dev=dev,
    )
    result["next_steps"] = next_steps

    result["_debug"] = {
        "rubric_section": research["rubric_section"],
        "pta_search_query": research["pta_search_query"],
        "pta_raw_text": research["pta_raw_text"],
        "pta_explanation": research["pta_explanation"],
    }

    return result


if __name__ == "__main__":
    result = classify_case(
        explanatory_note="AV is too high compared to neighbouring units, no other reason given.",
        file_upload_count=0,
        dev="Non-strata",
    )
    print(f"Category: {result['category']}")
    print(f"Reason: {result['reason']}")

    print(f"\n--- Precedent cases used ({len(result['precedent']['similar_cases'])} matched) ---")
    for i, case in enumerate(result['precedent']['similar_cases']):
        print(f"\n[{i+1}] (distance={case['distance']}, category={case['category']})")
        print(f"    Grounds: {case['explanatory_note']}")
        print(f"    Reason on file: {case['reason']}")

    print(f"\n--- Precedent synthesis ---\n{result['precedent']['recommendation']}")

    print(f"\n--- Next steps ---")
    print(f"RFI needed: {result['next_steps']['rfi_needed']}")
    for step in result['next_steps']['next_steps']:
        print(f"  - {step}")
    if result['next_steps']['escalation_needed']:
        print(f"Escalation: {result['next_steps']['escalation_reason']}")