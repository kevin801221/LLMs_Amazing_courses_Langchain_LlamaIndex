import os
from dotenv import load_dotenv
import json

# 載入 .env 文件
load_dotenv()

# 獲取環境變數
env_vars = {
    'LANGCHAIN_API_KEY': os.getenv('LANGCHAIN_API_KEY'),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'LANGCHAIN_TRACING_V2': os.getenv('LANGCHAIN_TRACING_V2'),
    'LANGCHAIN_ENDPOINT': os.getenv('LANGCHAIN_ENDPOINT')
}

# 打印環境變數（隱藏完整的 API 密鑰，只顯示前10個字符）
safe_env_vars = {
    k: (v[:10] + '...' if v and k.endswith('_KEY') else v) 
    for k, v in env_vars.items()
}

print(json.dumps(safe_env_vars, indent=2))
