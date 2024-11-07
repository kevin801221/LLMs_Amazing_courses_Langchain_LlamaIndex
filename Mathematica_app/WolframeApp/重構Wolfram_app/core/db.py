# core/db.py
import sqlite3
from pathlib import Path

def init_database(db_path: str):
    """初始化數據庫"""
    conn = sqlite3.connect(db_path)
    conn.close()

def get_db_path() -> str:
    """獲取數據庫路徑"""
    db_dir = Path(__file__).parent.parent / "database"
    db_dir.mkdir(exist_ok=True)
    return str(db_dir / "wolfram_app.db")