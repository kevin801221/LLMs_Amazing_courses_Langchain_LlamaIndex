import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI
import sys


def test_openai_api():
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, world!"}
            ]
        )
        print("✅ OpenAI API 金鑰有效。")
        return True
    except Exception as e:
        print("❌ OpenAI API 金鑰無效或請求失敗：", str(e))
        return False


def test_qdrant_connection():
    try:
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url:
            print("❌ QDRANT_URL 未設定")
            return False

        if qdrant_api_key:
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            client = QdrantClient(url=qdrant_url)

        # 測試連接
        response = client.get_collections()
        print("✅ 成功連接到 Qdrant。")
        return True
    except Exception as e:
        print("❌ 無法連接到 Qdrant：", str(e))
        return False


def check_env_variables():
    required_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "QDRANT_URL": os.getenv("QDRANT_URL"),
        "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY")
    }

    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value:
            print(f"⚠️ 警告: {var_name} 未設定")
            missing_vars.append(var_name)
        else:
            print(f"✓ {var_name} 已設定")

    return len(missing_vars) == 0


if __name__ == "__main__":
    print("正在檢查環境變數...")
    load_dotenv()

    if not check_env_variables():
        print("\n⚠️ 某些必要的環境變數未設定。請檢查你的 .env 檔案。")
        sys.exit(1)

    print("\n正在測試 OpenAI API 金鑰...")
    openai_success = test_openai_api()

    print("\n正在測試 Qdrant 連接...")
    qdrant_success = test_qdrant_connection()

    if not (openai_success and qdrant_success):
        print("\n❌ 測試未完全通過。請檢查以上錯誤訊息。")
        sys.exit(1)
    else:
        print("\n✅ 所有測試都通過了！")
        sys.exit(0)