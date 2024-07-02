from agent_graph import create_agent_graph, prompt_engineer
from audiorecorder import audiorecorder
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from loguru import logger
from openai import OpenAI
from pathlib import Path
import streamlit as st
import tempfile
import uuid

# ---------------------------------------------------------------------------- #
#                             Streamlit page set up                            #
# ---------------------------------------------------------------------------- #

ai_logo = "assets/logo.png"
st.set_page_config(page_title="Cora: Heart-Centered AI", page_icon=ai_logo, layout="wide")
st.logo(ai_logo, icon_image=ai_logo)


# ------------------------------ Session set up ------------------------------ #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.debug("Initialized chat history in session state")
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    logger.debug(f"Generated new thread ID: {st.session_state.thread_id}")

# --------------------------- Sidebar for settings --------------------------- #
st.sidebar.title("Settings")
selected_llm = st.sidebar.selectbox("Large Language Model", ("Anthropic Claude 3.5", "OpenAI GPT 4o"))
enable_web_search = st.sidebar.checkbox(
    "Enable Web Search", help="Permit the AI to search the web for information.", value=True
)
enable_preprompting = st.sidebar.checkbox(
    "Enable Pre-prompting", help="Do prompt engineering before sending it to the AI.", value=True
)
user_settings = {"llm": selected_llm, "search_web": enable_web_search}
logger.debug(f"User settings: {user_settings}")


# ----------------------------- Helper functions ----------------------------- #


def write_message(chat_message):
    """
    Writes a chat message to the Streamlit chat interface based on its type.

    Distinguish between AIMessage and ToolMessage and HumanMessage.

    Handle the difference between
    Anthropic Claude 3.5 (which responds with a list)
    vs
    OpenAI GPT 4o (which responds with a string).
    """
    if isinstance(chat_message, HumanMessage):
        with st.chat_message("Human"):
            st.write(chat_message.content)

    elif isinstance(chat_message, AIMessage):
        with st.chat_message("AI", avatar=ai_logo):
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


def transcribe_audio(audio_buffer):
    audio_file_name = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    audio_buffer.export(audio_file_name, format="wav")
    audio_file = Path.open(audio_file_name, "rb")

    client = OpenAI()
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcription.text


# Show the conversation from chat history
for message in st.session_state.chat_history:
    write_message(message)

# ---------------------------------------------------------------------------- #
#                              Handle the request                              #
# ---------------------------------------------------------------------------- #

user_request = st.chat_input("How may I assist you today?")

audio_buffer = audiorecorder("", "")
if len(audio_buffer) > 0:
    with st.spinner("Transcribing..."):
        user_request = transcribe_audio(audio_buffer)
        audio_buffer = None

if user_request:
    logger.debug(f"User input: {user_request}")

    # Handle user input
    st.session_state.chat_history.append(HumanMessage(content=user_request))
    with st.chat_message("Human"):
        st.write(user_request)

    if enable_preprompting:
        with st.spinner("Applying prompt engineering to your request..."):
            engineered_input = prompt_engineer(user_request)
            st.info(engineered_input.content)
            user_request = engineered_input.content

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
