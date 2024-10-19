import streamlit as st
import requests
from urllib.parse import quote

def get_fast_query_recognizer_result(WOLFRAM_APP_ID, query, mode, output_format):
    BASE_URL = "http://www.wolframalpha.com/queryrecognizer/query.jsp"
    
    params = {
        "appid": WOLFRAM_APP_ID,
        "mode": mode,
        "i": query,
        "output": output_format
    }
    
    url = f"{BASE_URL}?{'&'.join([f'{k}={quote(str(v))}' for k, v in params.items()])}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        if output_format == 'json':
            return response.json(), url
        else:
            return response.text, url
    except requests.RequestException as e:
        return str(e), url

def fast_query_recognizer_api_page(WOLFRAM_APP_ID, selected_question):
    st.header("Wolfram Alpha Fast Query Recognizer API")
    
    query = st.text_input("輸入您的問題:", value=selected_question)
    
    mode = st.radio("選擇模式:", ["Default", "Voice"])
    
    output_format = st.radio("選擇輸出格式:", ["xml", "json"])
    
    if st.button("分析查詢"):
        if query:
            result, url = get_fast_query_recognizer_result(WOLFRAM_APP_ID, query, mode, output_format)
            st.info(f"使用的 URL: {url}")
            
            if isinstance(result, dict):  # JSON result
                st.json(result)
                
                if result.get('query'):
                    query_info = result['query'][0]
                    st.subheader("查詢分析結果:")
                    st.write(f"接受狀態: {'接受' if query_info.get('accepted') == 'true' else '不接受'}")
                    st.write(f"處理時間: {query_info.get('timing', 'N/A')} 毫秒")
                    st.write(f"領域: {query_info.get('domain', 'N/A')}")
                    st.write(f"結果重要性分數: {query_info.get('resultsignificancescore', 'N/A')}")
                    
                    if 'summarybox' in query_info:
                        st.write(f"摘要框路徑: {query_info['summarybox'].get('path', 'N/A')}")
            else:  # XML result
                st.code(result, language='xml')
        else:
            st.warning("請輸入一個問題。")

    st.sidebar.markdown("""
    ### 使用說明
    1. 輸入您的問題或選擇預設問題
    2. 選擇模式:
       - Default: 適用於一般查詢
       - Voice: 針對語音輸入優化
    3. 選擇輸出格式:
       - XML: 原始 XML 格式
       - JSON: 結構化 JSON 格式
    4. 點擊 "分析查詢" 按鈕
    5. 查看結果分析:
       - 接受狀態: 查詢是否被接受
       - 處理時間: API 處理查詢所需時間
       - 領域: 查詢所屬的內容領域
       - 結果重要性分數: 預期結果的相關性評分
       - 摘要框路徑: 預計算摘要的路徑（如果有）
    
    此 API 可用於快速判斷查詢是否適合 Wolfram Alpha 處理，
    並提供初步的查詢分類信息。
    """)