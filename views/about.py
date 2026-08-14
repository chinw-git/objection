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

    ### Data Sources

    **<u>Property Tax Act (PTA)</u>** <br>
    The full text of the Property Tax Act is sourced from the official [Singapore Statutes Online](https://sso.agc.gov.sg//Act/PTA1960) in PDF format and serves as the legislative knowledge base for the application.

    **<u>Past Objection Cases</u>** <br>
    A set of 53 synthetic objection cases was created for the purpose of this prototype.
    
    ---

    ### Key Features
    
    1. **Flexible Input Modes** - users can toggle between _Single Objection_ and _Batch Upload_ mode.
        * _Single Objection_ allows users to input their objection text in a chat-like interface.
        * _Batch Upload_ allows users to upload multiple objection texts via a CSV or Excel file. <br>
        
    2. **Structured Assessment Results**<br> 
        Each objection is assessed and presented as a structured output comprising the complexity classification, relevant PTA provisions, recommended next steps, and similar past cases.
        In batch mode, a high-level summary of complexity level distribution is displayed instead, with full details available via export.
        
    3. **Assessment Export**<br> 
        Assessment results can be downloaded via the 'Export Assessment' button at the sidebar, covering all objections assessed in the current session.

    4. **Model Settings**<br>
        GPT model and temperature can be adjusted via the sidebar to customise the assistant's behaviour.

    ---

    #### Disclaimer

    This application is developed solely as a **proof-of-concept prototype** and is **not intended for operational use**. The outputs generated should not be relied upon for legal, financial, or official decision-making and should always be reviewed by qualified officers.

    _This application demonstrates the workflow for a single property type as part of a split-team prototype developed in conjunction with Objection Classifier and Recommender (Team 2). 
    Both submissions share a common problem statement and application framework, with each team independently developing its methodology and assessment criteria for its respective property type._

    ---

    **Members:** New Chin Wen, Wesley Teo

    """, unsafe_allow_html=True)