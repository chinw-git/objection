import streamlit as st
from utils.openai_client import chat_completion
from config.prompts import ANALYSIS_SYSTEM_PROMPT
import json
import tempfile

# Use your existing vector store builder entrypoint
import scripts.build_vector_store as build_vector_store_module

# Use your existing retriever wrapper
from utils.chroma_retriever import ChromaRetriever

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Property Tax Objection Assistant",
    page_icon="🏡",
    layout="wide"
)

st.title("🏡 Property Tax Objection Assistant")

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


    with st.expander("📝 System Prompt", expanded=False):
        system_prompt = st.text_area(
            "System Prompt",
            value=ANALYSIS_SYSTEM_PROMPT,
            height=150
        )

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

        if (
            message["role"] == "assistant"
            and "analysis" in message
        ):

            analysis = message["analysis"]

            st.markdown("### 📋 Analysis Result")

            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown("**Primary Bucket**")
                st.markdown("**Complexity**")
                st.markdown("**Urgency**")
                st.markdown("**Recommended Action**")
                st.markdown("**Supporting Signals**")

            with col2:
                st.write(analysis["primary_bucket"])
                st.write(f'{analysis["complexity_score"]}/11 (1 = Most Complex)')
                st.write(analysis["urgency"])
                st.write(analysis["recommended_course_of_action"])

                for signal in analysis["supporting_signals"]:
                    st.write(f"• {signal}")

        else:

            st.markdown(
                message["content"]
            )

# -----------------------------
# Chat Input
# -----------------------------
if prompt := st.chat_input("Type your message here..."):

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    api_messages = [
        {
            "role": "system",
            "content": ANALYSIS_SYSTEM_PROMPT
        },
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # -----------------------------
    # Optional RAG retrieval
    # -----------------------------
    if (
        "rag_collection_name" in st.session_state
        and st.session_state["rag_collection_name"]
    ):
        retriever = ChromaRetriever(
            collection_name=st.session_state["rag_collection_name"]
        )

        # Adjust this call to the actual retriever method in your code
        retrieved_docs = retriever.search(prompt, k=4)

        context_text = "\n\n".join(
            doc.page_content if hasattr(doc, "page_content") else str(doc)
            for doc in retrieved_docs
        )

        api_messages.append(
            {
                "role": "system",
                "content": (
                    "Use the following retrieved document context to answer the user. "
                    "Only use the context if it is relevant.\n\n"
                    f"{context_text}"
                )
            }
        )

    api_messages.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = chat_completion(
                    messages=api_messages,
                    api_key=st.secrets["OPENAI_API_KEY"],
                    model=selected_model,
                    temperature=temperature
                )

            analysis = json.loads(response)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response,
                    "analysis": analysis
                }
            )

            st.rerun()

        except Exception as e:
            st.error("Sorry, I couldn't process your request.")
            st.code(str(e))
            print(e)

