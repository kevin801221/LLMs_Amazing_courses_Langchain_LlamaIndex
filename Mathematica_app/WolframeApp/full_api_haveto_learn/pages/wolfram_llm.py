'''
這段程式碼是一個使用 Streamlit 构建的應用程式，用於整合 Wolfram Alpha API 和 Ollama 增強分析（若啟用）。該應用程式提供不同類別的查詢模板，讓用戶可以選擇特定類別並自訂查詢。以下是程式碼的詳細解說：

1. 模組與類別匯入

import streamlit as st
import requests
from typing import Dict, Any
import json
from datetime import datetime

	•	streamlit：用於構建網頁介面。
	•	requests：用於向 API 發送 HTTP 請求。
	•	Dict, Any：用於類型註解。
	•	json：解析和生成 JSON 格式數據。
	•	datetime：獲取當前日期和時間，用於記錄時間戳。

2. Ollama 集成（可選）

# import requests as ollama_requests

	•	這行程式碼被註解掉了，可能是未來用於 Ollama 模組請求功能的代碼。

3. WolframLLMAPI 類

這個類封裝了對 Wolfram Alpha API 的查詢，同時支持啟用 Ollama 增強分析功能。

初始化方法

class WolframLLMAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.wolframalpha.com/api/v1/llm-api"
        
        # Ollama 設置
        self.use_ollama = False
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = "llama3.1:latest"

	•	api_key：存儲 Wolfram Alpha 的 API 金鑰。
	•	base_url：Wolfram Alpha API 的基礎 URL。
	•	use_ollama：是否啟用 Ollama 增強分析。
	•	ollama_url 和 ollama_model：Ollama API 的 URL 和所使用的模型版本。

啟用 Ollama 方法

def enable_ollama(self):
    """啟用 Ollama 集成"""
    self.use_ollama = True
    return self

	•	該方法用於啟用 Ollama 增強分析功能，將 use_ollama 設為 True。

Query 方法

def query(self, input_text: str, max_chars: int = 6800, **kwargs) -> Dict[str, Any]:
    """執行 Wolfram LLM API 查詢"""
    params = {
        "appid": self.api_key,
        "input": input_text,
        "maxchars": str(max_chars)
    }
    params.update(kwargs)
    
    try:
        # Wolfram API 調用
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        wolfram_result = response.text

        # 如果啟用了 Ollama，進行增強處理
        if self.use_ollama:
            return self.enhance_with_ollama(wolfram_result, input_text)
        
        return wolfram_result

    except Exception as e:
        st.error(f"API 調用錯誤: {str(e)}")
        return None

	•	params：包含 Wolfram Alpha API 的查詢參數。
	•	try-except 塊用於捕獲請求中的錯誤。
	•	如果啟用了 Ollama，會調用 enhance_with_ollama 方法對 Wolfram Alpha 的結果進行進一步處理。

使用 Ollama 增強結果方法

def enhance_with_ollama(self, wolfram_result: str, original_query: str) -> Dict[str, Any]:
    """使用 Ollama 增強處理結果"""
    try:
        prompt = f"""Based on this Wolfram Alpha query and result:

Query: {original_query}

Result: {wolfram_result}

Please provide:
1. A clear explanation of the result
2. Key insights and observations
3. Practical applications or implications
4. Any additional context or caveats

Format your response as JSON with these sections.
"""

        # 調用 Ollama API
        ollama_response = requests.post(
            self.ollama_url,
            json={
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }
        )
        ollama_response.raise_for_status()
        
        # 解析 Ollama 響應
        ollama_analysis = ollama_response.json()

        # 組合結果
        enhanced_result = {
            "wolfram_result": wolfram_result,
            "ollama_analysis": ollama_analysis.get("response", ""),
            "query_info": {
                "original_query": original_query,
                "timestamp": datetime.now().isoformat()
            }
        }

        return enhanced_result

    except Exception as e:
        st.warning(f"Ollama 增強處理失敗: {str(e)}")
        return {"wolfram_result": wolfram_result}  # 返回原始結果

	•	prompt：用於請求 Ollama 的格式化文本，包含清晰解釋、關鍵洞察、實際應用等字段。
	•	ollama_response：通過 requests.post 調用 Ollama API，發送 prompt 請求分析。
	•	enhanced_result：包含原始的 Wolfram 結果和 Ollama 分析的增強結果。
	•	捕獲和處理可能的請求錯誤。

4. show_llm_page 函數

這是 Streamlit 的主界面設置，提供 API Key 輸入、Ollama 開關、查詢選項和執行查詢功能。

def show_llm_page():
    st.title("🤖 Wolfram LLM API 智能實驗室")

	•	API Key 輸入：用戶可以輸入 API Key 用於查詢。
	•	Ollama 開關：提供啟用 Ollama 分析的選項。
	•	查詢模板：定義了各種查詢模板（例如數學計算、科學查詢等）。
	•	執行查詢：用戶可以編輯查詢內容並點擊按鈕執行查詢。

5. 其他功能模組

	•	show_quick_query：快速查詢模組，允許用戶快速選擇模板進行查詢。
	•	show_parameter_lab：參數實驗室模組，允許用戶設置額外參數（如最大字符數、單位系統等）進行查詢。
	•	show_batch_processing：批量處理模組，用戶可以輸入多行查詢，一次性批量查詢多個問題。

6. 結果顯示函數

def display_result(result: Dict[str, Any]):
    """顯示 API 響應結果"""
    if not result:
        return
        
    # 顯示查詢解釋
    if "interpretation" in result:
        st.write("📝 解釋:", result["interpretation"])
    
    # 顯示主要結果
    if "result" in result:
        st.success("✨ 結果:")
        st.write(result["result"])
    
    # 顯示圖片
    if "images" in result:
        st.write("🖼️ 圖片:")
        for img_url in result["images"]:
            st.image(img_url)
    
    # 顯示網站連結
    if "website_link" in result:
        st.markdown(f"🔗 [在 Wolfram|Alpha 查看完整結果]({result['website_link']})")

	•	display_result：用於顯示查詢結果，包括解釋、主要結果、圖片和連結。

主函數調用

if __name__ == "__main__":
    show_llm_page()

	•	運行應用程式，顯示主頁面。

這段程式碼構建了一個智能查詢應用，整合 Wolfram Alpha API 查詢和 Ollama 分析功能，為用戶提供了多樣化的查詢體驗，包括數學、科學、數據分析等不同類別的查詢，並且支援批量查詢和高級選項設置，非常適合用於展示和研究各種查詢場景。
'''
import streamlit as st
import requests
from typing import Dict, Any
import json
from datetime import datetime

