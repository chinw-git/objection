import streamlit as st
from functions.openai_client import stream_chat

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
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    # Save and display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):

        stream = stream_chat(
            messages=st.session_state.messages,
            api_key=st.secrets["OPENAI_API_KEY"]
        )

        response = st.write_stream(
            chunk.choices[0].delta.content or ""
            for chunk in stream
        )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
    }
)