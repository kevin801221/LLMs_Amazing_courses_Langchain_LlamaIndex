from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
import streamlit as st
import pandas as pd
import os
import nltk

# 下載必要的 NLTK 資源
nltk.download('punkt')
nltk.download('popular')

# 定義支持的文件格式及其讀取函數
file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}

def clear_submit():
    """
    清除提交按鈕的狀態
    """
    st.session_state["submit"] = False

@st.cache_data(ttl="2h")
def load_data(uploaded_file):
    """
    加載上傳的數據文件
    """
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"不支持的文件格式：{ext}")
        return None

# 設置頁面配置
st.set_page_config(page_title="LangChain：與 pandas 資料框聊天", page_icon="🦜")
st.title("🦜 LangChain：與 pandas 資料框聊天")

# 文件上傳器
uploaded_file = st.file_uploader(
    "上傳資料文件",
    type=list(file_formats.keys()),
    help="支持各種文件格式",
    on_change=clear_submit,
)

# 當沒有上傳文件時顯示警告
if not uploaded_file:
    st.warning(
        "此應用使用 LangChain 的 `PythonAstREPLTool`，該工具容易受到任意代碼執行的攻擊。請在部署和分享此應用時謹慎使用。"
    )

# 當有文件上傳時，加載數據
if uploaded_file:
    df = load_data(uploaded_file)

# 側邊欄輸入 OpenAI API 金鑰
openai_api_key = st.sidebar.text_input("OpenAI API 金鑰", type="password")

# 清除對話歷史的按鈕
if "messages" not in st.session_state or st.sidebar.button("清除對話歷史"):
    st.session_state["messages"] = [{"role": "assistant", "content": "我能為您做些什麼？"}]

# 顯示對話歷史
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 用戶輸入提示
if prompt := st.chat_input(placeholder="這些數據是關於什麼的？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 如果沒有提供 API 金鑰，提示用戶
    if not openai_api_key:
        st.info("請添加您的 OpenAI API 金鑰以繼續。")
        st.stop()

    # 初始化聊天模型
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo-0613",
        openai_api_key=openai_api_key,
        streaming=True
    )

    # 創建 pandas 資料框代理，允許執行危險代碼
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
        allow_dangerous_code=True  # 允許執行危險代碼
    )

    # 生成回應並顯示
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            # 只傳遞當前的 prompt 字串
            response = pandas_df_agent.run(prompt, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except ValueError as e:
            st.error(f"生成回應時出錯：{e}")
            st.stop()