# Ollama 集成（可選）
# import requests as ollama_requests

class WolframLLMAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.wolframalpha.com/api/v1/llm-api"
        
        # Ollama 設置
        self.use_ollama = False
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = "llama3.1:latest"

    def enable_ollama(self):
        """啟用 Ollama 集成"""
        self.use_ollama = True
        return self

    def query(self, input_text: str, max_chars: int = 6800, **kwargs) -> Dict[str, Any]:
        """執行 Wolfram LLM API 查詢"""
        params = {
            "appid": self.api_key,
            "input": input_text,
            "maxchars": str(max_chars)
        }
        params.update(kwargs)
        
        try:
            # Wolfram API 調用
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            wolfram_result = response.text

            # 如果啟用了 Ollama，進行增強處理
            if self.use_ollama:
                return self.enhance_with_ollama(wolfram_result, input_text)
            
            return wolfram_result

        except Exception as e:
            st.error(f"API 調用錯誤: {str(e)}")
            return None

    def enhance_with_ollama(self, wolfram_result: str, original_query: str) -> Dict[str, Any]:
        """使用 Ollama 增強處理結果"""
        try:
            # 準備 Ollama prompt
            prompt = f"""Based on this Wolfram Alpha query and result:

Query: {original_query}

Result: {wolfram_result}

Please provide:
1. A clear explanation of the result
2. Key insights and observations
3. Practical applications or implications
4. Any additional context or caveats

Format your response as JSON with these sections.
"""

            # 調用 Ollama API
            ollama_response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            ollama_response.raise_for_status()
            
            # 解析 Ollama 響應
            ollama_analysis = ollama_response.json()

            # 組合結果
            enhanced_result = {
                "wolfram_result": wolfram_result,
                "ollama_analysis": ollama_analysis.get("response", ""),
                "query_info": {
                    "original_query": original_query,
                    "timestamp": datetime.now().isoformat()
                }
            }

            return enhanced_result

        except Exception as e:
            st.warning(f"Ollama 增強處理失敗: {str(e)}")
            return {"wolfram_result": wolfram_result}  # 返回原始結果

