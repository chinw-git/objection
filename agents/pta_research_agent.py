from dotenv import load_dotenv
from openai import OpenAI
from utils.industrial_context_loader import get_rubric_context
from retrievers.pta_retriever import retrieve_pta_sections

load_dotenv()
client = OpenAI()

EXTRACTION_SYSTEM_PROMPT = """You are a legal research assistant for property tax objections.
Given a rubric section and the taxpayer's case details, identify the specific legal
grounds or provisions being invoked. Output a concise search query (not a full sentence)
suitable for retrieving relevant sections of the Property Tax Act."""

EXPLANATION_SYSTEM_PROMPT = """You are explaining Property Tax Act provisions to support
a case classification decision. Given the raw Act text and the taxpayer's case, explain
in 2-4 sentences how the provision applies (or doesn't) to this specific case. Be precise,
do not speculate beyond what the text supports."""


def research_case(case_text: str, dev: str) -> dict:
    # Hop 1: find the relevant rubric section
    rubric_query = f"{case_text} {dev}"
    rubric_section = get_rubric_context(query=rubric_query)

    # Derive a PTA-specific search query from the rubric section + case
    query_derivation = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Rubric section:\n{rubric_section}\n\nCase:\n{case_text}"},
        ],
        temperature=0,
    )
    pta_search_query = query_derivation.choices[0].message.content.strip()

    # Hop 2: retrieve relevant PTA sections using the derived query
    pta_sections = retrieve_pta_sections(query=pta_search_query, k=3)

    # Explain how the PTA text applies to this case
    explanation = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EXPLANATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"PTA text:\n{pta_sections}\n\nCase:\n{case_text}"},
        ],
        temperature=0,
    )
    pta_explanation = explanation.choices[0].message.content.strip()

    return {
        "rubric_section": rubric_section,
        "pta_search_query": pta_search_query,
        "pta_raw_text": pta_sections,
        "pta_explanation": pta_explanation,
    }