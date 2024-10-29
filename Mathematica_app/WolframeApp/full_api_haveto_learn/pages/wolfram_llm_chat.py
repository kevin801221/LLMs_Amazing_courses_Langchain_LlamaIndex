import streamlit as st
import requests
import json
from datetime import datetime
import os
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WolframLLM:
    def __init__(self, app_id):
        self.app_id = app_id
        self.base_url = "https://www.wolframalpha.com/api/v1/llm-api"

    def query(self, input_text, max_chars=6800):
        """發送查詢到 Wolfram LLM API"""
        params = {
            'appid': self.app_id,
            'input': input_text,
            'maxchars': max_chars
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # 處理響應文本
            try:
                return response.json()
            except json.JSONDecodeError:
                # 如果不是 JSON 格式，直接返回文本
                return {"result": response.text}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API 調用錯誤: {str(e)}")
            return {"error": str(e)}

def format_response(response):
    """格式化 API 響應"""
    if isinstance(response, dict):
        if "error" in response:
            return f"錯誤: {response['error']}"
        elif "result" in response:
            return response["result"]
        else:
            # 格式化字典顯示
            return "\n".join(f"{k}: {v}" for k, v in response.items())
    else:
        return str(response)

def show_llm_page():
    """顯示 Wolfram LLM 聊天頁面"""
    st.title("🤖 Wolfram LLM API 實驗室")
    
    # 初始化 session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # 初始化 Wolfram LLM
    wolfram_llm = WolframLLM(os.getenv('WOLFRAM_APP_ID', 'DEMO'))

    # 創建兩列布局
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### 💬 與 Wolfram LLM 對話")
        
        # 聊天記錄顯示區
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        # 用戶輸入
        user_input = st.chat_input("輸入您的問題...")
        
        if user_input:
            # 添加用戶消息到歷史記錄
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            })

            # 顯示用戶消息
            with st.chat_message("user"):
                st.write(user_input)

            # 調用 API 並顯示響應
            with st.chat_message("assistant"):
                with st.spinner('Wolfram 思考中...'):
                    response = wolfram_llm.query(user_input)
                    formatted_response = format_response(response)
                    st.write(formatted_response)
                    # 保存助手回覆到歷史記錄
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": formatted_response,
                        "timestamp": datetime.now().isoformat()
                    })

    with col2:
        st.markdown("### ⚙️ 設置")
        
        # 添加一些控制選項
        max_chars = st.slider("最大響應字符數", 
                            min_value=1000, 
                            max_value=10000, 
                            value=6800,
                            step=1000)

        if st.button("🗑️ 清空對話歷史"):
            st.session_state.chat_history = []
            st.rerun()  # 使用新的 rerun 替換 experimental_rerun

        # 顯示使用統計
        st.markdown("### 📊 使用統計")
        if st.session_state.chat_history:
            total_messages = len(st.session_state.chat_history)
            user_messages = sum(1 for msg in st.session_state.chat_history if msg["role"] == "user")
            st.metric("總消息數", total_messages)
            st.metric("提問次數", user_messages)

        # 添加說明信息
        st.markdown("---")
        st.markdown("""
        #### 💡 使用提示
        - 可以用自然語言提問
        - 支持數學計算和科學查詢
        - 可以詢問多領域知識
        
        #### 🌟 示例問題
        - "計算 π 的前 10 位數字"
        - "地球和月球的距離"
        - "最常見的化學元素有哪些"
        """)

if __name__ == "__main__":
    show_llm_page()