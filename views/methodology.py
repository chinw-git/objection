## METHODOLOGY ##
import streamlit as st

def render_methodology():
#     st.set_page_config(page_title="Methodology", page_icon="🧩")

        st.title("Our Methodology")
        st.divider()

        st.markdown("""
        Our application combines **Retrieval-Augmented Generation (RAG)** with a **multi-agent workflow** 
        to support the assessment of property tax objections.

        Rather than relying solely on an LLM's general knowledge, the system retrieves
        relevant information from the **Property Tax Act (PTA)** and uses a
        **predefined complexity assessment rubric** to ground the assessment.
        """)


        # Overall Workflow
        st.subheader("Overall Workflow")

        st.image(
        "assets/workflow.png",
        caption="Multi-agent workflow for property tax objection assessment",
        width=700
        )

        st.markdown("""
        <div style="
        background-color: #EAF3FA;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        ">
        <ol style="margin: 0; padding-left: 20px;">
                <li style="margin-bottom: 10px;">
                When an objection is submitted, the <b>Legislation Agent</b> first
                retrieves the relevant Property Tax Act (PTA) sections.
                </li>
                <li style="margin-bottom: 10px;">
                The <b>Classifier Agent</b> then assesses the objection using the
                retrieved legislation and predefined criteria set out in the
                assessment rubric to help determine its complexity.
                </li>
                <li style="margin-bottom: 10px;">
                Based on the objection and its complexity assessment, the <b>Recommender Agent</b> suggests
                appropriate next steps for the officer.
                </li>
                <li>
                Similar past cases are retrieved separately and provided
                together with the assessment output to provide users with
                additional reference.
                </li>
        </ol>
        </div>""",
        unsafe_allow_html=True
        )

        # MULTI-AGENT APPROACH
        st.subheader("Multi-Agent Approach")

        st.markdown("""Each agent performs a specialised role within the overall workflow.""")

        agents = [
        (
                "⚖️ Legislation Agent",
                "Focuses on retrieving relevant PTA provisions to provide legislative context for the assessment."
        ),
        (
                "🏷️ Classifier Agent",
                "Evaluates the objection against the predefined rubric and retrieved legislative context to determine its complexity."
        ),
        (
                "💡 Recommender Agent",
                "Uses the assessed complexity to suggest appropriate next steps."
        )
        ]

        for title, description in agents:
                st.markdown(
                        f"""
                        <div style="
                        background-color: #F3F8FC;
                        padding: 14px 18px;
                        border-radius: 8px;
                        margin-bottom: 10px;
                        border-left: 4px solid #7DA3BD;
                        ">
                        <strong style="color:#39505C;">{title}</strong>
                        <p style="margin:5px 0 0 0; color:#39505C;">
                                {description}
                        </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                )

        # Vector Stores
        st.subheader("Knowledge and Retrieval")

        st.markdown(
        """
        <div style="
        background-color: #EAF3FA;
        padding: 10px 20px;
        margin-bottom: 10px;
        border-radius: 10px;
        ">
        <h5>⚖️ <u>Property Tax Act (PTA)</u></h5>
                <p>
                The primary source of legislative provisions 
                for the assessment and classification of objections.
                </p>
                <p>
                <b>Document processing</b><br>
                PTA content is divided into semantically meaningful chunks using <code>SemanticChunker</code>, 
                allowing related provisions to remain together and improving the retrieval of relevant legislative context.
                </p>
                <p>
                <b>Storage & Retrieval</b><br>
                The processed PTA chunks are embedded using <code>text-embedding-3-small</code> and stored in a 'legislation' <code>Chroma</code> vector store. <br>
                The <b>top 5</b> most relevant provisions are retrieved using <code>MultiQueryRetriever</code>, which generates multiple variations of the objection to
                capture different ways the same issue may be expressed, improving retrieval of relevant PTA provisions.
                </p>
        <h5>📂 <u>Past Objection Cases</u></h5>
                <p>
                Past objection cases are retrieved separately as reference material
                to provide additional context and examples of similar cases for users.
                </p>
                <p>
                <b>Document processing</b><br>
                Each past objection case is retained as an individual document without further chunking, preserving the 
                complete objection text and its context for retrieval as a reference.
                </p>
                <p>
                <b>Storage & Retrieval</b><br>
                Each past objection document is embedded using <code>text-embedding-3-small</code> and stored in a 'past cases' <code>Chroma</code>vector store. <br>
                Similar past cases are identified based on their semantic similarity to the submitted objection, with the <b>top 5</b> most similar cases retrieved as references.
                </p>
        </div>
        """,
        unsafe_allow_html=True
        )


        # COMPLEXITY ASSESSMENT
        st.subheader("Complexity Assessment")

        st.markdown(
        """
        Objections are categorised into 4 complexity levels to support
        the assessment and recommendation process.
        """
        )

        complexities = [
        (
                "🟢",
                "EASY – DISALLOW",
                "Straightforward cases suitable for disallowance"
        ),
        (
                "🟢",
                "EASY – RFI (minimal)",
                "Straightforward cases requiring limited further information"
        ),
        (
                "🟡",
                "MEDIUM – RFI (extensive)",
                "Cases requiring more extensive information or assessment"
        ),
        (
                "🔴",
                "DIFFICULT",
                "More complex cases requiring further review"
        ),
        ]

        columns = st.columns(4)

        for col, (icon, title, description) in zip(columns, complexities):
                with col:
                        st.markdown(
                        f"""
                        <div style="
                        background-color: #EAF3FA;
                        color: #39505C;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-radius: 10px;
                        text-align: center;
                        ">
                                {icon} <b>{title}</b>
                                <br>
                                <i>{description}</i>
                        </div>
                        """,
                        unsafe_allow_html=True
                        )

        # Output
        st.subheader("Assessment Output")

        st.markdown(
        """
        At the end, the application brings together the agents' assessments, recommendations and retrieved
        information to provide users with a consolidated view comprising of:
        """
        )

        st.markdown("**1. Complexity Assessment**")
        st.markdown("""
        The assessed complexity level of the objection, together with the reasoning behind the classification. <br>
        Relevant Property Tax Act (PTA) provisions supporting the assessment will also be displayed along with the rationale for its relevance. <br>
        _Up to 5_ relevant provisions may be shown, depending on their relevance to the assessment.
        """, unsafe_allow_html=True
        )

        st.markdown("**2. Recommendation and Next Steps**")
        st.markdown("""
        Recommended follow-up actions for officers based on the assessed complexity, such as requesting tenancy information or determining whether
        escalation to a senior officer is required.
        """
        )

        st.markdown("**3. Similar Cases**")
        st.markdown(
        "Similar past objection cases will be reflected as additional reference for the officers."
        )