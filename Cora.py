from agent_graph import create_agent_graph, prompt_engineer
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from loguru import logger
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
enable_preprompting = st.sidebar.checkbox(
    "Enable Pre-prompting", help="Do prompt engineering before sending it to the AI.", value=False
)

# Collect settings
user_settings = {"llm": selected_llm, "search_web": enable_web_search}
logger.debug(f"User settings: {user_settings}")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.debug("Initialized chat history in session state")
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    logger.debug(f"Generated new thread ID: {st.session_state.thread_id}")


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
                    return chat_message
            elif isinstance(chat_message.content, list):
                for chunk in chat_message.content:
                    if chunk["type"] == "text":
                        st.write(chunk["text"])
                        return AIMessage(content=chunk["text"])
                    elif chunk["type"] == "tool_use":
                        st.info(f"Tool Utilized: {chunk['name']}")
                        st.json(chunk, expanded=False)
    elif isinstance(chat_message, ToolMessage):
        with st.chat_message("AI"):
            st.info("Tool Response")
            st.json(chat_message.content, expanded=False)

    return None


# Show the conversation from chat history
for message in st.session_state.chat_history:
    write_message(message)

user_input = st.chat_input("How may I assist you today?")
if user_input is not None and user_input != "":
    logger.debug(f"User input: {user_input}")

    # Handle user input
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("Human"):
        st.write(user_input)

    if enable_preprompting:
        with st.spinner("Applying prompt engineering to your request..."):
            engineered_input = prompt_engineer(user_input)
            st.info(engineered_input.content)
            user_input = engineered_input.content

    # Set up graph with config and thread id
    agent_graph = create_agent_graph(user_settings)
    runnable_config = RunnableConfig(configurable={"thread_id": st.session_state.thread_id})

    for stream_event in agent_graph.stream({"messages": st.session_state.chat_history}, config=runnable_config):
        # The top level response will either be agent or tool_call
        if "agent" in stream_event:
            response_messages = stream_event["agent"]["messages"]
        elif "tools" in stream_event:
            response_messages = stream_event["tools"]["messages"]

        for chat_message in response_messages:
            saved_message = write_message(chat_message)
            if saved_message is not None:
                st.session_state.chat_history.append(saved_message)
