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

from langchain_core.pydantic_v1 import BaseModel, Field

from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

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
tool_node = ToolNode(tools)

# Agents
# model = model.bind_tools(tools)

# TODO: Define the graph state/agent state
class AgentState(TypedDict):

    messages: Annotated[list, add_messages]
    
# TODO: Define the Nodes & Edge

tool_executor = ToolExecutor(tools)

# Node 1:
def run_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": response}
    
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    
    if not last_message.tool_calls:
        return "end"
    return "action"
    
# TODO: Define LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_model)
workflow.add_node("action", tool_node)
# workflow.add_node("final", execute_tools)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    
    "agent",
    should_continue,

)

# Define normal edge
workflow.add_edge("action", "agent")
# workflow.add_edge("final", END)

memory = SqliteSaver.from_conn_string(":memory")
app = workflow.compile(checkpointer=memory)

# TODO: Run The Graph
config = {"configurable": {"thread_id": "memory_1"}}
inputs = HumanMessage(content="Hi, I'm Ken!")
for event in app.stream(
    {"messages": [inputs]},
    config,
    stream_mode="values"
):
    event["messages"][-1].pretty_print()
    
inputs = HumanMessage(content="What is my name?")
for event in app.stream(
    {"messages": [inputs]},
    config,
    stream_mode="values"
):
    event["messages"][-1].pretty_print()
    
inputs = HumanMessage(content="What is my name?")
for event in app.stream(
    {"messages": [inputs]},
    config = {"configurable": {"thread_id": "memory_2"}},
    stream_mode="values"
):
    event["messages"][-1].pretty_print()
    