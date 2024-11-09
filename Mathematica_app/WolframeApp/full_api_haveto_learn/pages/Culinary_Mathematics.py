'''
文件概述

代碼是一個使用 Streamlit 框架開發的網站，提供幾個功能，包括營養計算、單位換算、食譜調整和食材分析。

模塊匯入

代碼從以下模塊中匯入了函數：

streamlit：用於建立 Streamlit 網站
requests：用於 HTTP 請求
pandas
plotly.express和plotly.graph_objects：用於資料視覺化，但在您的代碼中未被使用
WolframCulinaryAPI類別

您的代碼定義了一個名為 WolframCulinaryAPI 的類別，用於與 Wolfram Alpha API 進行交互。該類別有一個方法：

__init__: 初始化 API 連接，傳入 app_id 參數
query: 執行 Wolfram API 查詢，根據 input_text 參數
初始化 session 狀態

您的代碼定義了一個名為 initialize_session_state 的函數，用於初始化 session 狀態。該函數檢查是否存在 api 和 wolfram_api_key 參數，如果不存在則初始化為 None。

main 函數

您的代碼的主程式入口是 main 函數，定義了以下功能：

設置頁面配置（標題、icon 等）
初始化 session 狀態
在側邊欄顯示 API 設置選項
定義四個主要功能標籤頁：營養計算、單位換算、食譜調整和食材分析
功能標籤頁

每個功能標籤頁都有以下功能：

營養計算：
選擇計算類型
輸入食材和份量
執行營養成分分析（使用 Wolfram API 查詢）
顯示結果
單位換算：
選擇從和到單位
輸入數量
執行換算（使用 Wolfram API 查詢）
顯示結果
食譜調整：
輸入原始配料
設定目標份量
執行食譜調整（使用 Wolfram API 查詢）
顯示結果
食材分析：
選擇分析項目
輸入食材
執行食材分析（使用 Wolfram API 查詢）
顯示結果
Wolfram API 查詢

您的代碼在每個功能標籤頁中都使用了 query 方法來執行 Wolfram API 查詢，根據輸入的參數。
'''
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class WolframCulinaryAPI:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = "http://api.wolframalpha.com/v2/query"

    def query(self, input_text: str) -> dict:
        """執行 Wolfram API 查詢"""
        params = {
            "appid": self.app_id,
            "input": input_text,
            "format": "plaintext,image",
            "output": "json"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def initialize_session_state():
    """初始化 session state"""
    if 'api' not in st.session_state:
        st.session_state.api = None
    if 'wolfram_api_key' not in st.session_state:
        st.session_state.wolfram_api_key = None

def main():
    st.set_page_config(
        page_title="料理數學小幫手",
        page_icon="🍳",
        layout="wide"
    )

    # 初始化 session state
    initialize_session_state()

    # 側邊欄 API 設置
    if not st.session_state.api:
        with st.sidebar:
            st.header("⚙️ API 設置")
            api_key = st.text_input("輸入 Wolfram API Key:", type="password")
            if api_key:
                st.session_state.wolfram_api_key = api_key
                st.session_state.api = WolframCulinaryAPI(api_key)
                st.success("✅ API Key 設置成功！")
                st.rerun()

    # 主標題
    st.title("🍳 料理數學小幫手")

    # 主要功能標籤頁
    tabs = st.tabs([
        "🥗 營養計算",
        "⚖️ 單位換算",
        "📊 食譜調整",
        "🔍 食材分析"
    ])

    # 營養計算標籤頁
    with tabs[0]:
        st.header("營養計算")
        
        nutrition_type = st.selectbox(
            "選擇計算類型",
            [
                "營養成分分析",
                "每日建議攝取量",
                "飲食需求計算",
                "卡路里計算"
            ]
        )
        
        if nutrition_type == "營養成分分析":
            food_item = st.text_input("輸入食材:", "apple")
            amount = st.number_input("份量 (克):", 1, 1000, 100)
            
            if st.button("計算營養成分", key="calc_nutrition"):
                query = f"nutrition facts {amount}g {food_item}"
                with st.spinner("分析中..."):
                    result = st.session_state.api.query(query)
                    if "queryresult" in result:
                        for pod in result["queryresult"].get("pods", []):
                            with st.expander(pod["title"], expanded=True):
                                for subpod in pod["subpods"]:
                                    if subpod.get("plaintext"):
                                        st.write(subpod["plaintext"])
                                    if "img" in subpod:
                                        st.image(subpod["img"]["src"])

    # 單位換算標籤頁
    with tabs[1]:
        st.header("單位換算")
        
        col1, col2 = st.columns(2)
        with col1:
            from_unit = st.text_input("從:", "1 cup")
        with col2:
            to_unit = st.selectbox(
                "換算至:",
                ["milliliters", "grams", "ounces", "tablespoons", "teaspoons"]
            )
        
        if st.button("換算", key="convert_units"):
            query = f"convert {from_unit} to {to_unit}"
            with st.spinner("換算中..."):
                result = st.session_state.api.query(query)
                if "queryresult" in result:
                    st.success("換算結果：")
                    for pod in result["queryresult"].get("pods", []):
                        if "Result" in pod.get("title", ""):
                            for subpod in pod["subpods"]:
                                st.write(subpod.get("plaintext", ""))

    # 食譜調整標籤頁
    with tabs[2]:
        st.header("食譜調整")
        
        col1, col2 = st.columns(2)
        with col1:
            original_servings = st.number_input("原始份量:", 1, 100, 4)
            target_servings = st.number_input("目標份量:", 1, 100, 6)
        
        with col2:
            ingredient = st.text_area(
                "輸入原始配料 (每行一個):",
                "2 cups flour\n1 cup sugar\n3 eggs"
            )
        
        if st.button("調整配量", key="adjust_recipe"):
            st.success("調整後的配料：")
            
            # 逐行處理配料
            for line in ingredient.split('\n'):
                if line.strip():
                    # 解析數量和單位
                    query = f"scale {line} by {target_servings}/{original_servings}"
                    with st.spinner(f"調整 {line} 中..."):
                        result = st.session_state.api.query(query)
                        if "queryresult" in result:
                            for pod in result["queryresult"].get("pods", []):
                                if "Result" in pod.get("title", ""):
                                    for subpod in pod["subpods"]:
                                        st.write(subpod.get("plaintext", ""))

    # 食材分析標籤頁
    with tabs[3]:
        st.header("食材分析")
        
        food_item = st.text_input("輸入食材:", "tomato")
        
        analysis_options = st.multiselect(
            "選擇分析項目",
            [
                "營養成分",
                "熱量",
                "維生素",
                "礦物質",
                "蛋白質",
                "脂肪",
                "碳水化合物"
            ],
            default=["營養成分", "熱量"]
        )
        
        if st.button("分析", key="analyze_food"):
            query = f"""
            {food_item} detailed analysis:
            - nutritional content
            - vitamins and minerals
            - caloric content
            - protein content
            - health benefits
            """
            
            with st.spinner(f"分析 {food_item} 中..."):
                result = st.session_state.api.query(query)
                if "queryresult" in result:
                    for pod in result["queryresult"].get("pods", []):
                        # 根據選擇的分析項目過濾結果
                        if any(option.lower() in pod.get("title", "").lower() 
                              for option in analysis_options):
                            with st.expander(pod["title"], expanded=True):
                                for subpod in pod["subpods"]:
                                    if subpod.get("plaintext"):
                                        st.write(subpod["plaintext"])
                                    if "img" in subpod:
                                        st.image(subpod["img"]["src"])

if __name__ == "__main__":
    main()