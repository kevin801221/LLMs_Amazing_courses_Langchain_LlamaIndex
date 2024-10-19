import streamlit as st
import requests
from urllib.parse import quote

def get_llm_api_result(WOLFRAM_APP_ID, query, max_chars=6800):
    BASE_URL = "https://www.wolframalpha.com/api/v1/llm-api"
    
    params = {
        "appid": WOLFRAM_APP_ID,
        "input": query,
        "maxchars": max_chars
    }
    
    url = f"{BASE_URL}?{'&'.join([f'{k}={quote(str(v))}' for k, v in params.items()])}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text, url
    except requests.RequestException as e:
        return str(e), url

def llm_api_page(WOLFRAM_APP_ID, selected_question):
    st.header("Wolfram Alpha LLM API")
    
    query = st.text_input("輸入您的問題:", value=selected_question)
    
    max_chars = st.slider("最大字符數", 100, 10000, 6800)
    
    if st.button("獲取結果"):
        if query:
            result, url = get_llm_api_result(WOLFRAM_APP_ID, query, max_chars)
            st.info(f"使用的 URL: {url}")
            
            st.subheader("API 響應:")
            st.text(result)

            # 嘗試解析和顯示結果的不同部分
            sections = result.split('\n\n')
            for section in sections:
                if ':' in section:
                    title, content = section.split(':', 1)
                    st.subheader(title.strip())
                    if 'image:' in content:
                        image_url = content.strip().split('image:')[1].strip()
                        st.image(image_url)
                    else:
                        st.write(content.strip())
                else:
                    st.write(section)

        else:
            st.warning("請輸入一個問題。")

    st.sidebar.markdown("""
    ### 使用說明
    1. 輸入您的問題或選擇預設問題
    2. 調整最大字符數（預設為 6800）
    3. 點擊 "獲取結果" 按鈕
    4. 查看 API 響應和解析後的結果

    LLM API 提供了設計用於大型語言模型使用的結果。它返回易於處理的計算結果，
    以及指向完整 Wolfram|Alpha 網站結果的鏈接。

    提示：
    - 盡可能使用簡化的關鍵字查詢（例如，將 "法國有多少人口" 轉換為 "法國人口"）
    - API 支持數學計算、日期和單位轉換、公式求解等
    - 結果可能包含圖片 URL，可以直接在支持的環境中顯示
    """)