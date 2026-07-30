import traceback

import streamlit as st
import json

from objection_crew import create_obj_assessment_crew
from tools.retrieve_past_obj import retrieve_similar_cases

def render_main():
    # -----------------------------
    # Page Configuration
    # -----------------------------
    st.set_page_config(
        page_title="Property Tax Objection Assistant",
        page_icon="🏡",
        layout="wide"
    )

    st.title("🏡 Property Tax Objection Assistant")

    ## -----------------------------
    # DISCLAIMER
    ## -----------------------------
    with st.expander("⚠️ Disclaimer", expanded=True):
        st.warning("""
        **IMPORTANT NOTICE:** This web application is developed as a proof-of-concept prototype. The information provided here is **NOT** intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

        *Always consult with qualified professionals for accurate and personalised advice.*
        """)

    # -----------------------------
    # Document Upload
    # -----------------------------
    st.markdown("##### 📄 Knowledge Document")

    uploaded_file = st.file_uploader(
        label="",
        type=["pdf", "csv", "xlsx", "xls"],
        label_visibility="collapsed",
        help="Upload a PDF, CSV or Excel file to build a temporary RAG knowledge base."
    )

    if uploaded_file is not None:
        st.success(f"Loaded: {uploaded_file.name}")

    st.caption("Supported formats: PDF • CSV • Excel (.xlsx)")

    st.divider()

    # -----------------------------
    # Initialize Chat History
    # -----------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Please provide your property objection case for analysis."
            }
        ]

    # -----------------------------
    # Sidebar
    # -----------------------------
    with st.sidebar:

        st.header("⚙️ Settings")

        # with st.expander("📝 System Prompt", expanded=False):
        #     system_prompt = st.text_area(
        #         "System Prompt",
        #         value=ANALYSIS_SYSTEM_PROMPT,
        #         height=150
        #     )

        selected_model = st.selectbox(
            "Model",
            [
                "gpt-4o-mini",
                "gpt-4o"
            ],
            index=0
        )

        # Temperature
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.2,
            step=0.1,
            help="Lower values produce more deterministic responses. Higher values produce more varied responses."
        )

        # Conversation Statistics
        character_count = sum(
            len(message["content"])
            for message in st.session_state.messages[1:]
        )

        estimated_tokens = character_count // 4

        st.divider()

        st.markdown(
            "<h5 style='margin-bottom:0.3rem;'>📊 Conversation</h5>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="font-size:13px; color:gray;">
                <strong>Characters:</strong> {character_count:,}<br>
                <strong>Estimated Tokens:</strong> {estimated_tokens:,}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # -----------------------------
        # Export Conversation
        # -----------------------------
        conversation_text = ""

        for message in st.session_state.messages:

            role = message["role"].upper()

            conversation_text += (
                f"========== {role} ==========\n"
                f"{message['content']}\n\n"
            )

        st.download_button(
            label="📥 Download Chat",
            data=conversation_text,
            file_name="property_objection_chat.txt",
            mime="text/plain"
        )

        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Please provide your property objection case for analysis."
                }
            ]

            st.rerun()

    # -----------------------------
    # Display Previous Messages
    # -----------------------------
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            # Assistant analysis
            if message["role"] == "assistant" and "analysis" in message:

                analysis = message["analysis"]

                st.subheader("📋 Complexity Assessment")

                st.metric(
                    "Complexity",
                    analysis["complexity"]
                )

                st.markdown("### Triggered Rubric Criteria")

                for criterion in analysis["rubric_criteria"]:
                    st.markdown(f"- {criterion}")

                st.markdown("### Relevant Property Tax Act Sections")

                for section in analysis["relevant_pta_sections"]:

                    with st.expander("Section " + section["section"]):

                        st.write(section["reason"])

                st.markdown("### Reasoning")

                st.write(
                    analysis["reasoning"]
                )

                # -----------------------------
                # Similar Past Cases
                # -----------------------------
                if "similar_cases" in message:

                    st.divider()

                    st.subheader("📂 Similar Past Cases")

                    for case in message["similar_cases"]:
                        metadata = case.metadata
                        #title = metadata.get("DEV", "Past Case")

                        with st.expander("Past Cases"):
                            st.markdown(case.page_content)

            else:
                st.markdown(message["content"])

    # -----------------------------
    # Chat Input
    # -----------------------------
    if prompt := st.chat_input("Describe your property tax objection..."):

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Analysing objection..."):

                    # -----------------------------
                    # Run Crew
                    # -----------------------------
                    crew = create_obj_assessment_crew()

                    result = crew.kickoff(
                        inputs={
                            "objection": prompt
                        }
                    )

                    analysis = json.loads(result.raw)

                    # -----------------------------
                    # Retrieve similar past cases
                    # -----------------------------
                    similar_cases = retrieve_similar_cases(prompt)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": "Complexity assessment completed.",
                        "analysis": analysis,
                        "similar_cases": similar_cases,
                    }
                )

                st.rerun()

            except Exception as e:
                traceback.print_exc()
                st.error("Unable to analyse the objection.")
                print(e)