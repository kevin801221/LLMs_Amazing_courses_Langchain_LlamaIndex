import streamlit as st
import requests
import json
from urllib.parse import quote
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
WOLFRAM_ALPHA_APPID = os.getenv("WOLFRAM_ALPHA_APPID")

# 默认问题列表
DEFAULT_QUESTIONS = [
    "What is the population of Tokyo?",
    "How far is the Moon from Earth?",
    "What is the boiling point of water in Fahrenheit?",
    "Who wrote 'Pride and Prejudice'?",
    "What is the square root of 256?",
    "How many planets are in our solar system?",
    "What is the capital of Brazil?",
    "What is the chemical formula for water?",
    "Who painted the Mona Lisa?",
    "What is the speed of light in miles per second?"
]

def get_conversation_response(query, conversation_id=None, s=None, host=None):
    if conversation_id and host:
        base_url = f"http://{host}/api/v1/conversation.jsp"
    else:
        base_url = "http://api.wolframalpha.com/v1/conversation.jsp"
    
    encoded_query = quote(query)
    url = f"{base_url}?appid={WOLFRAM_ALPHA_APPID}&i={encoded_query}"
    
    if conversation_id:
        url += f"&conversationid={conversation_id}"
    if s:
        url += f"&s={s}"

    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def conversational_api_content():
    st.title("Wolfram Alpha Conversational API")

    # 使用 session_state 来存储对话历史
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = None
    if 'host' not in st.session_state:
        st.session_state.host = None
    if 's' not in st.session_state:
        st.session_state.s = None

    # 添加默认问题选择器
    selected_question = st.selectbox(
        "Select a default question or type your own:",
        [""] + DEFAULT_QUESTIONS
    )

    query = st.text_input("Enter your query:", value=selected_question)

    if st.button("Ask"):
        if query:
            response = get_conversation_response(
                query, 
                st.session_state.conversation_id, 
                st.session_state.s, 
                st.session_state.host
            )
            if response:
                st.session_state.conversation_history.append(("You", query))
                st.session_state.conversation_history.append(("Wolfram Alpha", response['result']))
                
                # 更新对话参数
                st.session_state.conversation_id = response.get('conversationID')
                st.session_state.host = response.get('host')
                st.session_state.s = response.get('s')
            else:
                st.error("Failed to retrieve response from Wolfram Alpha.")
        else:
            st.warning("Please enter a query or select a default question.")

    # 显示对话历史
    st.subheader("Conversation History")
    for speaker, message in st.session_state.conversation_history:
        st.write(f"**{speaker}:** {message}")

    # 添加一个清除对话历史的按钮
    if st.button("Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.conversation_id = None
        st.session_state.host = None
        st.session_state.s = None
        st.success("Conversation history cleared.")

if __name__ == "__main__":
    conversational_api_content()