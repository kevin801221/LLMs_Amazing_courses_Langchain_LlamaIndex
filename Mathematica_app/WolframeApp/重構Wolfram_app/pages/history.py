import streamlit as st
import json

def show_history_page(auth_manager, username):
    """顯示歷史記錄頁面"""
    st.title("查詢歷史")
    
    history = auth_manager.get_query_history(username)
    
    if not history:
        st.info("暫無查詢記錄")
        return
        
    for query, result, timestamp in history:
        with st.expander(f"{timestamp}: {query}"):
            try:
                result_dict = json.loads(result)
                if "error" in result_dict:
                    st.error(result_dict["error"])
                else:
                    for pod in result_dict.get("pods", []):
                        st.subheader(pod["title"])
                        for content in pod["content"]:
                            if isinstance(content, str):
                                if content.startswith("http"):
                                    st.image(content)
                                else:
                                    st.write(content)
            except json.JSONDecodeError:
                st.error("結果解析錯誤")