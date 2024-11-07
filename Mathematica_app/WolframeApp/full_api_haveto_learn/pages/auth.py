# pages/auth.py
'''
文件概述

一個使用 Streamlit 框架開發的網站，提供登入和註冊功能。它使用 SQLite 資料庫管理用戶資訊。

模塊匯入

你的代碼從以下模塊中匯入了函數：

streamlit：用於建立 Streamlit 網站
sqlite3：用於與 SQLite 資料庫進行交互
hashlib：用於哈希處理密碼
jwt：不使用此模塊（你可能忘記了刪除它）
pathlib和os：用於管理檔案路徑
資料庫設定

你的代碼在建立資料庫前先創建了一個名為 "database" 的目錄，若該目錄不存在則會自動創建。然後，它定義了資料庫的路徑，並使用 sqlite3 連接到該檔案。

認證管理器

你的代碼定義了一個名為 AuthManager 的類別，用於管理用戶註冊、登入和 API 金鑰保存。該類別有一些方法：

__init__: 初始化資料庫連接，並創建用戶表
create_user_table: 創建用戶表，如果已經存在則不做任何事
hash_password: 哈希處理密碼，用於安全儲存密碼
register_user: 註冊新用戶，將用戶名、哈希後的密碼和電子郵件寫入資料庫
verify_user: 驗證登入用戶，檢查用戶名和密碼是否匹配
update_last_login: 更新上次登入時間
save_api_key: 儲存 API 金鑰到用戶的數據中
顯示認證頁面

你的代碼定義了一個名為 show_auth_page 的函數，用於顯示登入和註冊頁面。

在該函數中：

它創建了兩個 Streamlit 標籤頁：登入和註冊
它使用 AuthManager 類別的方法來檢查登入用戶和進行註冊
檢查用戶是否已登入

你的代碼定義了一個名為 check_auth 的函數，用於檢查用戶是否已經登入。如果尚未登入，它會顯示認證頁面並停止後續執行。

主程式入口

此代碼的主程式入口是 show_auth_page 函數，直接呼叫該函數。
'''
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import jwt
from pathlib import Path
import os

# 創建數據庫目錄（如果不存在）
# 定義數據庫文件的路徑，若目錄不存在則創建
DB_DIR = Path(__file__).parent.parent / "database"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "wolfram_app.db"

# 認證管理器類，用於管理用戶註冊、登入和API金鑰保存
class AuthManager:
    def __init__(self):
        # 初始化數據庫連接，使用絕對路徑，避免線程安全性問題
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.create_user_table()

    # 創建用戶表，如果表尚未存在
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

    # 密碼哈希函數，使用 SHA-256 加密
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # 註冊新用戶，將用戶名、密碼哈希和電子郵件存入數據庫
    def register_user(self, username: str, password: str, email: str) -> bool:
        try:
            # 將密碼進行哈希處理
            password_hash = self.hash_password(password)
            with self.conn:
                # 插入用戶數據
                self.conn.execute(
                    "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                    (username, password_hash, email)
                )
            return True  # 註冊成功
        except sqlite3.IntegrityError:
            return False  # 註冊失敗（如用戶名或郵件重複）

    # 驗證用戶登入，檢查用戶名和密碼是否匹配
    def verify_user(self, username: str, password: str) -> bool:
        # 將密碼進行哈希處理，並查詢數據庫中是否有匹配的紀錄
        password_hash = self.hash_password(password)
        cursor = self.conn.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        # 若找到紀錄且哈希值相符則返回 True
        return result and result[0] == password_hash

    # 更新用戶的上次登入時間
    def update_last_login(self, username: str):
        with self.conn:
            self.conn.execute(
                "UPDATE users SET last_login = ? WHERE username = ?",
                (datetime.now(), username)
            )

    # 儲存 API 金鑰到用戶的數據中
    def save_api_key(self, username: str, api_key: str):
        with self.conn:
            self.conn.execute(
                "UPDATE users SET api_key = ? WHERE username = ?",
                (api_key, username)
            )

# 顯示認證頁面，包括登入和註冊選項
def show_auth_page():
    st.title("歡迎使用 Wolfram Alpha API 學習平台")

    # 初始化 AuthManager 用於後續操作
    auth_manager = AuthManager()

    # 創建 Streamlit 標籤頁：登入和註冊
    tab1, tab2 = st.tabs(["登入", "註冊"])

    # 登入頁面
    with tab1:
        st.header("登入")
        # 輸入用戶名和密碼
        login_username = st.text_input("用戶名", key="login_username")
        login_password = st.text_input("密碼", type="password", key="login_password")
        
        # 當按下登入按鈕時執行驗證
        if st.button("登入", key="login_button"):
            # 檢查用戶名和密碼
            if auth_manager.verify_user(login_username, login_password):
                # 登入成功則更新上次登入時間並保存用戶狀態
                auth_manager.update_last_login(login_username)
                st.session_state.user = login_username
                st.success("登入成功！")
                # st.experimental_rerun()
            else:
                # 登入失敗顯示錯誤訊息
                st.error("用戶名或密碼錯誤！")

    # 註冊頁面
    with tab2:
        st.header("註冊")
        # 輸入用戶名、密碼、確認密碼和電子郵件
        reg_username = st.text_input("用戶名", key="reg_username")
        reg_password = st.text_input("密碼", type="password", key="reg_password")
        reg_password2 = st.text_input("確認密碼", type="password", key="reg_password2")
        reg_email = st.text_input("電子郵件", key="reg_email")
        
        # 當按下註冊按鈕時執行註冊
        if st.button("註冊", key="register_button"):
            # 檢查兩次密碼是否一致
            if reg_password != reg_password2:
                st.error("兩次輸入的密碼不一致！")
            elif auth_manager.register_user(reg_username, reg_password, reg_email):
                # 註冊成功顯示提示訊息
                st.success("註冊成功！請登入。")
            else:
                # 註冊失敗顯示錯誤訊息（如用戶名已存在）
                st.error("註冊失敗！用戶名可能已存在。")

# 初始化 session 狀態，用於保存用戶登入狀態和 API 金鑰
def init_session_state():
    """初始化 session state"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None

# 檢查用戶是否已登入，若未登入則顯示認證頁面並停止執行
def check_auth():
    """檢查用戶是否已登入"""
    init_session_state()
    if not st.session_state.user:
        show_auth_page()
        st.stop()  # 停止後續執行，直到登入
    return True

# 主程序入口，顯示認證頁面
if __name__ == "__main__":
    show_auth_page()