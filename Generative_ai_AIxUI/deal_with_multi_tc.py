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

from langgraph.checkpoint.memory import MemorySaver

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
    
    # tool_call = last_message.tool_calls[0]
    
    # action = ToolInvocation(
    #     tool=tool_call["name"],
    #     tool_input=tool_call["args"]
    # )
    
    tool_invocations = []
    for tool_call in last_message.tool_calls:
        action = ToolInvocation(
            tool=tool_call["name"],
            tool_input=tool_call["args"]
        ) 
        tool_invocations.append(action)   
    print("Tool Invocations: ", tool_invocations)
    
    # response = tool_executor.invoke(action)
    response = tool_executor.batch(tool_invocations, return_exceptions=True)
    
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

app = workflow.compile(checkpointer=MemorySaver(), interrupt_before=["action"])

# TODO: Run The Graph
inputs = {"messages": [HumanMessage(content="What is the weather in Taipei?")]}

# for sentence in app.stream(inputs):
#     print(list(sentence.values())[0])
#     print("------------------------------------------")

config = {"configurable": {"thread_id": "langGraph-1"}}

while True:
    for output in app.stream(inputs, config):
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("------------------------------------------")
            print(value)
        print("\n-------\n")
    snapshot = app.get_state(config)
    
    if not snapshot.next:
        break
    inputs = None
    response = input(
        "Do you approve the next step? Type y if you do, anything else to stop: "
    )
    if response != "y":
        break