# import os
# from langchain.agents import load_tools, initialize_agent
# from langchain.llms import OpenAI
# from langchain.chains.conversation.memory import ConversationBufferMemory
# from dotenv import load_dotenv
# load_dotenv()
# import os
# import streamlit as st

# # 初始化LangChain代理
# def create_agent():
#     llm = OpenAI(temperature=0)
#     tools = load_tools(['wolfram-alpha'])
#     memory = ConversationBufferMemory(memory_key="chat_history")
#     agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=True)
#     return agent

# agent = create_agent()

# # Streamlit 應用界面
# st.title("Streamlit & Wolfram Alpha Integration")

# # 應用選項
# option = st.sidebar.selectbox("選擇應用場景", [
#     "數學計算", "科學與工程計算", "財務計算", "地理與天文", "語言與文本", "健康與生物學", "歷史與文化"
# ])

# # 根據選項選擇不同的應用場景
# if option == "數學計算":
#     st.header("數學計算")
#     equation = st.text_input("輸入一個數學方程式進行計算", "x^2 - 4x + 4 = 0")
#     if st.button("解方程"):
#         result = agent.run(f"Solve {equation}")
#         st.write(f"結果: {result}")

# elif option == "科學與工程計算":
#     st.header("科學與工程計算")
#     calculation = st.text_input("輸入計算（例如: Calculate the energy of a photon with a wavelength of 500 nm）")
#     if st.button("進行計算"):
#         result = agent.run(calculation)
#         st.write(f"結果: {result}")

# elif option == "財務計算":
#     st.header("財務與經濟計算")
#     question = st.text_input("輸入財務問題（例如: What is the exchange rate between USD and EUR?）")
#     if st.button("查詢"):
#         result = agent.run(question)
#         st.write(f"結果: {result}")

# elif option == "地理與天文":
#     st.header("地理與天文計算")
#     location_question = st.text_input("輸入地理問題或天文問題（例如: How far is it from Chicago to Tokyo?）")
#     if st.button("查詢"):
#         result = agent.run(location_question)
#         st.write(f"結果: {result}")

# elif option == "語言與文本":
#     st.header("語言與文本分析")
#     language_query = st.text_input("輸入語言問題（例如: Translate 'hello' into French）")
#     if st.button("查詢"):
#         result = agent.run(language_query)
#         st.write(f"結果: {result}")

# elif option == "健康與生物學":
#     st.header("健康與生物學計算")
#     health_question = st.text_input("輸入健康問題（例如: Calculate BMI for someone who is 180 cm tall and weighs 75 kg）")
#     if st.button("查詢"):
#         result = agent.run(health_question)
#         st.write(f"結果: {result}")

# elif option == "歷史與文化":
#     st.header("歷史與文化")
#     history_question = st.text_input("輸入歷史問題（例如: What happened on July 20, 1969?）")
#     if st.button("查詢"):
#         result = agent.run(history_question)
#         st.write(f"結果: {result}")

# # 集成更多的API工具（例如Flask後端或其他API）

# # 例如，對接一個額外的API
# st.sidebar.markdown("## 更多的API擴展")
# custom_api_url = st.sidebar.text_input("輸入你想集成的API URL")
# if custom_api_url:
#     api_data = st.text_area("輸入API查詢的數據（例如JSON）")
#     if st.sidebar.button("發送請求"):
#         # 在這裡可以對接Flask API，發送HTTP請求
#         import requests
#         response = requests.post(custom_api_url, json=eval(api_data))
#         st.sidebar.write(f"API 回應: {response.json()}")
import wolframalpha 
  
# Taking input from user 
question = input('Question: ') 
  
# App id obtained by the above steps 
app_id = 
  
# Instance of wolf ram alpha  
# client class 
client = wolframalpha.Client(app_id) 
  
# Stores the response from  
# wolf ram alpha 
res = client.query(question) 
  
# Includes only text from the response 
answer = next(res.results).text 
  
print(answer) 