## METHODOLOGY ##

import streamlit as st

def render_methodology():
    st.set_page_config(page_title="Methodology", page_icon="🧩")

    st.title("Our Methodology")

    st.markdown("""
    This application adopts a **Retrieval-Augmented Generation (RAG)** approach coupled with a **multi-agent workflow**
    to assist valuation officers in assessing property tax objections.

    The assistant leverages a Large Language Model (LLM) to analyse property tax objections, while grounding its reasoning using the _Property Tax Act_ and a 
    _predefined complexity assessment rubric_. Similar historical objection cases are retrieved and presented as reference material for users.
    """)

    st.divider()

    # Overall Workflow
    st.subheader("Overall Workflow 🔄")

    st.markdown("""
    ```text
                    User submits objection
                            │
                            ▼
                    [legislation agent]
        Retrieve relevant Property Tax Act (PTA) sections
                            │
                            ▼
                    [classifier agent]
                Processes predefined criteria 
                            + 
         relevant PTA sections to determine complexity
                            │
                            ▼
                    [recommender agent]
      Recommend next steps based on complexity assessment
                            │
                            ├──────────────────────────────┐
                            ▼                              │
            Retrieve similar historical cases              │
                            │                              │
                            │                              │
                            └───────────────┬──────────────┘
                                            ▼
                            Assessment results presented to users
    """)