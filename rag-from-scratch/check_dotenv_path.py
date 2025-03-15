import os
from dotenv import load_dotenv, find_dotenv

# 打印當前工作目錄
print(f"Current working directory: {os.getcwd()}")

# 查找 .env 文件的路徑
dotenv_path = find_dotenv()
print(f"Found .env file at: {dotenv_path}")

# 檢查是否存在多個 .env 文件
possible_paths = [
    os.path.join(os.getcwd(), '.env'),
    os.path.join(os.path.dirname(os.getcwd()), '.env'),
    os.path.expanduser('~/.env'),
    '/Users/kevinluo/application/LLMs_Amazing_courses_Langchain_LlamaIndex/rag-from-scratch/.env'
]

print("\nChecking for .env files in possible locations:")
for path in possible_paths:
    if os.path.exists(path):
        print(f"- {path} (EXISTS)")
        # 讀取文件的前幾行來確認內容
        with open(path, 'r') as f:
            first_line = f.readline().strip()
            print(f"  First line: {first_line[:15]}...")
    else:
        print(f"- {path} (NOT FOUND)")

# 明確載入指定的 .env 文件
target_env = '/Users/kevinluo/application/LLMs_Amazing_courses_Langchain_LlamaIndex/rag-from-scratch/.env'
print(f"\nExplicitly loading .env from: {target_env}")
load_dotenv(target_env, override=True)

# 檢查載入後的環境變數
langchain_key = os.getenv('LANGCHAIN_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')

print(f"LANGCHAIN_API_KEY: {langchain_key[:10]}..." if langchain_key else "LANGCHAIN_API_KEY: Not found")
print(f"OPENAI_API_KEY: {openai_key[:10]}..." if openai_key else "OPENAI_API_KEY: Not found")
