# Agentic Mesh Project

一個基於生成式AI的自主代理(Autonomous Agent)生態系統框架，讓代理能夠安全地互相發現、協作、互動和交易。

## 目錄
- [概述](#概述)
- [核心特點](#核心特點)
- [系統架構](#系統架構)
- [代理特性](#代理特性)
- [關鍵組件](#關鍵組件)
- [接口規範](#接口規範)
- [安裝指南](#安裝指南)
- [使用說明](#使用說明)
- [信任機制](#信任機制)
- [實作過程](#實作過程)

[前面內容保持不變直到信任機制部分...]

## 實作過程

### 1. 環境設置
```bash
# 建立專案與虛擬環境
mkdir agentic-mesh
cd agentic-mesh
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 .\venv\Scripts\activate  # Windows

# 安裝依賴
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv requests anthropic openai
```

### 2. 配置文件
在專案根目錄創建 `.env` 文件：
```plaintext
APP_NAME="Agentic Mesh"
DEBUG=true
OPENAI_API_KEY="your-openai-api-key"
ANTHROPIC_API_KEY="your-anthropic-api-key"
DEFAULT_LLM_PROVIDER="anthropic"
REGISTRY_HOST="localhost"
REGISTRY_PORT=8000
```

### 3. 實現測試
首先啟動註冊服務：
```bash
python scripts/start_registry.py
```

#### 測試結果
```plaintext
Testing root endpoint...
Response: {'message': 'Agentic Mesh Registry Service'}

Testing agent registration...
Registration response: {'agent_id': 'fe64920c-36e2-495f-9239-93f9015036d8', 'status': 'registered'}

Testing get agent info...
Agent info: {
  "name": "TestAgent",
  "purpose": "Testing",
  "capabilities": ["test", "debug"],
  "endpoint": "http://localhost:8001",
  "owner": "test_user",
  "policies": {
    "max_runtime": "1h"
  },
  "agent_id": "fe64920c-36e2-495f-9239-93f9015036d8",
  "status": "active",
  "registered_at": "2024-11-21T22:16:55.105688",
  "last_active": "2024-11-21T22:16:55.105695"
}
```

### 4. 故障排除指南

#### 模組導入問題
如果遇到 `ModuleNotFoundError: No module named 'src'`，可以：

1. 設置 PYTHONPATH：
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

2. 或創建 `setup.py` 並安裝：
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="agentic-mesh",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "requests"
    ]
)
```

然後執行：
```bash
pip install -e .
```

### 5. 代碼範例
完整的代理測試程序可參見 `scripts/test_intelligent_agent.py`，展示了：
- 代理註冊
- 任務規劃
- 協作查找
- 複雜場景處理

### 6. 開發建議
1. 確保環境變數正確配置
2. 使用非同步操作處理網絡請求
3. 實現錯誤處理和重試機制
4. 添加日誌記錄
5. 規劃擴展性

### 7. 下一步開發計劃
- 實現更複雜的任務規劃邏輯
- 添加代理間的安全通訊
- 開發用戶界面
- 實現性能監控
- 完善文檔

## 貢獻指南
歡迎提交 Pull Requests 來改進這個項目。主要關注：
- 代碼品質
- 測試覆蓋
- 文檔完善
- 新功能提案

