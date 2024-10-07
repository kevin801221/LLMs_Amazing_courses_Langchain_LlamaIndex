import csv
from replit import db

# 檢查 Replit 資料庫中是否已初始化
if 'initialized' not in db.keys():
  with open('name_df.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # 跳過首行（表頭）

    for row in csvreader:
        index = row[0]
        stock_id = row[1]
        stock_name = row[2]
        industry = row[3]
        
        # 存儲到 Replit 的資料庫中
        db[stock_id] = {'stock_name': stock_name, 
                        'industry': industry}
  
  # 在資料庫中設置 'initialized'，用於標記資料庫已被初始化
  db['initialized'] = True


