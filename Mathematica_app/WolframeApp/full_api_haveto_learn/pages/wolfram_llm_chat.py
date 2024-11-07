'''
以下是對程式碼進行了仔細的解說：

**功能**

* 這是一個 Streamlit 應用程式，用於顯示 Wolfram LLM 聊天頁面。
* 使用者可以與 Wolfram LLM 對話，輸入問題，並收到回答。
* 頁面包含一個聊天區域、輸入框和一些控制選項。

**程式碼結構**

1. `show_llm_page()` 函數：顯示 Wolfram LLM 聊天頁面。
2. `format_response()` 函數：格式化 API 響應。
3. `show_chat_tips()` 函數：顯示使用統計和提示。

**程式碼解說**

1. `st.title("🤖 Wolfram LLM API 實驗室")`：設定頁面標題。
2. `wolfram_llm = WolframLLM(os.getenv('WOLFRAM_APP_ID', 'DEMO'))`：初始化 Wolfram LLM，用於與使用者對話。
3. `st.session_state.chat_history = []`：初始化聊天歷史列表。
4. `with col1:`：創建兩列布局，其中第一列為聊天區域，第二列為控制選項。
5. `chat_container = st.container()`：創建容器用於顯示聊天記錄。
6. `for msg in st.session_state.chat_history:`：遍歷聊天歷史，顯示每個消息。
7. `user_input = st.chat_input("輸入您的問題...")`：提示使用者輸入問題，並添加到聊天歷史。
8. `response = wolfram_llm.query(user_input)`：調用 Wolfram LLM API，用於回答使用者的問題。
9. `formatted_response = format_response(response)`：格式化 API 響應。
10. `st.write(formatted_response)`：顯示格式化的響應。

**控制選項**

1. `max_chars = st.slider("最大響應字符數", min_value=1000, max_value=10000, value=6800, step=1000)`：設置最大響應字符數。
2. `if st.button("🗑️ 清空對話歷史"): st.session_state.chat_history = []`：清空聊天歷史按鈕。

**使用統計**

1. `total_messages = len(st.session_state.chat_history)`：計算總消息數。
2. `user_messages = sum(1 for msg in st.session_state.chat_history if msg["role"] == "user")`：計算用戶消息數。
3. `st.metric("總消息數", total_messages)`：顯示總消息數。
4. `st.metric("提問次數", user_messages)`：顯示提問次數。

**說明信息**

1. `show_chat_tips()`：顯示使用統計和提示。

**結論**

這個程式碼建立了一個 Streamlit 應用程式，用於顯示 Wolfram LLM 聊天頁面。使用者可以與 Wolfram LLM 對話，輸入問題，並收到回答。程式碼包含控制選項、使用統計和說明信息。
'''
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
def show_chat_tips():
    st.markdown("""
    ### 💡 Usage Tips
    - Use natural language for questions
    - Supports mathematical calculations, scientific queries, and general knowledge
    - Can handle complex equations and data analysis
    - Provides step-by-step solutions for math problems
    - Supports unit conversions and comparisons
    
    ### 🌟 Example Questions by Category
    
    #### 📐 Mathematics
    - "Solve the equation x^2 - 4x + 4 = 0"
    - "Calculate the derivative of sin(x)cos(x)"
    - "Find the integral of e^x from 0 to 1"
    - "What is the probability of rolling two sixes with two dice?"
    - "Calculate the area of a circle with radius 5"
    
    #### 🧪 Science & Physics
    - "What is the speed of light in vacuum?"
    - "Compare the size of Jupiter and Saturn"
    - "Explain quantum superposition"
    - "What is the half-life of uranium-235?"
    - "Calculate the force needed to accelerate a 2kg mass at 5 m/s²"
    
    #### 🧬 Chemistry & Biology
    - "Show the molecular structure of caffeine"
    - "What is the pH of vinegar?"
    - "List the noble gases in order of atomic number"
    - "How does DNA replication work?"
    - "What are the products of photosynthesis?"
    
    #### 📊 Data Analysis
    - "Compare GDP of USA and China"
    - "What is the population growth rate of India?"
    - "Show bitcoin price trends over the last year"
    - "Calculate the correlation between height and weight"
    - "What is the average life expectancy worldwide?"
    
    #### 🌍 Geography & Astronomy
    - "What is the distance between Earth and Mars?"
    - "Calculate the time difference between New York and Tokyo"
    - "What is the deepest point in the ocean?"
    - "How many galaxies are in the observable universe?"
    - "Compare the size of the Sun and Alpha Centauri"
    
    #### 💹 Finance & Economics
    - "Convert 1000 USD to EUR"
    - "Calculate compound interest on $1000 at 5% for 10 years"
    - "Compare inflation rates of major economies"
    - "What is the market cap of Apple Inc?"
    - "Calculate monthly mortgage payment for $300000 at 3% for 30 years"
    
    #### 🔧 Engineering & Technology
    - "Calculate the resistance in a parallel circuit"
    - "What is the efficiency of a heat engine?"
    - "Convert 100 horsepower to watts"
    - "Calculate the resonant frequency of an LC circuit"
    - "What is the bandwidth needed for 4K video streaming?"
    
    #### 🎵 Music & Arts
    - "What are the frequencies of musical notes?"
    - "Calculate the golden ratio"
    - "Convert tempo from BPM to milliseconds"
    - "What is the wavelength of middle C?"
    - "Calculate harmony ratios in music"
    
    ### 🔍 Advanced Query Features
    - Add "step by step" for detailed solutions
    - Use "compare" for comparisons
    - Specify units for conversions
    - Add "graph" or "plot" for visualizations
    - Use "explain" for detailed explanations
    
    ### 💪 Power User Tips
    1. **For Mathematical Queries:**
       - Use proper mathematical notation: x^2 for x², sqrt() for square root
       - Specify domains for functions: "solve x^2 + 1 = 0 over complex numbers"
       - Request specific formats: "give result in scientific notation"
    
    2. **For Scientific Queries:**
       - Specify units: "in meters", "in celsius"
       - Ask for comparisons: "compared to", "relative to"
       - Request visualizations: "show graph", "plot trajectory"
    
    3. **For Data Analysis:**
       - Specify time ranges: "over the last 5 years"
       - Request specific metrics: "show median and quartiles"
       - Ask for trends: "show growth rate"
    """)
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
        with st.expander("📚 View Examples and Tips"):
            show_chat_tips()

if __name__ == "__main__":
    show_llm_page()  # 當腳本直接執行時，顯示聊天頁面