def show_llm_page():
    st.title("🤖 Wolfram LLM API 智能實驗室")

    # 確保有 API Key
    if "wolfram_api_key" not in st.session_state:
        api_key = st.text_input(
            "請輸入你的 Wolfram API Key:",
            type="password",
            key="api_key_input"
        )
        if api_key:
            st.session_state.wolfram_api_key = api_key
        else:
            st.warning("請先輸入 API Key 才能繼續")
            return

    # Ollama 開關
    use_ollama = st.sidebar.checkbox("啟用 Llama 3.1 增強分析", value=False)
    
    if use_ollama:
        st.sidebar.info("""
        🚀 Llama 3.1 增強功能將：
        - 深度分析 Wolfram 結果
        - 提供關鍵洞察
        - 補充實際應用場景
        """)

    # 選擇查詢類型
    query_templates = {
        "數學計算": {
            "基礎運算": "2+2",
            "方程求解": "solve x^2 + 5x + 6 = 0",
            "微積分": "integrate sin(x) dx",
            "統計": "mean{1,2,3,4,5,6}"
        },
        "科學查詢": {
            "物理常數": "speed of light",
            "化學元素": "properties of gold",
            "分子結構": "caffeine molecular structure",
            "天文數據": "distance to Mars"
        },
        "數據分析": {
            "人口統計": "population of France",
            "經濟數據": "GDP of USA",
            "氣候數據": "temperature in Tokyo",
            "匯率轉換": "convert 100 USD to EUR"
        },
        "進階計算": {
            "特徵值": "eigenvalues {{1,2},{3,4}}",
            "傅立葉變換": "fourier transform of sin(x)",
            "微分方程": "solve y'' + y = 0",
            "概率計算": "probability of 3 heads in 5 coin flips"
        }
    }

    # 選擇查詢類型
    category = st.selectbox(
        "選擇查詢類別",
        list(query_templates.keys())
    )

    if category:
        subcategory = st.selectbox(
            "選擇具體查詢",
            list(query_templates[category].keys())
        )

        # 顯示並允許編輯查詢
        default_query = query_templates[category][subcategory]
        query = st.text_input(
            "編輯查詢內容:",
            value=default_query
        )

        # 高級選項
        with st.expander("高級選項"):
            max_chars = st.number_input(
                "最大返回字符數",
                min_value=100,
                max_value=10000,
                value=6800
            )
            
            units = st.radio(
                "單位系統",
                ["metric", "imperial"]
            )

        # 執行查詢
        if st.button("執行查詢"):
            if not query:
                st.warning("請輸入查詢內容")
                return

            # 顯示 loading 動畫
            with st.spinner("正在處理查詢..."):
                api = WolframLLMAPI(st.session_state.wolfram_api_key)
                if use_ollama:
                    api.enable_ollama()

                result = api.query(
                    query,
                    max_chars=max_chars,
                    units=units
                )

                # 顯示結果
                if result:
                    st.success("查詢成功！")
                    
                    # 檢查是否是增強結果
                    if isinstance(result, dict) and "wolfram_result" in result:
                        # 顯示 Wolfram 結果
                        st.subheader("Wolfram Alpha 結果")
                        st.text(result["wolfram_result"])
                        
                        # 顯示 Llama 分析
                        if "ollama_analysis" in result:
                            st.subheader("Llama 3.1 分析")
                            try:
                                # 嘗試解析 JSON 格式的分析
                                analysis = json.loads(result["ollama_analysis"])
                                
                                if "explanation" in analysis:
                                    st.markdown("### 解釋")
                                    st.write(analysis["explanation"])
                                    
                                if "insights" in analysis:
                                    st.markdown("### 關鍵洞察")
                                    for insight in analysis["insights"]:
                                        st.markdown(f"- {insight}")
                                        
                                if "applications" in analysis:
                                    st.markdown("### 實際應用")
                                    for app in analysis["applications"]:
                                        st.markdown(f"- {app}")
                                        
                                if "context" in analysis:
                                    st.markdown("### 補充說明")
                                    st.write(analysis["context"])
                            
                            except json.JSONDecodeError:
                                # 如果不是 JSON 格式，直接顯示文本
                                st.write(result["ollama_analysis"])
                    else:
                        # 顯示普通結果
                        st.text(result)

                    # 顯示 Wolfram Alpha 網站鏈接
                    st.markdown(f"[在 Wolfram Alpha 網站上查看完整結果](https://www.wolframalpha.com/input?i={query})")

    # 顯示使用說明
    with st.expander("使用說明"):
        st.markdown("""
        ### 查詢優化建議
        1. **簡化查詢**
           - 使用關鍵詞而不是完整句子
           - 例如："France population" 而不是 "What is the population of France"
           
        2. **數學表達式**
           - 使用標準數學符號
           - 支持基礎運算、方程、積分等
           
        3. **單位處理**
           - 可以指定單位系統（公制/英制）
           - 支持單位轉換查詢
           
        4. **錯誤處理**
           - 如果結果不符合預期，嘗試重新表述查詢
           - 檢查數學表達式的語法
        """)

