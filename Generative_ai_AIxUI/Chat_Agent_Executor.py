import os
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

import operator
from typing import TypedDict, Sequence, Annotated
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage

from langgraph.prebuilt.tool_executor import ToolExecutor

from langgraph.graph import END, StateGraph

from langchain_core.messages import ToolMessage, HumanMessage
from langgraph.prebuilt import ToolInvocation

load_dotenv()

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
model = model.bind_tools(tools)

# TODO: Define the graph state/agent state
class AgentState(TypedDict):

    messages: Annotated[Sequence[BaseMessage],operator.add]
    
# TODO: Define the Nodes & Edge

tool_executor = ToolExecutor(tools)

# Node 1:
def run_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

# Node 2:
def execute_tools(state):
    messages = state["messages"]
    last_message = messages[-1]
    tool_call = last_message.tool_calls[0]
    
    action = ToolInvocation(
        tool=tool_call["name"],
        tool_input=tool_call["args"]
    )
    response = tool_executor.invoke(action)
    
    tool_message = ToolMessage(
        content=str(response),
        name=action.tool,
        tool_call_id=tool_call["id"]
    )
    
    return {"messages": [tool_message]}
    
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    
# TODO: Define LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_model)
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
inputs = {"messages": [HumanMessage(content="What is the weather in Taipei?")]}

# for sentence in app.stream(inputs):
#     print(list(sentence.values())[0])
#     print("------------------------------------------")

for output in app.stream(inputs):
    for key, value in output.items():
        print(f"Output from node '{key}':")
        print("------------------------------------------")
        print(value)
    print("\n-------\n")