from agent_graph import create_agent_graph
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import streamlit as st
import uuid

# Set page config
st.set_page_config(page_title="Cora: Heart Centered AI", page_icon="💙", layout="wide")

# Sidebar for LLM provider selection
st.sidebar.title("Settings")
llm = st.sidebar.selectbox("Select LLM Provider", ("Anthropic Claude 3.5", "OpenAI GPT 4o"))

# Title
st.title("Cora: Heart Centered AI 🤖 + 💙")

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Show the conversation from chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)


# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    # Set up graph with config and thread id
    graph = create_agent_graph(llm)
    callbacks = []
    config = RunnableConfig(callbacks=callbacks, configurable={"thread_id": st.session_state.thread_id})

    with st.chat_message("Human"):
        st.write(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))

    response_text = ""
    for event in graph.stream({"messages": st.session_state.chat_history}, config=config):
        # The top level response will either be agent or tool_call
        if "agent" in event:
            messages = event["agent"]["messages"]
        elif "tools" in event:
            messages = event["tools"]["messages"]

        for message in messages:
            if isinstance(message, ToolMessage):
                with st.chat_message("AI"):
                    st.info("Tool response")
                    st.json(message.content, expanded=False)

            elif isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    # The message content can either be a string or a list, depending on the LLM provider
                    if isinstance(message.content, str):
                        if message.content == "" and message.tool_calls:
                            st.info(f"Tool called: {message.tool_calls[0]['name']}")
                            st.json(message.tool_calls[0], expanded=False)
                        else:
                            st.write(message.content)
                            st.session_state.chat_history.append(AIMessage(content=message.content))

                    elif isinstance(message.content, list):
                        for chunk in message.content:
                            if chunk["type"] == "text":
                                st.write(chunk["text"])
                                st.session_state.chat_history.append(AIMessage(content=message.content))
                            elif chunk["type"] == "tool_use":
                                st.info(f"Tool used: {chunk['name']}")
                                st.json(chunk, expanded=False)