def show_quick_query():
    st.subheader("快速查詢")
    
    # 預設查詢模板
    query_templates = {
        "數學計算": {
            "基礎運算": "2+2",
            "方程求解": "solve x^2 + 5x + 6 = 0",
            "微積分": "integrate sin(x) dx"
        },
        "科學查詢": {
            "物理常數": "speed of light",
            "元素性質": "atomic weight of gold",
            "分子結構": "water molecule structure"
        },
        "數據分析": {
            "人口統計": "population of Tokyo",
            "經濟數據": "GDP of France",
            "氣候數據": "average temperature in New York"
        }
    }

    # 選擇查詢類型
    category = st.selectbox(
        "選擇查詢類別",
        list(query_templates.keys()),
        key="quick_query_category"
    )

    subcategory = st.selectbox(
        "選擇查詢類型",
        list(query_templates[category].keys()),
        key="quick_query_subcategory"
    )

    # 查詢輸入
    query = st.text_input(
        "輸入查詢:",
        value=query_templates[category][subcategory],
        key="quick_query_input"
    )

    if st.button("執行查詢", key="quick_query_button"):
        with st.spinner("正在處理..."):
            api = WolframLLMAPI(st.session_state.wolfram_api_key)
            result = api.query(query)
            display_result(result)

def show_parameter_lab():
    st.subheader("參數實驗室")
    
    # 基本查詢
    query = st.text_input(
        "輸入查詢:",
        value="10 densest elemental metals",
        key="param_query_input"
    )

    # 參數設置
    col1, col2 = st.columns(2)
    
    with col1:
        max_chars = st.number_input(
            "最大字符數",
            min_value=100,
            max_value=10000,
            value=6800,
            step=100,
            key="max_chars_input"
        )
        
        units = st.radio(
            "單位系統",
            ["metric", "imperial"],
            key="units_input"
        )
    
    with col2:
        location = st.text_input(
            "位置（可選）",
            key="location_input"
        )
        
        timezone = st.text_input(
            "時區（可選）",
            key="timezone_input"
        )

    if st.button("執行查詢", key="param_query_button"):
        params = {
            "maxchars": max_chars,
            "units": units
        }
        
        if location:
            params["location"] = location
        if timezone:
            params["timezone"] = timezone
            
        api = WolframLLMAPI(st.session_state.wolfram_api_key)
        result = api.query(query, **params)
        display_result(result)

def show_batch_processing():
    st.subheader("批量處理")
    
    # 輸入多個查詢
    queries = st.text_area(
        "輸入多個查詢（每行一個）:",
        height=200,
        key="batch_queries_input"
    )
    
    max_chars = st.slider(
        "每個查詢的最大字符數",
        100, 10000, 1000,
        key="batch_max_chars"
    )

    if st.button("批量處理", key="batch_process_button"):
        if not queries.strip():
            st.warning("請輸入至少一個查詢")
            return
            
        query_list = [q.strip() for q in queries.split('\n') if q.strip()]
        
        with st.spinner(f"正在處理 {len(query_list)} 個查詢..."):
            api = WolframLLMAPI(st.session_state.wolfram_api_key)
            
            for query in query_list:
                st.markdown(f"### 查詢: {query}")
                result = api.query(query, max_chars=max_chars)
                display_result(result)
                st.markdown("---")

def display_result(result: Dict[str, Any]):
    """顯示 API 響應結果"""
    if not result:
        return
        
    # 顯示查詢解釋
    if "interpretation" in result:
        st.write("📝 解釋:", result["interpretation"])
    
    # 顯示主要結果
    if "result" in result:
        st.success("✨ 結果:")
        st.write(result["result"])
    
    # 顯示圖片
    if "images" in result:
        st.write("🖼️ 圖片:")
        for img_url in result["images"]:
            st.image(img_url)
    
    # 顯示網站連結
    if "website_link" in result:
        st.markdown(f"🔗 [在 Wolfram|Alpha 查看完整結果]({result['website_link']})")

if __name__ == "__main__":
    show_llm_page()