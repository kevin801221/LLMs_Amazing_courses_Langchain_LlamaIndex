import streamlit as st
import requests
from urllib.parse import quote

def get_wolfram_short_answer(WOLFRAM_APP_ID, query):
    # 基礎 URL
    BASE_URL = "http://api.wolframalpha.com/v1/result"
    
    # URL 編碼查詢字符串
    encoded_query = quote(query)
    
    # 構建完整 URL
    url = f"{BASE_URL}?appid={WOLFRAM_APP_ID}&i={encoded_query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果狀態碼不是 200，會拋出異常
        
        # 如果成功獲取結果
        if response.status_code == 200:
            return response.text, url
        else:
            return f"Error: Status code {response.status_code}", url
            
    except requests.RequestException as e:
        return f"Error: {str(e)}", url

def short_answers_api_page(WOLFRAM_APP_ID, selected_question):
    st.header("Wolfram Alpha Short Answers API")
    
    # 輸入框
    query = st.text_input("輸入您的問題:", value=selected_question)
    
    # 當按下按鈕時獲取結果
    if st.button("獲取答案"):
        if query:
            answer, url = get_wolfram_short_answer(WOLFRAM_APP_ID, query)
            
            # 顯示結果
            if not answer.startswith("Error"):
                st.success("答案：")
                st.write(answer)
            else:
                st.error(answer)
            
            # 顯示使用的 URL（用於調試）
            with st.expander("顯示 API 調用詳情"):
                st.info(f"使用的 URL: {url}")
        else:
            st.warning("請輸入一個問題。")

    # 顯示使用說明
    with st.expander("使用說明"):
        st.markdown("""
        ### 如何使用
        1. 在輸入框中輸入您的問題
        2. 點擊"獲取答案"按鈕
        3. 查看結果
        
        ### 示例問題
        - How far is Los Angeles from New York?
        - What is the population of Tokyo?
        - What is the boiling point of water?
        - Who is the president of France?
        
        ### 注意事項
        - 問題要盡量明確和具體
        - 使用英文提問可能會得到更準確的結果
        - API 返回簡短的文本答案
        """)