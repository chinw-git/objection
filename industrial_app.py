"""
industrial_app.py

Streamlit UI for the PTA objection classification pipeline.
"""

import streamlit as st
from industrial_pipeline import run_pipeline

st.title("PTA Objection Classifier")

explanatory_note = st.text_area("Explanatory Note")
file_upload_count = st.number_input("File Upload Count", min_value=0, value=0)
dev = st.selectbox("DEV", ["Non-strata", "Strata"])

if st.button("Classify"):
    with st.spinner("Running classification pipeline..."):
        result = run_pipeline(explanatory_note, file_upload_count, dev)

    st.subheader(f"Category: {result['category']}")
    st.write(result['reason'])

    st.subheader("Precedent Cases")
    for case in result['precedent']['similar_cases']:
        with st.expander(f"Case (distance={case['distance']}, category={case['category']})"):
            st.write(case['explanatory_note'])
            st.caption(case['reason'])

    st.subheader("Next Steps")
    st.write(f"RFI needed: {result['next_steps']['rfi_needed']}")
    for step in result['next_steps']['next_steps']:
        st.write(f"- {step}")
    if result['next_steps']['escalation_needed']:
        st.warning(result['next_steps']['escalation_reason'])