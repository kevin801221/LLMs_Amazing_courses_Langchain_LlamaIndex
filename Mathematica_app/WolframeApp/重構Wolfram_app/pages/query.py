import streamlit as st
import json
from core.api import WolframAPI

def show_query_page(api: WolframAPI, auth_manager, username: str):
    """顯示查詢頁面"""
    st.title("Wolfram Alpha API 查詢")
    
    # 定義查詢模板
    templates = {
        "基礎計算": {
            "簡單運算": "2+2",
            "開平方": "sqrt(16)",
            "三角函數": "sin(pi/2)"
        },
        "進階數學": {
            "微分": "derivative of x^2",
            "積分": "integrate x^2 dx",
            "方程求解": "solve x^2 + 2x + 1 = 0"
        },
        "科學計算": {
            "物理常數": "speed of light",
            "化學分子": "water molecule",
            "天文數據": "distance to moon"
        },
        "生活應用": {
            "貨幣換算": "convert 100 USD to EUR",
            "單位轉換": "convert 1 kg to pounds",
            "時間查詢": "time in Tokyo"
        }
    }
    
    # 選擇查詢類型
    category = st.selectbox(
        "選擇查詢類別",
        options=list(templates.keys())
    )
    
    # 選擇具體查詢
    query_type = st.selectbox(
        "選擇查詢類型",
        options=list(templates[category].keys())
    )
    
    # 顯示並允許編輯查詢
    query = st.text_input(
        "編輯查詢內容",
        value=templates[category][query_type]
    )
    
    # 執行查詢
    if st.button("執行查詢"):
        if not query:
            st.warning("請輸入查詢內容")
            return
            
        with st.spinner("正在查詢..."):
            try:
                # 執行 API 查詢
                result = api.query(query)
                formatted_result = api.format_result(result)
                
                # 保存到歷史記錄
                auth_manager.save_query(
                    username,
                    query,
                    json.dumps(formatted_result)
                )
                
                # 顯示結果
                if "error" in formatted_result:
                    st.error(f"查詢錯誤: {formatted_result['error']}")
                else:
                    st.success("查詢成功！")
                    
                    # 顯示結果內容
                    if "pods" in formatted_result:
                        for pod in formatted_result["pods"]:
                            with st.expander(pod["title"]):
                                for content in pod["content"]:
                                    if isinstance(content, str):
                                        if content.startswith("http"):
                                            st.image(content)
                                        else:
                                            st.write(content)
                    else:
                        st.info("無結果返回")
                        
            except Exception as e:
                st.error(f"發生錯誤: {str(e)}")