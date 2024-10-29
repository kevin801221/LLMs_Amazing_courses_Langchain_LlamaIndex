# pages/auth.py
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import jwt
from pathlib import Path
import os

# 創建數據庫目錄（如果不存在）
DB_DIR = Path(__file__).parent.parent / "database"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "wolfram_app.db"

class AuthManager:
    def __init__(self):
        # 使用絕對路徑
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.create_user_table()

    def create_user_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    api_key TEXT
                )
            """)

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str, email: str) -> bool:
        try:
            password_hash = self.hash_password(password)
            with self.conn:
                self.conn.execute(
                    "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                    (username, password_hash, email)
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username: str, password: str) -> bool:
        password_hash = self.hash_password(password)
        cursor = self.conn.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        return result and result[0] == password_hash

    def update_last_login(self, username: str):
        with self.conn:
            self.conn.execute(
                "UPDATE users SET last_login = ? WHERE username = ?",
                (datetime.now(), username)
            )

    def save_api_key(self, username: str, api_key: str):
        with self.conn:
            self.conn.execute(
                "UPDATE users SET api_key = ? WHERE username = ?",
                (api_key, username)
            )

def show_auth_page():
    st.title("歡迎使用 Wolfram Alpha API 學習平台")

    # 初始化 AuthManager
    auth_manager = AuthManager()

    # 創建標籤頁
    tab1, tab2 = st.tabs(["登入", "註冊"])

    with tab1:
        st.header("登入")
        login_username = st.text_input("用戶名", key="login_username")
        login_password = st.text_input("密碼", type="password", key="login_password")
        
        if st.button("登入", key="login_button"):
            if auth_manager.verify_user(login_username, login_password):
                auth_manager.update_last_login(login_username)
                st.session_state.user = login_username
                st.success("登入成功！")
                # st.experimental_rerun()
            else:
                st.error("用戶名或密碼錯誤！")

    with tab2:
        st.header("註冊")
        reg_username = st.text_input("用戶名", key="reg_username")
        reg_password = st.text_input("密碼", type="password", key="reg_password")
        reg_password2 = st.text_input("確認密碼", type="password", key="reg_password2")
        reg_email = st.text_input("電子郵件", key="reg_email")
        
        if st.button("註冊", key="register_button"):
            if reg_password != reg_password2:
                st.error("兩次輸入的密碼不一致！")
            elif auth_manager.register_user(reg_username, reg_password, reg_email):
                st.success("註冊成功！請登入。")
            else:
                st.error("註冊失敗！用戶名可能已存在。")

def init_session_state():
    """初始化 session state"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None

def check_auth():
    """檢查用戶是否已登入"""
    init_session_state()
    if not st.session_state.user:
        show_auth_page()
        st.stop()
    return True

if __name__ == "__main__":
    show_auth_page()