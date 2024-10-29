import streamlit as st
import streamlit.components.v1 as components
import time
import random
from datetime import datetime
# 在現有代碼中添加 API 相關功能

import requests
import xml.etree.ElementTree as ET
import json
from typing import Dict, Any

class WolframAPIHandler:
    """Wolfram API 處理類"""
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = "http://api.wolframalpha.com/v2/query"

    def make_query(self, query: str, params: Dict[str, Any] = None) -> dict:
        """執行 API 查詢"""
        default_params = {
            "appid": self.app_id,
            "input": query,
            "format": "plaintext,image",
            "output": "json"
        }
        if params:
            default_params.update(params)
            
        try:
            response = requests.get(self.base_url, params=default_params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

def show_api_demo():
    """API 演示區域"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔮 API 調用演示")

    # API 配置區
    col1, col2 = st.columns([3, 2])
    
    with col1:
        api_key = st.text_input("API Key:", type="password", key="api_key")
        
    with col2:
        output_format = st.selectbox(
            "輸出格式:",
            ["plaintext", "image", "plaintext,image"]
        )

    # 查詢類型選擇
    query_types = {
        "數學計算": {
            "簡單運算": "2+2",
            "方程求解": "solve x^2 + 3x + 2 = 0",
            "微積分": "integrate x^2 from 0 to 1"
        },
        "科學查詢": {
            "物理常數": "speed of light",
            "化學元素": "properties of gold",
            "天文數據": "distance to Mars"
        },
        "生活應用": {
            "天氣查詢": "weather in Tokyo",
            "貨幣轉換": "convert 100 USD to EUR",
            "時間轉換": "time in New York"
        }
    }

    col1, col2 = st.columns([1, 2])
    
    with col1:
        category = st.selectbox("選擇類別:", list(query_types.keys()))
    
    with col2:
        if category:
            subcategory = st.selectbox("選擇查詢:", list(query_types[category].keys()))
            default_query = query_types[category][subcategory]
            query = st.text_input("自定義查詢:", value=default_query)

    # API 調用和結果展示
    if st.button("🚀 執行查詢", key="execute_query"):
        if not api_key:
            st.error("請輸入 API Key!")
            return

        with st.spinner("正在處理請求..."):
            # 創建進度條
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            # 執行 API 調用
            api_handler = WolframAPIHandler(api_key)
            result = api_handler.make_query(
                query,
                {"format": output_format}
            )

            # 清除進度條
            progress_bar.empty()

            # 結果展示區
            st.markdown("#### 📊 查詢結果")
            
            # 創建選項卡顯示不同格式的結果
            result_tabs = st.tabs(["📝 文本", "🖼️ 圖片", "🔍 原始數據"])
            
            with result_tabs[0]:
                try:
                    if "queryresult" in result:
                        for pod in result["queryresult"].get("pods", []):
                            st.subheader(pod.get("title", "未知標題"))
                            for subpod in pod.get("subpods", []):
                                st.write(subpod.get("plaintext", "無文本數據"))
                    else:
                        st.error("未找到有效結果")
                except Exception as e:
                    st.error(f"解析錯誤: {str(e)}")

            with result_tabs[1]:
                try:
                    if "queryresult" in result:
                        for pod in result["queryresult"].get("pods", []):
                            for subpod in pod.get("subpods", []):
                                if "img" in subpod:
                                    st.image(
                                        subpod["img"]["src"],
                                        caption=pod.get("title", ""),
                                        use_column_width=True
                                    )
                except Exception as e:
                    st.error(f"圖片載入錯誤: {str(e)}")

            with result_tabs[2]:
                st.json(result)

            # 添加響應狀態指示器
            if result.get("queryresult", {}).get("success") == True:
                st.success("✅ 查詢成功!")
            else:
                st.error("❌ 查詢失敗!")

    # API 文檔快速參考
    with st.expander("📚 API 文檔快速參考"):
        st.markdown("""
        ### 常用參數說明
        - `format`: 響應格式 (plaintext, image, sound, etc.)
        - `output`: 輸出類型 (json, xml)
        - `units`: 單位系統 (metric, imperial)
        - `timeout`: 超時設置 (默認 5s)
        
        ### 示例代碼
        ```python
        import requests
        
        url = "http://api.wolframalpha.com/v2/query"
        params = {
            "appid": "YOUR_APP_ID",
            "input": "YOUR_QUERY",
            "format": "plaintext,image"
        }
        
        response = requests.get(url, params=params)
        ```
        """)

    st.markdown('</div>', unsafe_allow_html=True)


def create_particle_effect():
    """創建粒子動畫效果"""
    return """
    <div class="particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    <style>
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
    .particle {
        position: absolute;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border-radius: 50%;
        animation: float 8s infinite;
        opacity: 0.5;
    }
    @keyframes float {
        0% { transform: translateY(0px) translateX(0px); }
        50% { transform: translateY(-20px) translateX(20px); }
        100% { transform: translateY(0px) translateX(0px); }
    }
    </style>
    """
def api_lab_section():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔮 API 互動實驗室")
    
    # API 配置
    api_key = st.text_input("輸入你的 API Key:", type="password", key="api_key_lab")
    
    # 查詢類型和對應的預設值
    query_templates = {
        "數學計算": {
            "基礎運算": "2+2",
            "方程求解": "solve x^2 + 5x + 6 = 0",
            "微積分": "integrate sin(x) dx",
            "統計": "mean{1,2,3,4,5,6}"
        },
        "科學查詢": {
            "物理常數": "speed of light",
            "元素性質": "atomic weight of gold",
            "天文數據": "distance to Mars",
            "單位轉換": "convert 1 light year to kilometers"
        },
        "生活應用": {
            "天氣": "weather in Tokyo",
            "匯率": "1 USD in EUR",
            "人口": "population of France",
            "時區": "current time in New York"
        }
    }

    col1, col2 = st.columns(2)
    
    with col1:
        query_type = st.selectbox(
            "選擇查詢類型",
            list(query_templates.keys()),
            key="query_type_lab"  # 添加唯一的 key
        )
        
    with col2:
        if query_type:
            sub_type = st.selectbox(
                "選擇具體查詢",
                list(query_templates[query_type].keys()),
                key="sub_type_lab"  # 添加唯一的 key
            )
            
    # 查詢輸入
    query = st.text_input(
        "自定義你的查詢:",
        value=query_templates[query_type][sub_type],
        key="query_input_lab"  # 添加唯一的 key
    )

    # 格式選項
    format_options = st.multiselect(
        "選擇輸出格式",
        ["plaintext", "image", "mathml"],
        default=["plaintext", "image"],
        key="format_options_lab"  # 添加唯一的 key
    )

    # 執行按鈕
    if st.button("✨ 執行查詢"):
        if not api_key:
            st.error("請輸入 API Key!")
            return
            
        if not query:
            st.warning("請輸入查詢內容!")
            return

        # 顯示加載動畫
        with st.spinner("正在處理請求..."):
            try:
                # 構建 API 請求
                url = "http://api.wolframalpha.com/v2/query"
                params = {
                    "appid": api_key,
                    "input": query,
                    "format": ",".join(format_options),
                    "output": "json"
                }

                # 發送請求
                response = requests.get(url, params=params)
                response.raise_for_status()  # 檢查響應狀態
                result = response.json()

                # 創建結果顯示區
                results_container = st.container()
                
                with results_container:
                    st.success("✅ 查詢成功!")
                    
                    # 顯示結果
                    if "queryresult" in result:
                        queryresult = result["queryresult"]
                        
                        # 創建選項卡顯示不同類型的結果
                        tabs = st.tabs(["📝 文本結果", "🖼️ 圖片結果", "🔍 原始數據"])
                        
                        with tabs[0]:
                            for pod in queryresult.get("pods", []):
                                st.subheader(pod.get("title", ""))
                                for subpod in pod.get("subpods", []):
                                    if "plaintext" in format_options:
                                        st.write(subpod.get("plaintext", ""))
                        
                        with tabs[1]:
                            for pod in queryresult.get("pods", []):
                                for subpod in pod.get("subpods", []):
                                    if "image" in format_options and "img" in subpod:
                                        st.image(
                                            subpod["img"]["src"],
                                            caption=pod.get("title", ""),
                                            use_column_width=True
                                        )
                        
                        with tabs[2]:
                            st.json(result)
                            
                        # 顯示其他相關信息
                        with st.expander("查詢詳情"):
                            st.write(f"耗時: {queryresult.get('timing', 'N/A')} 秒")
                            st.write(f"數據類型: {queryresult.get('datatypes', 'N/A')}")
                            st.write(f"超時: {queryresult.get('timedout', 'N/A')}")
                            
                    else:
                        st.error("未找到結果!")

            except requests.RequestException as e:
                st.error(f"請求錯誤: {str(e)}")
            except json.JSONDecodeError:
                st.error("響應格式錯誤!")
            except Exception as e:
                st.error(f"發生錯誤: {str(e)}")

    # 添加使用說明
    with st.expander("💡 使用說明"):
        st.markdown("""
        #### 如何使用 API 互動實驗室
        1. 輸入你的 API Key
        2. 選擇查詢類型和具體查詢
        3. 自定義你的查詢內容（可選）
        4. 選擇想要的輸出格式
        5. 點擊執行按鈕
        
        #### 支持的查詢類型
        - **數學計算**: 基礎運算、方程求解、微積分等
        - **科學查詢**: 物理常數、元素性質、天文數據等
        - **生活應用**: 天氣、匯率、人口、時區等
        
        #### 輸出格式說明
        - **plaintext**: 純文本結果
        - **image**: 圖片結果（如圖表、圖像等）
        - **mathml**: 數學標記語言（適用於數學公式）
        """)

    st.markdown('</div>', unsafe_allow_html=True)
def show_basic_page():
    # 注入粒子效果
    st.markdown(create_particle_effect(), unsafe_allow_html=True)
    
    # 添加自定義 CSS
    st.markdown("""
    <style>
    .big-font {
        font-size: 2em !important;
        font-weight: bold;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .highlight {
        background: linear-gradient(45deg, #ff6b6b22, #4ecdc422);
        padding: 0.2em 0.4em;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 動態標題
    st.markdown(f'<p class="big-font">🌟 Wolfram Full API 探索之旅</p>', unsafe_allow_html=True)
    
    # 添加即時時鐘
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"### ⏰ 現在時間: {current_time}")

    # 創建動態進度指示器
    progress_placeholder = st.empty()
    progress = 0
    
    # 主要內容區域
    tabs = st.tabs(["🎯 開始探索", "🔮 API 魔法", "🛠️ 實戰練習"])
    
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🚀 開啟你的 API 冒險
        
        讓我們一起探索 Wolfram Full API 的神奇世界！
        
        <div class="highlight">
        選擇你的冒險路徑：
        - 🌱 新手村
        - 🏃 進階道路
        - 🎯 專家之路
        </div>
        """, unsafe_allow_html=True)
        
        # 創建互動式學習路徑選擇器
        learning_path = st.selectbox(
            "選擇你的學習路徑",
            ["🌱 新手入門", "🏃 進階學習", "🎯 專家挑戰"]
        )
        
        # 根據選擇顯示不同內容
        if learning_path == "🌱 新手入門":
            st.info("讓我們從基礎開始！")
            # 添加新手教程內容
            
        elif learning_path == "🏃 進階學習":
            st.warning("準備好接受挑戰了嗎？")
            # 添加進階內容
            
        else:
            st.error("專家級別的挑戰等待著你！")
            # 添加專家內容
            
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        api_lab_section()
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # API 互動實驗室
        st.markdown("### 🔮 API 互動實驗室")
        
        # 創建一個模擬的 API 請求生成器
        col1, col2 = st.columns(2)
        
        with col1:
            query_type = st.selectbox(
                "選擇查詢類型",
                ["數學計算", "科學查詢", "生活應用"]
            )
            
        with col2:
            if query_type == "數學計算":
                st.text_input("輸入算式", value="2+2")
            elif query_type == "科學查詢":
                st.text_input("輸入問題", value="mass of earth")
            else:
                st.text_input("輸入查詢", value="weather in Tokyo")
                
        # 添加動畫效果的執行按鈕
        if st.button("✨ 執行魔法"):
            with st.spinner("施展魔法中..."):
                for i in range(100):
                    time.sleep(0.02)
                    progress_placeholder.progress(i + 1)
                st.success("✨ 魔法完成！")
                
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ API 工具箱")
        
        # 創建一個互動式的工具選擇器
        tool_choice = st.radio(
            "選擇工具",
            ["📝 代碼生成器", "🔍 請求分析器", "🎨 響應格式化器"]
        )
        
        # 根據選擇顯示相應工具
        if tool_choice == "📝 代碼生成器":
            st.code("""
            import requests
            
            def make_query(query):
                return "生成的代碼"
            """)
        elif tool_choice == "🔍 請求分析器":
            st.json({
                "url": "http://api.wolframalpha.com/v2/query",
                "params": {
                    "appid": "YOUR_APP_ID",
                    "input": "example query"
                }
            })
        else:
            st.markdown("格式化工具正在開發中...")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 添加底部導航
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ 上一頁"):
            st.write("導航到上一頁")
            
    with col2:
        st.markdown("### 📍 當前位置：基礎入門")
        
    with col3:
        if st.button("下一頁 ➡️"):
            st.write("導航到下一頁")

if __name__ == "__main__":
    show_basic_page()