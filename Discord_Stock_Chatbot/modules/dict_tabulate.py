from tabulate import tabulate

def dict_to_tabulate(data):
  # 中英轉換表
  header_translation = {
      '日期': 'Date',
      '營收成長率': 'Revenue QoQ',
      'EPS': 'EPS',
      'EPS 季增率': 'EPS QoQ',
      '收盤價': 'Close',
      '每日報酬':'Return',
      '漲跌價差':'Up/Down',
      '標題':'title'
  }
  
  # 轉換 headers 到英文
  en_headers = [header_translation.get(key, key) for key in data.keys()]
  
  # 將資料轉換成 tabulate 表格
  table_data = [list(row) for row in zip(*[data[key] for key in data.keys()])]
  tabulate_data = tabulate(table_data, headers=en_headers, tablefmt="ascii")
  
  return tabulate_data
