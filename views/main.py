import traceback
import streamlit as st
import pandas as pd

from utils.process_objection import process_objection
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

    ## -----------------------------
    # Input Mode Selection
    ## -----------------------------
    with st.container(border=True):

        st.markdown(
            """
            <style>
            [data-testid="stRadio"] > label p  {
                font-size: 20px;
                font-weight: 600;
                color: #39505C;
            }

            [data-testid="stTooltipContent"] {
                max-width: 450px !important;
                text-align: left !important;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

        input_mode = st.radio(
            "Input Mode",
            ["Single Objection 💬", "Batch Upload 📂"],
            horizontal=True,
            help = """
            **Single Objection** allows you to assess _one case at a time_.  
            **Batch Upload** allows you to assess _multiple cases_ from a CSV or Excel file.
            """,
        )

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

    if "batch_results" not in st.session_state:
        st.session_state.batch_results = []

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
            ⚙️ Settings ⚙️
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
            0.0, #min
            2.0, #max
            0.2, #default
            0.1, #step
            label_visibility="collapsed",
            help="Lower values produce more deterministic responses. Higher values produce more varied responses."
        )

        # -----------------------------
        # Export Assessment Output
        # -----------------------------
        excel_bytes = create_assessment_output(
            st.session_state.assessment_history
        )

        _, sidebar_centre, _ = st.columns([1, 8, 1])
        with sidebar_centre:
            st.download_button(
                label="📥 Export Assessment",
                data=excel_bytes,
                file_name="assessment_history.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type='primary'
            )

            if st.button(
                "🗑️ Clear Conversation",
                use_container_width=True,
                type='primary'
            ):
                st.session_state.messages = [{
                        "role": "assistant",
                        "content": "Please provide your property objection case for analysis."
                }]

                st.session_state.assessment_history = []
                st.session_state.batch_results = []

                st.rerun()


    if input_mode == "Single Objection 💬":
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
                        background-color:#DBEDF3;
                        padding:8px;
                        border-radius:8px;
                        margin-top:10px;
                        margin-bottom:25px;
                    ">
                    <h4 style="margin:0; color:#497488;">
                        📋 Complexity Assessment
                    </h4>
                    </div>
                    """, unsafe_allow_html=True)

                    # complexity category
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
                        background-color:#DBEDF3;
                        padding:8px;
                        border-radius:8px;
                        margin-top:10px;
                        margin-bottom:20px;
                    ">
                    <h4 style="margin:0; color:#497488;">
                        📝 Recommendation
                    </h4>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("##### Recommended Next Steps")
                    #RFI indicator
                    reco_left, reco_right = st.columns([4, 6])
                    with reco_left:
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
                        esca_left, esca_right = st.columns([4, 6])
                        with esca_left:
                            st.success("No escalation required.")
                    # ===== CHANGED END =====

                    # -----------------------------
                    # 3. Similar Past Cases
                    # -----------------------------
                    if "similar_cases" in message:

                        st.divider()

                        st.markdown("""
                        <div style="
                            background-color:#DBEDF3;
                            padding:8px;
                            border-radius:8px;
                            margin-top:10px;
                            margin-bottom:20px;
                        ">
                        <h4 style="margin:0; color:#497488;">
                            📂 Similar Past Cases
                        </h4>
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
                    "content": prompt.replace("$", r"\$")
                }
            )
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt.replace("$", r"\$"))

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Analysing objection..."):

                        # -----------------------------
                        # Process objection
                        # -----------------------------
                        assessment = process_objection(prompt, selected_model, selected_temperature) #use selected model & temperature from the sidebar settings

                    # Save assessment outputs for display
                    st.session_state.messages.append({
                            "role": "assistant",
                            "content": "Complexity assessment completed.",
                            "classification": assessment["classification"],
                            "recommendation": assessment["recommendation"],
                            "similar_cases": assessment["similar_cases"],
                    })

                    # Save assessment outputs for possible export
                    st.session_state.assessment_history.append(assessment)

                    st.rerun()

                except Exception as e:
                    traceback.print_exc()
                    st.error("Unable to analyse the objection.")
                    print(e)

    else:
        # -----------------------------
        # Upload bulk objections
        # -----------------------------
        st.markdown(
            """
            <style>
            .stFileUploader label p  {
                font-size: 18px;
                font-weight: 600;
                color: #39505C;
                margin-bottom: 10px;
            }

            [data-testid="stFileUploader"] {
                width: 100%;
                max-width: 400px;
            }
            
            [data-testid="stAlert"] {
                width: 100%;
                max-width: 450px;
            }
            </style>
            """, unsafe_allow_html=True
        )

        uploaded_file = st.file_uploader(
            label="Objection File Upload",
            type=["csv", "xlsx"],
            label_visibility="visible",
            help="Upload a CSV or Excel file containing property objections."
        )
        st.caption("Ensure file has required column: 'ExplanatoryNote'")

        if uploaded_file is None:
            #reset batch results when no file uploaded
            st.session_state.batch_results = []

        #if got file uploaded
        else:

            # Read uploaded file
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Validate required column
            if "ExplanatoryNote" not in df.columns:
                st.error("Invalid file. The file must contain an 'ExplanatoryNote' column.")

            else:
                st.success(f"{uploaded_file.name} uploaded successfully")

                st.caption(f"**{len(df)}** objections found.")

                # Only appears if validation passes
                _, process_center, _ = st.columns([4, 2, 4])
                with process_center:
                    process_clicked = st.button("🔍 Process Objections", use_container_width=True, type='primary')

                _, bulk_results_center, _ = st.columns([2, 6, 2])
                with bulk_results_center:
                    if process_clicked:
                        progress = st.progress(0)
                        status = st.empty()

                        results = []
                        #process each objection
                        for i, row in df.iterrows():
                            objection = str(row["ExplanatoryNote"]).strip()

                            if not objection:
                                continue

                            with st.spinner(f"Processing objection {i + 1} of {len(df)}..."):

                                try:
                                    assessment = process_objection(
                                        objection=objection,
                                        model=selected_model,
                                        temperature=selected_temperature,
                                    )

                                    results.append(assessment)
                                    
                                    progress.progress((i + 1) / len(df), text=f"{(i + 1)} of {len(df)} done")

                                    # Save assessment outputs for possible export
                                    st.session_state.assessment_history.append(assessment)

                                except Exception as e:
                                    traceback.print_exc()
                                    st.error(f"Unable to analyse objection {i + 1}.")
                                    print(e)

                        status.success(f"Completed {len(results)} objections.")

                        # Save results so they survive reruns
                        st.session_state.batch_results = results

                    # -----------------------------
                    # Display Bulk Assessment Summary
                    # -----------------------------
                    if st.session_state.batch_results:
                        st.markdown("""
                        <div style="
                            background-color:#DBEDF3;
                            padding:8px;
                            border-radius:8px;
                            margin-top:20px;
                            margin-bottom:25px;
                        ">
                        <h4 style="margin:0; color:#497488; text-align:center">
                            Assessment Summary
                        </h4>
                        </div>
                        """, unsafe_allow_html=True)

                        easy_disallow, easy_rfi, medium_rfi, difficult =  0, 0, 0, 0

                        for assessment in st.session_state.batch_results:

                            complexity = assessment["classification"]["complexity"]

                            if "easy – disallow" in complexity.lower():
                                easy_disallow += 1
                            elif "easy – rfi" in complexity.lower():
                                easy_rfi += 1
                            elif "medium – rfi" in complexity.lower():
                                medium_rfi += 1
                            else:
                                difficult += 1

                        col1, col2, col3, col4 = st.columns(4)

                        #styling the metrics
                        def metric_card(label, value, bg, fg):
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: {bg};
                                    padding: 12px 16px;
                                    border-radius: 10px;
                                    text-align: center;
                                    border: 3px solid {fg}20;
                                ">
                                    <div style="
                                        color: {fg};
                                        font-size: 14px;
                                        font-weight: 600;
                                        margin-bottom: 4px;
                                    ">
                                        {label}
                                    </div>
                                    <div style="
                                        color: {fg};
                                        font-size: 28px;
                                        font-weight: 700;
                                    ">
                                        {value}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with col1:
                            metric_card("EASY – DISALLOW", easy_disallow, "#E8F5E9", "#2E7D32")

                        with col2:
                            metric_card("EASY – RFI (minimal)", easy_rfi, "#E8F5E9", "#2E7D32")

                        with col3:
                            metric_card("MEDIUM – RFI (extensive)", medium_rfi, "#FFF8E1", "#F9A825")

                        with col4:
                            metric_card("DIFFICULT", difficult, "#FFEBEE", "#C62828")

                        st.divider()
                        st.markdown("""
                            Want to view the full assessment details? <br>
                            Click on the <b>📥 Export Assessment</b> button at the sidebar on the left to download the results.
                        """, unsafe_allow_html=True
                        )