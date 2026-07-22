import streamlit as st
from utils.openai_client import stream_chat
from config.prompts import ANALYSIS_SYSTEM_PROMPT

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Property Objection Analyzer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Property Objection Analyzer")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("⚙️ Settings")

    system_prompt = st.text_area(
        "System Prompt",
        value="You are an experienced property tax officer. Analyse the objection and determine the Primary Bucket, Complexity Score (1–11), Urgency (Y/N), Recommended Course of Action, and supporting signals.",
        height=150,
    )

    selected_model = st.selectbox(
        "Model",
        [
            "gpt-4o-mini",
            "gpt-4o"
        ],
        index=0
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

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
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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

    # -----------------------------
    # Build messages for OpenAI
    # -----------------------------
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

    api_messages.extend(st.session_state.messages)

    # -----------------------------
    # Generate assistant response
    # -----------------------------
    with st.chat_message("assistant"):

        try:
            stream = stream_chat(
                messages=api_messages,
                api_key=st.secrets["OPENAI_API_KEY"],
                model=selected_model
            )

            response = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
            )

        except Exception as e:
            # Show friendly error message in Streamlit
            st.error(
                "Sorry, I was unable to process your request. "
                "Please try again later."
            )

            # Print full error details in terminal
            print("OpenAI API Error:", repr(e))

            # Fallback response for chat history
            response = (
                "I encountered an error while analysing your objection. "
                "Please try again."
            )

    # -----------------------------
    # Save assistant response
    # -----------------------------
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )