# scripts/start_registry.py
import os
import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import uvicorn
from src.registry.service import app

def main():
    print(f"Starting registry service at http://localhost:8000")
    uvicorn.run(app, host="localhost", port=8000)

if __name__ == "__main__":
    main()