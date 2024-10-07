# import requests
# from bs4 import BeautifulSoup
# import datetime as dt

# # 新聞資料
# def stock_news(stock_name="大盤", add_content=True):
#     if stock_name == "大盤":
#         stock_name = "台股 -盤中速報"

#     date_list = []
#     title_list = []
#     content_list = []

#     # 取得 Json 格式資料
#     json_data = requests.get(f'https://ess.api.cnyes.com/ess/api/v1/news/keyword?q={stock_name}&limit=5&page=1').json()

#     # 依照格式擷取資料
#     items = json_data['data']['items']
#     for item in items:
#         # 網址、標題和日期
#         news_id = item["newsId"]
#         title = item["title"]
#         publish_at = item["publishAt"]

#         # 使用 UTC 時間格式
#         utc_time = dt.datetime.utcfromtimestamp(publish_at)
#         formatted_date = utc_time.strftime('%Y-%m-%d')

#         date_list.append(formatted_date)
#         title_list.append(title)

#         # 前往網址擷取內容
#         if add_content:
#             url = requests.get(f'https://news.cnyes.com/news/id/{news_id}').content
#             soup = BeautifulSoup(url, 'html.parser')
#             p_elements = soup.find_all('p')

#             # 提取段落內容
#             p = ''
#             for paragraph in p_elements[4:]:
#                 p += paragraph.get_text()
                
#             content_list.append(p)

#     final_dict = {
#         '日期': date_list,
#         '標題': title_list
#     }
#     if add_content:
#         final_dict['內容'] = content_list

#     return final_dict  

import requests
from bs4 import BeautifulSoup
import datetime as dt

# 新聞資料
def stock_news(stock_name="大盤", limit=5, add_content=True):
    if stock_name == "大盤":
        stock_name = "台股 -盤中速報"

    date_list = []
    title_list = []
    content_list = []

    # 取得 Json 格式資料，將 limit 參數動態化
    json_data = requests.get(f'https://ess.api.cnyes.com/ess/api/v1/news/keyword?q={stock_name}&limit={limit}&page=1').json()

    # 依照格式擷取資料
    items = json_data['data']['items']
    for item in items:
        # 網址、標題和日期
        news_id = item["newsId"]
        title = item["title"]
        publish_at = item["publishAt"]

        # 使用 UTC 時間格式
        utc_time = dt.datetime.utcfromtimestamp(publish_at)
        formatted_date = utc_time.strftime('%Y-%m-%d')

        date_list.append(formatted_date)
        title_list.append(title)

        # 前往網址擷取內容
        if add_content:
            url = requests.get(f'https://news.cnyes.com/news/id/{news_id}').content
            soup = BeautifulSoup(url, 'html.parser')
            p_elements = soup.find_all('p')

            # 提取段落內容
            p = ''
            for paragraph in p_elements[4:]:
                p += paragraph.get_text()

            content_list.append(p)

    final_dict = {
        '日期': date_list,
        '標題': title_list
    }
    if add_content:
        final_dict['內容'] = content_list

    return final_dict
