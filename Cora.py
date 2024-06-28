import streamlit as st

# Set page config
st.set_page_config(page_title="Cora: Heart Centered AI", page_icon="💙", layout="wide")

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("Cora: Heart Centered AI 🤖 + 💙")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simulate AI response (replace with actual AI logic later)
    response = "42"

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response)
