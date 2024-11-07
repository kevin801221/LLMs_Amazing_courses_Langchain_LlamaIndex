import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

class WolframFinanceAPI:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = "http://api.wolframalpha.com/v2/query"

    def analyze_finance(self, query: str) -> dict:
        """執行金融分析查詢"""
        params = {
            "appid": self.app_id,
            "input": query,
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
    st.set_page_config(page_title="金融投資小幫手", layout="wide")
    st.title("💰 金融投資小幫手")

    # 初始化 session state
    initialize_session_state()

    # API Key 設置區域
    if not st.session_state.api:
        st.sidebar.header("⚙️ API 設置")
        api_key = st.sidebar.text_input("請輸入 Wolfram API Key:", type="password")
        if api_key:
            st.session_state.wolfram_api_key = api_key
            st.session_state.api = WolframFinanceAPI(api_key)
            st.sidebar.success("✅ API Key 設置成功！")
            st.rerun()

    # 如果沒有設置 API Key，顯示提示訊息
    if not st.session_state.api:
        st.warning("👆 請先在側邊欄設置 Wolfram API Key")
        st.stop()

    # 創建兩個主要標籤頁
    tab1, tab2 = st.tabs(["📊 投資組合分析", "🔍 股票分析"])

    with tab1:
        st.header("投資組合分析")
        
        # 資產配置輸入
        st.subheader("輸入資產配置")
        col1, col2 = st.columns(2)
        
        with col1:
            stocks = st.number_input("股票比例 (%)", 0, 100, 60)
            bonds = st.number_input("債券比例 (%)", 0, 100, 30)
            cash = st.number_input("現金比例 (%)", 0, 100, 10)
        
        with col2:
            investment_amount = st.number_input("投資金額 ($)", 10000, 10000000, 100000)
            risk_tolerance = st.select_slider(
                "風險承受度",
                options=["保守", "穩健", "積極"]
            )

        if st.button("分析投資組合", key="analyze_portfolio"):
            total = stocks + bonds + cash
            if total != 100:
                st.error("❌ 資產配置比例總和必須為100%")
            else:
                # 生成查詢字符串
                query = f"""
                investment portfolio analysis with:
                - {stocks}% stocks (${investment_amount * stocks/100:,.2f})
                - {bonds}% bonds (${investment_amount * bonds/100:,.2f})
                - {cash}% cash (${investment_amount * cash/100:,.2f})
                for {risk_tolerance} risk tolerance
                """
                
                with st.spinner("分析投資組合中..."):
                    result = st.session_state.api.analyze_finance(query)
                    
                    # 顯示圓餅圖
                    fig = go.Figure(data=[go.Pie(
                        labels=['股票', '債券', '現金'],
                        values=[stocks, bonds, cash],
                        hole=.3,
                        marker_colors=['#FF9999', '#66B2FF', '#99FF99']
                    )])
                    fig.update_layout(
                        title="資產配置比例",
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 顯示分析結果
                    if "queryresult" in result and "pods" in result["queryresult"]:
                        st.success("✅ 分析完成！")
                        
                        # 建立分析結果標籤頁
                        result_tabs = st.tabs([
                            "預期報酬",
                            "風險分析",
                            "投資建議"
                        ])
                        
                        for pod in result["queryresult"]["pods"]:
                            # 根據 pod 標題分配到相應的標籤頁
                            if "return" in pod["title"].lower():
                                with result_tabs[0]:
                                    st.subheader(pod["title"])
                                    for subpod in pod["subpods"]:
                                        if subpod.get("plaintext"):
                                            st.info(subpod["plaintext"])
                                        if "img" in subpod:
                                            st.image(subpod["img"]["src"])
                            
                            elif "risk" in pod["title"].lower():
                                with result_tabs[1]:
                                    st.subheader(pod["title"])
                                    for subpod in pod["subpods"]:
                                        if subpod.get("plaintext"):
                                            st.warning(subpod["plaintext"])
                                        if "img" in subpod:
                                            st.image(subpod["img"]["src"])
                            
                            else:
                                with result_tabs[2]:
                                    st.subheader(pod["title"])
                                    for subpod in pod["subpods"]:
                                        if subpod.get("plaintext"):
                                            st.success(subpod["plaintext"])
                                        if "img" in subpod:
                                            st.image(subpod["img"]["src"])
                    else:
                        st.error("❌ 分析過程中發生錯誤，請稍後再試")

    with tab2:
        st.header("股票分析")
        
        col1, col2 = st.columns(2)
        with col1:
            stock_symbol = st.text_input(
                "股票代碼",
                "AAPL",
                help="輸入股票代碼，例如：AAPL（蘋果）、GOOGL（谷歌）、TSLA（特斯拉）"
            )
        
        with col2:
            analysis_type = st.multiselect(
                "分析內容",
                [
                    "基本面分析",
                    "技術分析",
                    "財務比率",
                    "市場表現",
                    "新聞分析"
                ],
                default=["基本面分析", "技術分析"]
            )

        if st.button("開始分析", key="analyze_stock"):
            query = f"""
            {stock_symbol} stock detailed analysis:
            - current price and market data
            - financial ratios and metrics
            - technical indicators
            - market performance metrics
            - recent price movements
            """
            
            with st.spinner(f"正在分析 {stock_symbol} ..."):
                result = st.session_state.api.analyze_finance(query)
                
                if "queryresult" in result and "pods" in result["queryresult"]:
                    st.success(f"✅ {stock_symbol} 分析完成！")
                    
                    # 使用 expander 顯示結果
                    for pod in result["queryresult"]["pods"]:
                        with st.expander(pod["title"], expanded=True):
                            for subpod in pod["subpods"]:
                                if subpod.get("plaintext"):
                                    st.write(subpod["plaintext"])
                                if "img" in subpod:
                                    st.image(subpod["img"]["src"])
                else:
                    st.error(f"❌ 無法獲取 {stock_symbol} 的數據，請確認股票代碼是否正確")

if __name__ == "__main__":
    main()
