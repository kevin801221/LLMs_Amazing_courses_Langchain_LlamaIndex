import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="langchain_search_api_key_openai", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/kevin801221/Langchain_course_code/blob/main/10-Streamlit_Page_Designing_Template_For_LLMApps/streamlit_llm-examples/pages/2_Chat_with_search.py)"
    

st.title("🔎 LangChain - 聊天加上搜尋")

"""
在這個例子中，我們將使用 StreamlitCallbackHandler 來在互動式 Streamlit 應用程式中顯示代理的思考和行動。

更多 LangChain 🤝 Streamlit 代理範例請參閱 [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "嗨，我是一個可以搜尋網路的聊天機器人。我能為你做些什麼？"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="2024年台灣在科技創新方面有什麼新突破？還有台灣在2024年針對環保議題推出了哪些新政策？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("請給我你的OPENAI api key")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent(
        [search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
