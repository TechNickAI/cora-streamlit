from agent_graph import create_agent_graph
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import streamlit as st
import uuid

# Set page config
st.set_page_config(page_title="Cora: Heart-Centered AI", page_icon="💙", layout="wide")

# Sidebar for settings
st.sidebar.title("Settings")
selected_llm = st.sidebar.selectbox("Large Language Model", ("Anthropic Claude 3.5", "OpenAI GPT 4o"))
enable_web_search = st.sidebar.checkbox(
    "Enable Web Search", help="Permit the AI to search the web for information.", value=True
)

# Collect settings
user_settings = {"llm": selected_llm, "search_web": enable_web_search}

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


def write_message(chat_message):
    if isinstance(chat_message, HumanMessage):
        with st.chat_message("Human"):
            st.write(chat_message.content)
    elif isinstance(chat_message, AIMessage):
        with st.chat_message("AI"):
            if isinstance(chat_message.content, str):
                if chat_message.content == "" and chat_message.tool_calls:
                    st.info(f"Tool Invoked: {chat_message.tool_calls[0]['name']}")
                    st.json(chat_message.tool_calls[0], expanded=False)
                else:
                    st.write(chat_message.content)
                    st.session_state.chat_history.append(AIMessage(content=chat_message.content))
            elif isinstance(chat_message.content, list):
                for chunk in chat_message.content:
                    if chunk["type"] == "text":
                        st.write(chunk["text"])
                        st.session_state.chat_history.append(AIMessage(content=chunk["text"]))
                    elif chunk["type"] == "tool_use":
                        st.info(f"Tool Utilized: {chunk['name']}")
                        st.json(chunk, expanded=False)
    elif isinstance(chat_message, ToolMessage):
        with st.chat_message("AI"):
            st.info("Tool Response")
            st.json(chat_message.content, expanded=False)


# Show the conversation from chat history
for message in st.session_state.chat_history:
    write_message(message)

user_input = st.chat_input("How may I assist you today?")
if user_input is not None and user_input != "":
    # Set up graph with config and thread id
    agent_graph = create_agent_graph(user_settings)
    runnable_config = RunnableConfig(configurable={"thread_id": st.session_state.thread_id})

    with st.chat_message("Human"):
        st.write(user_input)
        st.session_state.chat_history.append(HumanMessage(content=user_input))

    for stream_event in agent_graph.stream({"messages": st.session_state.chat_history}, config=runnable_config):
        # The top level response will either be agent or tool_call
        if "agent" in stream_event:
            response_messages = stream_event["agent"]["messages"]
        elif "tools" in stream_event:
            response_messages = stream_event["tools"]["messages"]

        for chat_message in response_messages:
            write_message(chat_message)
