import os
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()

# 獲取 APPID
WOLFRAM_ALPHA_APPID = os.getenv("WOLFRAM_ALPHA_APPID")

if not WOLFRAM_ALPHA_APPID:
    raise ValueError("WOLFRAM_ALPHA_APPID not found in .env file")