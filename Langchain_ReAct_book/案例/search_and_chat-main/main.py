from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory)

import streamlit as st

# 创建 浏览器 tab title
st.set_page_config(page_title='基于 Streamlit 的聊天机器人')

# ================== 左边栏配置部分 =======================
openai_api_base = st.sidebar.text_input(
    'OpenAI API Base', value='https://api.openai.com/v1'
)
openai_api_key = st.sidebar.text_input(
    'OpenAI API Key', type='password'
)

model = st.sidebar.selectbox(
    'Model', ('gpt-3.5-turbo', 'gpt-4-1106-preview')
)

temperature = st.sidebar.slider(
    'Temperature', 0.0, 2.0, value=0.6, step=0.1
)

# ================== 中间聊天部分 =======================
# 实例化用于存储聊天记录的 History 对象
message_history = StreamlitChatMessageHistory()
# 当没有聊天内容或点击“清空聊天历史记录”按钮时，做一些初始化的操作
if not message_history.messages or st.sidebar.button('清空聊天历史记录'):
    message_history.clear()
    message_history.add_ai_message('有什么可以帮你的吗？')

    # 用于存放中间步骤信息
    st.session_state.steps = {}

# 每次提问都会刷新清空整个聊天列表
# 所以这里需要通过 message_history 将历史聊天消息再遍历的添加回聊天列表中
for index, msg in enumerate(message_history.messages):
    with st.chat_message(msg.type):
        # 将中间步骤添加到聊天列表中
        for step in st.session_state.steps.get(str(index), []):
            if step[0].tool == '_Exception':
                continue
            with st.status(
                f'**{step[0].tool}**: {step[0].tool_input}',
                state='complete'
            ):
                st.write(step[0].log)
                st.write(step[1])

        # 将对话内容添加到聊天列表中
        st.write(msg.content)

# 添加问题输入框
prompt = st.chat_input(placeholder='请输入提问内容')
if prompt:
    # 如果没有设置 openai_api_key 就设置消息框，并且停止后续的执行
    if not openai_api_key:
        st.info('请先输入 OpenAI API Key')
        st.stop()

    # 将输入框的内容添加到用户聊天内容中
    st.chat_message('human').write(prompt)

    # 构建 Agent
    llm = ChatOpenAI(
        model=model,
        openai_api_key=openai_api_key,
        streaming=True,
        temperature=temperature,
        openai_api_base=openai_api_base
    )

    tools = [DuckDuckGoSearchRun(name='Search')]
    chat_agent = ConversationalChatAgent.from_llm_and_tools(
        llm=llm, tools=tools
    )
    memory = ConversationBufferWindowMemory(
        chat_memory=message_history,
        return_messages=True,
        memory_key='chat_history',
        output_key='output',
        k=6
    )
    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )

    # 添加ai回复内容
    with st.chat_message('ai'):
        # 会在界面上显示中间步骤，如搜索、思考等，但只限当前提问
        # 下一轮提问时，这里显示的步骤将不会存在
        # 所以在上方会再一次将中间步骤添加到聊天列表中，
        # 这样中间步骤将会一直保留在聊天列表中
        st_cb = StreamlitCallbackHandler(
            st.container(),
            expand_new_thoughts=False
        )
        response = executor(prompt, callbacks=[st_cb])
        st.write(response['output'])

        # 保存中间步骤
        step_index = str(len(message_history.messages) - 1)
        st.session_state.steps[step_index] = response['intermediate_steps']
