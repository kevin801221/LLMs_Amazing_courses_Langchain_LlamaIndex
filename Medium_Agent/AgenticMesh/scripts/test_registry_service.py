# scripts/test_registry_service.py
import os
import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import requests
import json

def test_registry():
    base_url = "http://localhost:8000"
    
    # 測試根端點
    print("Testing root endpoint...")
    response = requests.get(base_url)
    print(f"Response: {response.json()}\n")
    
    # 測試代理註冊
    print("Testing agent registration...")
    agent_data = {
        "name": "TestAgent",
        "purpose": "Testing",
        "capabilities": ["test", "debug"],
        "endpoint": "http://localhost:8001",
        "owner": "test_user",
        "policies": {"max_runtime": "1h"}
    }
    
    response = requests.post(
        f"{base_url}/register",
        json=agent_data
    )
    print(f"Registration response: {response.json()}\n")
    
    # 獲取註冊的代理ID
    agent_id = response.json()["agent_id"]
    
    # 測試獲取代理信息
    print("Testing get agent info...")
    response = requests.get(f"{base_url}/agents/{agent_id}")
    print(f"Agent info: {json.dumps(response.json(), indent=2)}\n")
    
    # 測試列出所有代理
    print("Testing list all agents...")
    response = requests.get(f"{base_url}/agents")
    print(f"All agents: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    test_registry()