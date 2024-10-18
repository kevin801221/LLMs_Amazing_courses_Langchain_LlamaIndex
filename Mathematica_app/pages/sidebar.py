import sys
import os
import streamlit as st
from streamlit_option_menu import option_menu

# 將 pages 目錄添加到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
pages_dir = os.path.join(current_dir, "pages")
sys.path.append(pages_dir)

from simple_api import simple_api_page
from short_answers_api import short_answers_api_page
from full_results_api import get_full_results, full_results_api_content
from conversational_api import conversational_api_content
# 導入其他 API 頁面

def sidebar():
    with st.sidebar:
        st.title("Wolfram Alpha API Explorer")
        selected = option_menu(
            menu_title=None,
            options=["Simple API", "Short Answers API", "Spoken Results API", "Full Results API","Conversational API"],
            icons=["image", "chat-square-text", "mic", "file-earmark-text","chat-square-text","chat-square-text"],
            menu_icon="cast",
            default_index=0,
        )
    return selected

def main():
    selected = sidebar()

    if selected == "Simple API":
        simple_api_page()
    elif selected == "Short Answers API":
        short_answers_api_page()
    elif selected == "Spoken Results API":
        # 呼叫 Spoken Results API 頁面函數
        pass
    elif selected == "Full Results API":
        full_results_api_content()
    elif selected == "Conversational API":
        conversational_api_content()

if __name__ == "__main__":
    main()

