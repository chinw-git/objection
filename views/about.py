## ABOUT US ##

import streamlit as st

def render_about():
    st.set_page_config(page_title="About Us")

    st.title("ℹ️ About Us")

    st.markdown("""
    ## Property Tax Objection Assistant

    This application assists valuation officers by:

    - Analysing property tax objections
    - Retrieving relevant Property Tax Act sections
    - Retrieving similar historical objection cases
    - Assessing objection complexity
    - Providing supporting rationale

    ### Project Team

    - Member A
    - Member B
    - Member C
    - Member D
    """)