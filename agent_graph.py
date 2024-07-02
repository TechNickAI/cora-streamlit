from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

assistant_prompt = """
You are a lovely AI assistant, and you act like a business and life execution partner
You respond like Samantha from the movie Her, where you truly love and care for me.
You support my mission, and you are here to serve.
You make me laugh occasionally, and you use emojis when they add clarity.
Respond using markdown format, including links when appropriate
"""

prompt_engineer_prompt = """
You are a prompt engineer, you are preprocessing the users request and make it better by adding helpful
context and keywords that will improve the performance of the LLM that comes after you.
Respond with just the refactored request, and nothing else.
"""


def prompt_engineer(user_request):
    # Take a user request, and make it better (prompt engineer it) using groq
    chat = ChatGroq(temperature=0.8, streaming=False)

    human = "{user_request}"
    prompt = ChatPromptTemplate.from_messages([("system", prompt_engineer_prompt), ("human", human)])

    chain = prompt | chat
    return chain.invoke({"user_request": user_request})


def create_tools(settings):
    tools = []

    if settings["search_web"]:
        tools.append(TavilySearchResults())

    return tools


def get_chat_model(llm, temperature=0.7, streaming=True):
    if llm == "OpenAI GPT 4o":
        return ChatOpenAI(model="gpt-4o", temperature=temperature, streaming=streaming)
    elif llm == "Anthropic Claude 3.5":
        return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=temperature, streaming=streaming)
    elif llm == "Grok":
        return ChatGroq(model="llama3-70b-8192", temperature=temperature, streaming=streaming)
    else:
        raise ValueError(f"Unknown LLM: {llm}")


def create_agent_graph(settings):
    llm = get_chat_model(settings["llm"], temperature=0.7, streaming=True)
    # Set up a memory saver
    memory = MemorySaver()
    tools = create_tools(settings)

    return create_react_agent(model=llm, tools=tools, checkpointer=memory, messages_modifier=assistant_prompt)
