import os
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub

from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor

load_dotenv()

prompt = hub.pull("hwchase17/openai-functions-agent")
model = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.9
)

# Tool
search = TavilySearchResults(tavily_api_key=os.getenv("TAVITY_API_KEY"))
tools = [search]

# Agents
search_agent = create_openai_functions_agent(model, tools, prompt)
result = search_agent.invoke({"input": "What is the weather in Taiwan?", "intermediate_steps": []})

# print(result.tool)
# print(result.tool_input)
# print(result)

agent_executor = AgentExecutor(
    agent = search_agent,
    tools = tools
)
agent_result = agent_executor.invoke({"input": "What is the weather in Taiwan?"})

# print(agent_result)

for step in agent_executor.stream({"input": "What is the weather in HongKong?"}):
    print(step)