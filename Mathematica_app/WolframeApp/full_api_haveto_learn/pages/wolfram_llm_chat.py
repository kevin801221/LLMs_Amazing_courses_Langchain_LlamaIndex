import streamlit as st  # 引入Streamlit庫，用於建立Web應用
import requests  # 引入requests庫，用於發送HTTP請求
import json  # 引入JSON處理庫，用於解析和處理JSON數據
from datetime import datetime  # 引入datetime，用於處理日期和時間
import os  # 引入os庫，用於處理環境變數
import logging  # 引入logging庫，用於記錄日誌

# 設置日誌
logging.basicConfig(level=logging.INFO)  # 設定日誌級別為INFO
logger = logging.getLogger(__name__)  # 創建日誌記錄器

class WolframLLM:
    """Wolfram API 處理類"""
    def __init__(self, app_id):
        """初始化Wolfram LLM，設置應用程式ID和基本URL"""
        self.app_id = app_id  # 儲存API應用程式ID
        self.base_url = "https://www.wolframalpha.com/api/v1/llm-api"  # 設定基本URL

    def query(self, input_text, max_chars=6800):
        """發送查詢到 Wolfram LLM API並返回結果"""
        params = {
            'appid': self.app_id,  # 設置應用程式ID
            'input': input_text,  # 設置查詢內容
            'maxchars': max_chars  # 設置最大返回字符數
        }

        try:
            # 發送GET請求
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # 檢查請求是否成功
            
            # 嘗試解析響應為JSON格式
            try:
                return response.json()  # 返回解析後的JSON數據
            except json.JSONDecodeError:
                # 如果響應不是JSON格式，直接返回文本數據
                return {"result": response.text}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API 調用錯誤: {str(e)}")  # 記錄API調用錯誤
            return {"error": str(e)}  # 返回錯誤信息

def format_response(response):
    """格式化 API 響應"""
    if isinstance(response, dict):
        if "error" in response:
            return f"錯誤: {response['error']}"  # 如果有錯誤，返回錯誤信息
        elif "result" in response:
            return response["result"]  # 返回結果
        else:
            # 如果沒有錯誤和結果，格式化字典顯示
            return "\n".join(f"{k}: {v}" for k, v in response.items())
    else:
        return str(response)  # 如果不是字典，直接轉換為字符串

def show_llm_page():
    """顯示 Wolfram LLM 聊天頁面"""
    st.title("🤖 Wolfram LLM API 實驗室")  # 設定頁面標題
    
    # 初始化 session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []  # 如果沒有聊天歷史，初始化為空列表

    # 初始化 Wolfram LLM
    wolfram_llm = WolframLLM(os.getenv('WOLFRAM_APP_ID', 'DEMO'))  # 獲取環境變數中的API ID

    # 創建兩列布局
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### 💬 與 Wolfram LLM 對話")  # 創建聊天區標題
        
        # 聊天記錄顯示區
        chat_container = st.container()  # 創建容器用於顯示聊天記錄
        with chat_container:
            for msg in st.session_state.chat_history:  # 遍歷聊天歷史
                with st.chat_message(msg["role"]):  # 顯示消息角色（用戶或助手）
                    st.write(msg["content"])  # 顯示消息內容

        # 用戶輸入
        user_input = st.chat_input("輸入您的問題...")  # 提示用戶輸入問題
        
        if user_input:
            # 添加用戶消息到歷史記錄
            st.session_state.chat_history.append({
                "role": "user",  # 設置角色為用戶
                "content": user_input,  # 設置消息內容
                "timestamp": datetime.now().isoformat()  # 記錄時間戳
            })

            # 顯示用戶消息
            with st.chat_message("user"):
                st.write(user_input)

            # 調用 API 並顯示響應
            with st.chat_message("assistant"):
                with st.spinner('Wolfram 思考中...'):  # 顯示處理過程的加載動畫
                    response = wolfram_llm.query(user_input)  # 調用Wolfram LLM API
                    formatted_response = format_response(response)  # 格式化響應
                    st.write(formatted_response)  # 顯示格式化的響應
                    # 保存助手回覆到歷史記錄
                    st.session_state.chat_history.append({
                        "role": "assistant",  # 設置角色為助手
                        "content": formatted_response,  # 設置助手的消息內容
                        "timestamp": datetime.now().isoformat()  # 記錄時間戳
                    })

    with col2:
        st.markdown("### ⚙️ 設置")  # 設置區標題
        
        # 添加一些控制選項
        max_chars = st.slider("最大響應字符數", 
                            min_value=1000, 
                            max_value=10000, 
                            value=6800,  # 預設值
                            step=1000)  # 步進值

        if st.button("🗑️ 清空對話歷史"):  # 清空聊天記錄按鈕
            st.session_state.chat_history = []  # 清空聊天歷史
            st.rerun()  # 重新加載頁面以顯示最新狀態

        # 顯示使用統計
        st.markdown("### 📊 使用統計")
        if st.session_state.chat_history:  # 如果有聊天歷史
            total_messages = len(st.session_state.chat_history)  # 計算總消息數
            user_messages = sum(1 for msg in st.session_state.chat_history if msg["role"] == "user")  # 計算用戶消息數
            st.metric("總消息數", total_messages)  # 顯示總消息數
            st.metric("提問次數", user_messages)  # 顯示提問次數

        # 添加說明信息
        st.markdown("---")  # 添加分隔線
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
    show_llm_page()  # 當腳本直接執行時，顯示聊天頁面