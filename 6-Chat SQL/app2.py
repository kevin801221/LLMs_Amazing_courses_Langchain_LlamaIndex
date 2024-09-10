from pathlib import Path
from langchain.agents import create_sql_agent, initialize_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
import streamlit as st

# 設定頁面
st.set_page_config(page_title="LangChain: Chat with SQL and Web Search", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL and Web Search")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# 側邊欄選項
radio_opt = ["Use SQLLite 3 Database - Student.db", "Connect to your MySQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB you want to chat with", options=radio_opt)

# 根據選擇的資料庫類型，決定是否需要 MySQL 的變數
if selected_opt == "Connect to your MySQL Database":
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL password", type="password")
    mysql_db = st.sidebar.text_input("MySQL database")
else:
    db_uri = LOCALDB

# Groq API Key
api_key = st.sidebar.text_input(label="Groq API Key", type="password")

# 提示使用者輸入資料庫資訊和 API key
if not db_uri:
    st.info("Please enter the database information and URI")

if not api_key:
    st.info("Please add the Groq API key")

# 定義 LLM 模型
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# 定義資料庫配置函數
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

# 建立資料庫連接
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

# 定義 SQL 工具包
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Arxiv and Wikipedia Tools for external search
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)
search = DuckDuckGoSearchRun(name="Search")

# 結合 SQL 代理和搜尋工具
tools = [search, arxiv, wiki]  # 新增的搜尋工具
combined_agent = initialize_agent(
    tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# SQL Agent
sql_agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 管理訊息歷史
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 顯示歷史訊息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 使用者輸入的查詢
user_query = st.chat_input(placeholder="Ask anything from the database or search")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())

        # 根據輸入內容自動選擇 SQL 還是搜尋工具
        if "search" in user_query.lower() or "query" in user_query.lower():
            response = combined_agent.run(user_query, callbacks=[streamlit_callback])
        else:
            response = sql_agent.run(user_query, callbacks=[streamlit_callback])

        # 顯示回應
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
