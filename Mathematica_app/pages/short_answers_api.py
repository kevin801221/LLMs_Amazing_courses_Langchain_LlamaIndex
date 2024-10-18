import sys
import os
import streamlit as st
import requests
from urllib.parse import quote

# 將專案根目錄添加到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config import WOLFRAM_ALPHA_APPID

def get_short_answer(query):
    encoded_query = quote(query)
    url = f"http://api.wolframalpha.com/v1/result?appid={WOLFRAM_ALPHA_APPID}&i={encoded_query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

def short_answers_api_content():
    st.title("Wolfram Alpha Short Answers API")

    query = st.text_input("Enter your query:")

    if st.button("Get Answer"):
        if query:
            answer = get_short_answer(query)
            if answer:
                st.success(answer)
            else:
                st.error("Failed to retrieve answer from Wolfram Alpha.")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    short_answers_api_content()