import streamlit as st
from dotenv import load_dotenv
import os

# 導入其他 API 頁面
from simple_api import simple_api_page
from short_answers_api import short_answers_api_page
from spoken_result_api import spoken_result_api_page
from full_results_api import full_results_api_page
from fast_query_recognizer_api import fast_query_recognizer_api_page
from llm_api import llm_api_page
load_dotenv()

WOLFRAM_APP_ID = os.getenv("WOLFRAM_ALPHA_APPID")

def main():
    st.sidebar.title("Wolfram Alpha API Demo")
    app_mode = st.sidebar.selectbox("選擇 API 模式", ["Simple API", "Short Answers API", "Spoken Result API", "Full Results API","Fast Query Recognizer API","LLM API"
])
    
    example_questions = {
        "Simple API": [
            "Plot sin(x) + cos(x) from -10 to 10",
            "Compare GDP of USA, China, and Japan",
            "Solar system planets",
            "Chemical structure of caffeine"
        ],
        "Short Answers API": [
            "What is the 1000th digit of pi?",
            "Distance from Earth to Mars today",
            "Population of Tokyo in 2023",
            "Boiling point of ethanol"
        ],
        "Spoken Result API": [
            "How old is the universe?",
            "What is the speed of light in miles per hour?",
            "Who wrote The Great Gatsby?",
            "What is the capital of Brazil?"
        ],
        "Full Results API": [
            "Weather in New York next week",
            "Nutritional information of an apple",
            "Solve x^2 - 4x + 4 = 0",
            "Properties of gold"
        ],
        "Fast Query Recognizer API": [
            "France",
            "2+2",
            "population of Tokyo",
            "distance to Mars",
            "weather in New York"
        ],
        "LLM API": [
            "10 densest elemental metals",
            "population of France",
            "solve x^2 + 3x - 4 = 0",
            "convert 100 km/h to mph",
            "chemical formula of caffeine"
]
    }

    st.sidebar.markdown("### 示例問題")
    if app_mode == "Full Results API":
        category = st.sidebar.selectbox("選擇問題類別", list(example_questions["Full Results API"].keys()))
        selected_question = st.sidebar.selectbox("選擇一個示例問題", example_questions["Full Results API"][category])
    else:
        selected_question = st.sidebar.selectbox("選擇一個示例問題", example_questions[app_mode])

    if app_mode == "Simple API":
        simple_api_page(WOLFRAM_APP_ID, selected_question)
    elif app_mode == "Short Answers API":
        short_answers_api_page(WOLFRAM_APP_ID, selected_question)
    elif app_mode == "Spoken Result API":
        spoken_result_api_page(WOLFRAM_APP_ID, selected_question)
    elif app_mode == "Fast Query Recognizer API":
        fast_query_recognizer_api_page(WOLFRAM_APP_ID, selected_question)
    elif app_mode == "LLM API":
        llm_api_page(WOLFRAM_APP_ID, selected_question)
    else:
        full_results_api_page(WOLFRAM_APP_ID, selected_question)

    st.sidebar.markdown("""
    ### 使用說明
    - 選擇一個 API 模式
    - 選擇問題類別（僅適用於 Full Results API）
    - 從示例問題中選擇，或輸入您自己的問題
    - 對於 Full Results API，您可以選擇多種輸出格式
    - 調整參數以自定義結果
    - 點擊按鈕獲取結果
    - 探索 Wolfram Alpha 在各個領域的強大功能！
    
    ### 應用價值
    - 健康管理：快速獲取健康指標、營養信息和運動建議
    - 商業管理：進行財務計算、分析商業模型和理解管理概念
    - 股票分析：獲取即時股票數據、計算金融指標和比較投資表現
    """)

if __name__ == "__main__":
    main()