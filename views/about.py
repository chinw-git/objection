## ABOUT US ##

import streamlit as st

def render_about():
    # st.set_page_config(page_title="About Us", page_icon="ℹ️")

    st.title("🏘️ About the Project")

    st.markdown("""
    ### Overview

    The **Property Tax Objection Assistant** is a proof-of-concept application developed to explore how Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) can assist officers in assessing property tax objection cases.

    The application analyses objection grounds, assesses case complexity using predefined assessment rubrics and relevant Property Tax Act provisions, and retrieves similar historical objection cases to support consistent and informed decision-making.

    Our aim is to make objection assessments more efficient and consistent, so officers can focus their time and expertise on cases that need closer attention.

    ---

    ### Objectives

    This prototype is designed to:

    * Serve as a decision-support tool to assist officers in assessing property tax objection cases.
    * Assess case complexity based on established assessment rubrics.
    * Identify relevant Property Tax Act provisions to support each assessment.
    * Retrieve similar historical objection cases as useful references for officers.
    * Improve consistency by providing a structured approach to case assessment.
    * Streamline initial case assessment by bringing relevant information together in one place.

    ---
    
    #### Disclaimer

    This application is developed solely as a **proof-of-concept prototype** and is **not intended for operational use**. The outputs generated should not be relied upon for legal, financial, or official decision-making and should always be reviewed by qualified officers.

    _This application demonstrates the workflow for a single property type as part of a split-team prototype developed in conjunction with Objection Classifier and Recommender (Team 2). 
    Both submissions share a common problem statement and application framework, with each team independently developing its methodology and assessment criteria for its respective property type._

    ---

    **Members:** New Chin Wen, Wesley Teo

    """)