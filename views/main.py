import traceback
import streamlit as st
import json

from objection_crew import create_obj_assessment_crew
from tools.retrieve_past_obj import retrieve_similar_cases
from utils.export_assessment import create_assessment_output


def render_main():
    st.title("🏢 Property Tax Objection Assistant")

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

    if "assessment_history" not in st.session_state:
        st.session_state.assessment_history = []

    # -----------------------------
    # Sidebar
    # -----------------------------
    with st.sidebar:
        st.divider()

        st.markdown("""
        <div style="
            text-align: center;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 14px;
        ">
            ⚙️ Settings
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### AI Model")

        selected_model = st.selectbox(
            "",
            ["gpt-4o-mini", "gpt-4o"],
            label_visibility="collapsed"
        )

        st.markdown("### Temperature")

        selected_temperature = st.slider(
            "",
            0.0,
            2.0,
            0.2,
            0.1,
            label_visibility="collapsed",
            help="Lower values produce more deterministic responses. Higher values produce more varied responses."
        )

        # -----------------------------
        # Export Assessment Output
        # -----------------------------
        excel_bytes = create_assessment_output(
            st.session_state.assessment_history
        )

        left, centre, right = st.columns([0.1, 0.8, 0.1])

        with centre:
            st.download_button(
                label="📥 Export Assessment",
                data=excel_bytes,
                file_name="assessment_history.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            if st.button(
                "🗑️ Clear Conversation",
                use_container_width=True
            ):
                st.session_state.messages = [{
                        "role": "assistant",
                        "content": "Please provide your property objection case for analysis."
                }]

                st.session_state.assessment_history = []

                st.rerun()

        # st.header("⚙️ Settings")

        # with st.expander("📝 System Prompt", expanded=False):
        #     system_prompt = st.text_area(
        #         "System Prompt",
        #         value=ANALYSIS_SYSTEM_PROMPT,
        #         height=150
        #     )

        # selected_model = st.selectbox(
        #     "Model",
        #     [
        #         "gpt-4o-mini",
        #         "gpt-4o"
        #     ],
        #     index=0
        # )

        # # Temperature
        # temperature = st.slider(
        #     "Temperature",
        #     min_value=0.0,
        #     max_value=2.0,
        #     value=0.2,
        #     step=0.1,
        #     help="Lower values produce more deterministic responses. Higher values produce more varied responses."
        # )

        # # Conversation Statistics
        # character_count = sum(
        #     len(message["content"])
        #     for message in st.session_state.messages[1:]
        # )

        # estimated_tokens = character_count // 4

        # st.divider()

        # st.markdown(
        #     "<h5 style='margin-bottom:0.3rem;'>📊 Conversation</h5>",
        #     unsafe_allow_html=True
        # )

        # st.markdown(
        #     f"""
        #     <div style="font-size:13px; color:gray;">
        #         <strong>Characters:</strong> {character_count:,}<br>
        #         <strong>Estimated Tokens:</strong> {estimated_tokens:,}
        #     </div>
        #     """,
        #     unsafe_allow_html=True,
        # )

        # st.divider()

        # # -----------------------------
        # # Export Conversation
        # # -----------------------------
        # conversation_text = ""

        # for message in st.session_state.messages:

        #     role = message["role"].upper()

        #     conversation_text += (
        #         f"========== {role} ==========\n"
        #         f"{message['content']}\n\n"
        #     )

        # st.download_button(
        #     label="📥 Download Chat",
        #     data=conversation_text,
        #     file_name="property_objection_chat.txt",
        #     mime="text/plain"
        # )

        # if st.button("🗑️ Clear Conversation"):
        #     st.session_state.messages = [
        #         {
        #             "role": "assistant",
        #             "content": "Please provide your property objection case for analysis."
        #         }
        #     ]

        #     st.rerun()

    # -----------------------------
    # Display Previous Messages
    # -----------------------------
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            # Assistant analysis
            # ===== CHANGED START =====
            if (message["role"] == "assistant"and "classification" in message):

                classification = message["classification"]
                recommendation = message["recommendation"]
            # ===== CHANGED END =====

                # -----------------------------
                # 1. Complexity Assessment
                # -----------------------------
                st.markdown("""
                <div style="
                    background-color:#E3F2FD;
                    padding:10px 15px;
                    border-radius:8px;
                    margin-top:10px;
                    margin-bottom:15px;
                ">
                <h3 style="margin:0; color:#0D47A1;">
                    📋 Complexity Assessment
                </h3>
                </div>
                """, unsafe_allow_html=True)

                # complexity category
                # st.markdown(f"#### {classification['complexity']}")
                complexity = classification["complexity"]

                if "easy" in complexity.lower():
                    bg = "#E8F5E9"
                    fg = "#2E7D32"
                elif "medium" in complexity.lower():
                    bg = "#FFF8E1"
                    fg = "#F9A825"
                else:
                    bg = "#FFEBEE"
                    fg = "#C62828"

                st.markdown(
                    f"""
                    <div style="
                        display:inline-block;
                        background:{bg};
                        color:{fg};
                        padding:10px 20px;
                        margin-bottom:20px;
                        border-radius:999px;
                        font-size:20px;
                        font-weight:600;
                    ">
                        {complexity}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # reasoning for complexity
                st.markdown("##### Reasoning")
                st.write(classification["reasoning"].replace("$", r"\$")) #prevent Streamlit from interpreting $ as a LaTeX delimiter

                # triggered rubric criteria
                st.markdown("##### Triggered Rubric Criteria")

                for criterion in classification["rubric_criteria"]:
                    st.markdown(f"- {criterion}")

                #relevant Property Tax Act sections
                st.markdown("##### Relevant Property Tax Act Sections")

                for section in classification["relevant_pta_sections"]:

                    with st.expander("Section " + section["section"]):

                        st.markdown("**Legislation**")
                        st.info(section["content"])

                        st.markdown("**Why it applies**")
                        st.write(section["reason"])

                # -----------------------------
                # 2. Recommendation (next steps)
                # -----------------------------

                # ===== CHANGED START =====
                st.divider()

                st.markdown("""
                <div style="
                    background-color:#E3F2FD;
                    padding:10px 15px;
                    border-radius:8px;
                    margin-top:10px;
                    margin-bottom:15px;
                ">
                <h3 style="margin:0; color:#0D47A1;">
                    📝 Recommendation
                </h3>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("##### Recommended Next Steps")
                #RFI indicator
                if recommendation["rfi_needed"]:
                    st.info("📄 Request for Information (RFI) Required")
                else:
                    st.success("No Request for Information Required")

                #next steps
                for step in recommendation["next_steps"]:
                    st.markdown(f"- {step}")

                st.markdown("##### Escalation")
                #escalation info
                if recommendation["escalation_needed"]:
                    st.warning(recommendation["escalation_reason"])
                else:
                    st.success("No escalation required.")
                # ===== CHANGED END =====

                # -----------------------------
                # 3. Similar Past Cases
                # -----------------------------
                if "similar_cases" in message:

                    st.divider()

                    st.markdown("""
                    <div style="
                        background-color:#E3F2FD;
                        padding:10px 15px;
                        border-radius:8px;
                        margin-top:10px;
                        margin-bottom:15px;
                    ">
                    <h3 style="margin:0; color:#0D47A1;">
                        📂 Similar Past Cases
                    </h3>
                    </div>
                    """, unsafe_allow_html=True)

                    for i, case in enumerate(message["similar_cases"], start=1):
                        with st.expander(f"Past Case {i}"):

                            content = case["grounds_of_objection"].replace("$", r"\$") #prevent Streamlit from interpreting $ as a LaTeX delimiter

                            st.markdown("**Property Type**")
                            st.write(case["property_type"])

                            st.markdown("**Development**")
                            st.write(case["development"])

                            st.markdown("**Strata Classification**")
                            st.write(case["strata_classification"])

                            st.markdown(content) #objection text

                            st.markdown("**No. of Uploaded Files**")
                            st.write(case["file_upload_count"])

                            st.markdown(f"""
                            **Complexity Category**  
                            {case["complexity"]}
                            """)

                            st.markdown("**Reasoning**")
                            st.write(case["reasoning"])

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
                    crew = create_obj_assessment_crew(selected_model, selected_temperature) #use selected model & temperature from the sidebar settings

                    result = crew.kickoff(
                        inputs={
                            "objection": prompt
                        }
                    )

                    # ===== CHANGED START =====
                    result_json = json.loads(result.raw)

                    classification = result_json["classification"]
                    recommendation = result_json["recommendation"]
                    # ===== CHANGED END =====

                    # -----------------------------
                    # Retrieve similar past cases
                    # -----------------------------
                    similar_cases = retrieve_similar_cases(prompt)

                # ===== CHANGED START =====
                st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Complexity assessment completed.",
                        "classification": classification,
                        "recommendation": recommendation,
                        "similar_cases": similar_cases,
                })
                # ===== CHANGED END =====

                # Save assessment outputs for possible export
                st.session_state.assessment_history.append({
                    "grounds_of_objection": prompt,
                    "classification": classification,
                    "recommendation": recommendation,
                    "similar_cases": similar_cases,
                })

                st.rerun()

            except Exception as e:
                traceback.print_exc()
                st.error("Unable to analyse the objection.")
                print(e)