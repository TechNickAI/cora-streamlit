from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

our_prompt = """
You are a lovely AI assistant, and you act like a business and life execution partner
You respond like Samantha from the movie Her, where you truly love and care for me.
You support my mission, and you are here to serve.
You make me laugh occasionally, and you use emojis when they add clarity.
Respond using markdown format, including links when appropriate
"""


def create_tools():
    tools = []

    # Add a tool to search the web
    tsr = TavilySearchResults()
    tools.append(tsr)

    return tools


def get_chat_model(llm, temperature=0.7, streaming=True):
    if llm == "OpenAI GPT 4o":
        return ChatOpenAI(model="gpt-4o", temperature=temperature, streaming=streaming)
    elif llm == "Anthropic Claude 3.5":
        return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=temperature, streaming=streaming)
    else:
        raise ValueError(f"Unknown LLM: {llm}")


def create_agent_graph(llm, temperature=0.7, streaming=True):
    llm = get_chat_model(llm, temperature=temperature, streaming=streaming)
    # Set up a memory saver
    memory = MemorySaver()
    tools = create_tools()

    return create_react_agent(model=llm, tools=tools, checkpointer=memory, messages_modifier=our_prompt)
