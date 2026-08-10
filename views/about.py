## ABOUT US ##

import streamlit as st

def render_about():
    # st.set_page_config(page_title="About Us", page_icon="ℹ️")

    st.title("🏘️ About the Project")

    st.markdown("""
    ### Overview

    The **Property Tax Objection Assistant** is a proof-of-concept decision support application developed to explore how Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) can assist officers in assessing property tax objection cases.

    The application analyses objection grounds, assesses case complexity using predefined assessment rubrics and relevant Property Tax Act provisions, and retrieves similar historical objection cases to support consistent and informed decision-making.

    Its objective is to reduce manual effort, improve assessment consistency, and enable officers to focus on cases that require greater professional judgement.

    ---

    ### Objectives

    This prototype is designed to:

    * Assess the complexity of property tax objection cases based on established assessment rubrics.
    * Identify relevant Property Tax Act provisions supporting each assessment.
    * Retrieve similar historical objection cases for reference.
    * Provide officers with structured information to support efficient and consistent case assessments.

    ---

    #### Disclaimer

    This application is developed solely as a **proof-of-concept prototype** and is **not intended for operational use**. The outputs generated should not be relied upon for legal, financial, or official decision-making and should always be reviewed by qualified officers.

    _Prototype is developed in conjunction with Team 2 - our solution shares a common application framework with each team developing a tailored methodology for our respective property types._

    ---

    **Members:** New Chin Wen, Wesley Teo

    """)