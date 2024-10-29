from langchain import hub
from langchain.agents import Tool, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from typing import TypedDict, Annotated, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator
from typing import TypedDict, Annotated
from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.prebuilt import ToolInvocation
from langgraph.graph import END, StateGraph
from langchain_core.agents import AgentActionMessageLog
import streamlit as st
# from langchain.tools.serper import Serper
os.environ["SERPER_API_KEY"] = ""

search = GoogleSerperAPIWrapper()

# st.set_page_config(page_title="LangChain Agent", layout="wide")

# def toggle_case(word):
#             toggled_word = ""
#             for char in word:
#                 if char.islower():
#                     toggled_word += char.upper()
#                 elif char.isupper():
#                     toggled_word += char.lower()
#                 else:
#                     toggled_word += char
#             return toggled_word

# def sort_string(string):
#      return ''.join(sorted(string))

# tools = [
#       Tool(
#           name = "Search",
#           func=search.run,
#           description="useful for when you need to answer questions about current events",
#       ),
#       Tool(
#           name = "Toogle_Case",
#           func = lambda word: toggle_case(word),
#           description = "use when you want covert the letter to uppercase or lowercase",
#       ),
#       Tool(
#           name = "Sort String",
#           func = lambda string: sort_string(string),
#           description = "use when you want sort a string alphabetically",
#       ),

#         ]
# prompt = hub.pull("hwchase17/react")

# llm = ChatGoogleGenerativeAI(model="gemini-pro",
#       google_api_key="AIzaSyDJF8A6JHpucPUCEEbNWwUPfUmq1mE4Zn4",
#       convert_system_message_to_human = True,
#       verbose = True,
# )

# agent_runnable = create_react_agent(llm, tools, prompt)
# class AgentState(TypedDict):
#     input: str
#     chat_history: list[BaseMessage]
#     agent_outcome: Union[AgentAction, AgentFinish, None]
#     return_direct: bool
#     intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

#  tool_executor = ToolExecutor(tools)



# def run_agent(state):
#             """
#             #if you want to better manages intermediate steps
#             inputs = state.copy()
#             if len(inputs['intermediate_steps']) > 5:
#                 inputs['intermediate_steps'] = inputs['intermediate_steps'][-5:]
#             """
#             agent_outcome = agent_runnable.invoke(state)
#             return {"agent_outcome": agent_outcome}
# def main():
#     # Streamlit UI elements
#     st.title("LangGraph Agent + Gemini Pro + Custom Tool + Streamlit")

#     # Input from user
#     input_text = st.text_area("Enter your text:")
    
#     if st.button("Run Agent"):

# app.py
# import os
# import streamlit as st
# from typing import TypedDict, Annotated, Union
# import operator

# # LangChain 和相關庫
# from langchain import PromptTemplate
# from langchain.llms import GooglePalm
# from langchain.agents import Tool, initialize_agent, AgentType
# from langchain.tools import BaseTool
# from langchain.schema import AgentAction, AgentFinish, BaseMessage
# from langchain.agents import AgentExecutor
# # from langchain_community.serper import SerperAPIWrapper
# # LangGraph
# from langgraph.graph import StateGraph, END
# from langgraph.prebuilt.tool_executor import ToolExecutor
# from langgraph.prebuilt import ToolInvocation

# 確保已經設置了 GOOGLE_API_KEY 和 SERPER_API_KEY 環境變量
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

if not GOOGLE_API_KEY:
    st.error("請設置您的 GOOGLE_API_KEY 環境變量。")
    st.stop()

if not SERPER_API_KEY:
    st.error("請設置您的 SERPER_API_KEY 環境變量。")
    st.stop()

# 設置頁面配置
st.set_page_config(page_title="LangGraph Agent", layout="wide")

def main():
    # Streamlit UI 元素
    st.title("LangGraph Agent + Gemini Pro + 自定義工具 + Streamlit")

    # 用戶輸入
    input_text = st.text_area("請輸入您的文字：")

    if st.button("運行 Agent"):
        # 定義自定義工具
        # 1. 搜索工具（使用 Serper API）
        from langchain.utilities import SerperAPIWrapper
        search = SerperAPIWrapper(serper_api_key=SERPER_API_KEY)

        # 2. 大小寫轉換工具
        def toggle_case(word):
            toggled_word = ""
            for char in word:
                if char.islower():
                    toggled_word += char.upper()
                elif char.isupper():
                    toggled_word += char.lower()
                else:
                    toggled_word += char
            return toggled_word

        # 3. 字串排序工具
        def sort_string(string):
            return ''.join(sorted(string))

        # 定義工具列表
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="當你需要回答有關當前事件的問題時很有用。"
            ),
            Tool(
                name="Toggle_Case",
                func=toggle_case,
                description="當你想將字母轉換為大寫或小寫時使用。"
            ),
            Tool(
                name="Sort_String",
                func=sort_string,
                description="當你想按字母順序排序字串時使用。"
            ),
        ]

        # 初始化 LLM（使用 Google Gemini Pro）
        llm = GooglePalm(
            api_key=GOOGLE_API_KEY,
            model_name="models/chat-bison-001",
            temperature=0.7,
            verbose=True
        )

        # 定義 Agent 的狀態類
        class AgentState(TypedDict):
            input: str
            chat_history: list[BaseMessage]
            agent_outcome: Union[AgentAction, AgentFinish, None]
            return_direct: bool
            intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

        # 初始化 ToolExecutor
        tool_executor = ToolExecutor(tools)

        # 定義 Agent 的函數
        def run_agent(state):
            # 使用 LangChain 的 AgentExecutor
            agent = initialize_agent(
                tools,
                llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )
            agent_outcome = agent.agent.plan(
                intermediate_steps=state.get('intermediate_steps', []),
                callbacks=None,
                user_input=state['input']
            )
            return {"agent_outcome": agent_outcome}

        def execute_tools(state):
            agent_outcome = state['agent_outcome']
            if isinstance(agent_outcome, AgentAction):
                action = ToolInvocation(
                    tool=agent_outcome.tool,
                    tool_input=agent_outcome.tool_input
                )
                response = tool_executor.invoke(action)
                return {
                    "intermediate_steps": state.get('intermediate_steps', []) + [(agent_outcome, response)],
                    "agent_outcome": agent_outcome
                }
            else:
                return {"agent_outcome": agent_outcome}

        def should_continue(state):
            agent_outcome = state['agent_outcome']
            if isinstance(agent_outcome, AgentFinish):
                return "end"
            else:
                return "continue"

        # 定義處理流程圖
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

        workflow.add_edge('action', 'agent')

        app = workflow.compile()

        # 運行應用
        inputs = {
            "input": input_text,
            "chat_history": [],
            "return_direct": False,
            "intermediate_steps": []
        }

        results = []
        for s in app.stream(inputs):
            result = s.get('agent_outcome')
            if isinstance(result, AgentAction):
                st.write(f"Agent 決定使用工具：{result.tool}")
                st.write(f"工具輸入：{result.tool_input}")
            elif isinstance(result, AgentFinish):
                st.write("Agent 最終回應：")
                st.write(result.return_values['output'])
            else:
                st.write("未知的 Agent 結果")

if __name__ == "__main__":
    main()