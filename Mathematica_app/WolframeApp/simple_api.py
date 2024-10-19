import streamlit as st
import requests
from urllib.parse import urlencode

def get_wolfram_alpha_image(WOLFRAM_APP_ID, query, width):
    SIMPLE_API_URL = "http://api.wolframalpha.com/v1/simple"
    params = {
        "appid": WOLFRAM_APP_ID,
        "i": query,
        "width": width
    }
    url = f"{SIMPLE_API_URL}?{urlencode(params)}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.content, url
    else:
        return None, url

def simple_api_page(WOLFRAM_APP_ID, selected_question):
    st.header("Wolfram Alpha Simple API")
    query = st.text_input("輸入您的問題 (Simple API):", value=selected_question)
    width = st.slider("圖片寬度", 300, 1000, 500)

    if st.button("獲取圖片結果"):
        if query:
            image, url = get_wolfram_alpha_image(WOLFRAM_APP_ID, query, width)
            if image:
                st.image(image, use_column_width=True)
                st.info(f"使用的 URL: {url}")
            else:
                st.error("無法從 Wolfram Alpha 獲取結果。")
                st.info(f"嘗試的 URL: {url}")
        else:
            st.warning("請輸入一個問題。")