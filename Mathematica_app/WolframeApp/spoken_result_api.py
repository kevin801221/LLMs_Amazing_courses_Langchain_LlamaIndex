import streamlit as st
import requests
from urllib.parse import urlencode

def get_wolfram_spoken_result(WOLFRAM_APP_ID, query, units):
    SPOKEN_RESULT_API_URL = "http://api.wolframalpha.com/v1/spoken"
    params = {
        "appid": WOLFRAM_APP_ID,
        "i": query,
        "units": units
    }
    url = f"{SPOKEN_RESULT_API_URL}?{urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text, url
    except requests.RequestException as e:
        return str(e), url

def spoken_result_api_page(WOLFRAM_APP_ID,selected_question):
    st.header("Wolfram Alpha Spoken Result API")
    query = st.text_input("輸入您的問題 (Spoken Result API):", selected_question)
    units = st.radio("選擇單位系統:", ["metric", "imperial"])

    if st.button("獲取口語化答案"):
        if query:
            answer, url = get_wolfram_spoken_result(WOLFRAM_APP_ID, query, units)
            st.write("口語化答案:", answer)
            st.info(f"使用的 URL: {url}")
        else:
            st.warning("請輸入一個問題。")