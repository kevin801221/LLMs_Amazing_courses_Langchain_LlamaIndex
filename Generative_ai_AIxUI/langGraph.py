import os
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent

import operator
from typing import TypedDict, Union, Annotated
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage

from langgraph.prebuilt.tool_executor import ToolExecutor

from langgraph.graph import END, StateGraph

load_dotenv()

prompt = hub.pull("hwchase17/openai-functions-agent")
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.9,
    streaming=True
)

# Tool
search = TavilySearchResults(
    tavily_api_key=os.getenv("TAVITY_API_KEY"),
    max_results=1
)
tools = [search]

# Agents
search_agent = create_openai_functions_agent(model, tools, prompt)

# TODO: Define the graph state/agent state
class AgentState(TypedDict):
    
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]],operator.add]
    
# TODO: Define the Nodes & Edge

tool_executor = ToolExecutor(tools)

# Node 1:
def run_agent(data):
    agent_outcome = search_agent.invoke(data)
    return {"agent_outcome": agent_outcome}

# Node 2:
def execute_tools(data):
    agent_action = data["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}
    
def should_continue(data):
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    else:
        return "continue"
    
# TODO: Define LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

# Define normal edge
workflow.add_edge("action", "agent")

app = workflow.compile()

# TODO: Run The Graph
inputs = {"input": "What is the weather in Taipei?", "chat_history": []}

for sentence in app.stream(inputs):
    print(list(sentence.values())[0])
    print("------------------------------------------")

