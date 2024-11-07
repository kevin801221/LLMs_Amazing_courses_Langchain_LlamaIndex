import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

class AuthManager:
    """認證管理類"""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        """創建必要的數據表"""
        with self.conn:
            # 用戶表
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    api_key TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # 查詢歷史表
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    query TEXT,
                    result TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users (username)
                )
            """)
    
    def hash_password(self, password: str) -> str:
        """密碼哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username: str, password: str, api_key: str) -> bool:
        """用戶註冊"""
        try:
            password_hash = self.hash_password(password)
            with self.conn:
                self.conn.execute(
                    "INSERT INTO users (username, password_hash, api_key) VALUES (?, ?, ?)",
                    (username, password_hash, api_key)
                )
            return True
        except sqlite3.IntegrityError:
            return False
    
    def login(self, username: str, password: str) -> str:
        """用戶登入"""
        password_hash = self.hash_password(password)
        cursor = self.conn.execute(
            "SELECT api_key FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        result = cursor.fetchone()
        
        if result:
            # 更新最後登入時間
            with self.conn:
                self.conn.execute(
                    "UPDATE users SET last_login = ? WHERE username = ?",
                    (datetime.now(), username)
                )
            return result[0]
        return None
    
    def save_query(self, username: str, query: str, result: str):
        """保存查詢歷史"""
        with self.conn:
            self.conn.execute(
                "INSERT INTO query_history (username, query, result) VALUES (?, ?, ?)",
                (username, query, result)
            )
    
    def get_query_history(self, username: str, limit: int = 10) -> list:
        """獲取查詢歷史"""
        cursor = self.conn.execute(
            """
            SELECT query, result, timestamp 
            FROM query_history 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
            """,
            (username, limit)
        )
        return cursor.fetchall()