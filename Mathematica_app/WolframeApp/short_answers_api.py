#Ref: https://products.wolframalpha.com/short-answers-api/documentation
import streamlit as st
import requests
from urllib.parse import urlencode

def get_wolfram_short_answer(WOLFRAM_APP_ID, query, units, timeout):
    SHORT_ANSWERS_API_URL = "http://api.wolframalpha.com/v1/result"
    params = {
        "appid": WOLFRAM_APP_ID,
        "i": query,
        "units": units,
        "timeout": timeout
    }
    url = f"{SHORT_ANSWERS_API_URL}?{urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text, url
    except requests.RequestException as e:
        return str(e), url

def short_answers_api_page(WOLFRAM_APP_ID,selected_question):
    st.header("Wolfram Alpha Short Answers API")
    query = st.text_input("輸入您的問題 (Short Answers API):", selected_question)
    units = st.radio("選擇單位系統:", ["metric", "imperial"])
    timeout = st.slider("設置超時時間 (秒):", 1, 20, 5)

    if st.button("獲取簡短答案"):
        if query:
            answer, url = get_wolfram_short_answer(WOLFRAM_APP_ID, query, units, timeout)
            st.write("答案:", answer)
            st.info(f"使用的 URL: {url}")
        else:
            st.warning("請輸入一個問題。")
        st.sidebar.markdown("""
    ### 使用說明
    1. 在輸入框中輸入您的問題
    2. 選擇度量單位系統（公制或英制）
    3. 設置 API 請求的超時時間
    4. 點擊 "獲取答案" 按鈕
    5. 查看結果和使用的 URL
    
    例如，嘗試輸入:
    - How far is Los Angeles from New York?
    - What is the population of Tokyo?
    - What is the boiling point of water?
    """)