# import openai
# from replit import db
# from my_commands.stock_price import stock_price
# from my_commands.stock_news import stock_news
# from my_commands.stock_value import stock_fundamental

# # 建立 GPT 3.5-16k 模型
# def get_reply(messages):
#   try:
#     response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                             messages=messages)
#     reply = response["choices"][0]["message"]["content"]
#   except openai.OpenAIError as err:
#     reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
#   return reply

# # 建立訊息指令(Prompt)
# def generate_content_msg(stock_id):

#   stock_name = db[stock_id]["stock_name"] if stock_id != "大盤" else stock_id

#   price_data = stock_price(stock_id)
#   news_data = stock_news(stock_name)

#   content_msg = '你現在是一位專業的證券分析師, \
#       你會依據以下資料來進行分析並給出一份完整的分析報告:\n'

#   content_msg += f'近期價格資訊:\n {price_data}\n'

#   if stock_id != "大盤":
#     stock_value_data = stock_fundamental(stock_id)
#     content_msg += f'每季營收資訊：\n {stock_value_data}\n'

#   content_msg += f'近期新聞資訊: \n {news_data}\n'
#   content_msg += f'請給我{stock_name}近期的趨勢報告,請以詳細、\
#       嚴謹及專業的角度撰寫此報告,並提及重要的數字, reply in 繁體中文'

#   return content_msg

# # StockGPT
# def stock_gpt(stock_id):
#   content_msg = generate_content_msg(stock_id)

#   msg = [{
#     "role":
#     "system",
#     "content":
#     "你現在是一位專業的證券分析師, 你會統整近期的股價\
#       、基本面、新聞資訊等方面並進行分析, 然後生成一份專業的趨勢分析報告"
#   }, {
#     "role": "user",
#     "content": content_msg
#   }]

#   reply_data = get_reply(msg)

#   return reply_data

import openai
from replit import db
from my_commands.stock_price import stock_price
from my_commands.stock_news import stock_news
from my_commands.stock_value import stock_fundamental
from my_commands.stock_prediction import predict_stock


# 建立 GPT-4 模型
def get_reply(messages):
  try:
    response = openai.ChatCompletion.create(model="gpt-4",
                                            messages=messages,
                                            temperature=0.7,
                                            max_tokens=2000)
    reply = response["choices"][0]["message"]["content"]
  except openai.OpenAIError as err:
    reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
  return reply


import tiktoken

def estimate_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def generate_content_msg(stock_id):
    stock_name = db[stock_id]["stock_name"] if stock_id != "大盤" else stock_id
    price_data = stock_price(stock_id, days=30)  # 只取30天的數據
    news_data = stock_news(stock_name, limit=3)  # 只取3條新聞
    prediction_data = predict_stock(stock_id)

    content_msg = f'''分析 {stock_name}(代碼:{stock_id}):
1. 近期價格: {price_data}
2. 重要新聞: {news_data}
3. 技術指標: {prediction_data}
4. 產業: {db[stock_id]["industry"]}

請提供:
1. 價格走勢摘要
2. 新聞影響分析
3. 技術面分析
4. 產業分析
5. 短期和中期投資建議
6. 風險提示'''

    while estimate_tokens(content_msg) > 7500:  # 留一些餘地給GPT-4的回應
        # 進一步縮減內容...
        price_data = price_data[:len(price_data)//2]
        news_data = news_data[:len(news_data)//2]
        content_msg = f'''分析 {stock_name}(代碼:{stock_id}):
1. 近期價格: {price_data}
2. 重要新聞: {news_data}
3. 技術指標: {prediction_data}

請簡要分析並給出投資建議或風險提示。'''

    return content_msg


# StockGPT
def stock_gpt(stock_id):
  content_msg = generate_content_msg(stock_id)
  msg = [{
    "role":
    "system",
    "content":
    "你是一位經驗豐富的證券分析師,擅長整合各種市場信息並提供深入的股票分析。你的分析應該客觀、全面,同時要考慮到各種可能影響股價的因素。"
  }, {
    "role": "user",
    "content": content_msg
  }]
  reply_data = get_reply(msg)
  return reply_data
