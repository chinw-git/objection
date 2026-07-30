## METHODOLOGY ##

import streamlit as st

def render_methodology():
    st.set_page_config(page_title="Methodology")

    st.title("📖 Methodology")

    st.markdown("""
    ## Workflow

    1. User submits an objection.
    2. Retrieve relevant Property Tax Act sections.
    3. Retrieve similar past objections.
    4. Load complexity rubric.
    5. AI analyses all retrieved information.
    6. Return:
        - Complexity
        - Supporting legislation
        - Similar cases
        - Explanation
    """)