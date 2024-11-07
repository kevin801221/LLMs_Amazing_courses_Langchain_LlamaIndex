# app.py
import streamlit as st
from pathlib import Path
from core.api import WolframAPI
from core.auth import AuthManager
from pages.home import show_home_page
from pages.query import show_query_page
from pages.history import show_history_page

def main():
    """主程序"""
    # 確保數據庫目錄存在
    db_dir = Path("database")
    db_dir.mkdir(exist_ok=True)
    db_path = str(db_dir / "wolfram_app.db")
    
    # 初始化認證管理器
    auth_manager = AuthManager(db_path)
    
    # 檢查登入狀態
    if "user" not in st.session_state:
        username, api_key = show_home_page(auth_manager)
        if username and api_key:
            st.session_state.user = username
            st.session_state.api_key = api_key
            st.rerun()
    else:
        # 側邊欄導航
        st.sidebar.title("導航")
        page = st.sidebar.radio(
            "選擇頁面",
            ["查詢", "歷史記錄", "登出"]
        )
        
        if page == "登出":
            del st.session_state.user
            del st.session_state.api_key
            st.rerun()
        else:
            # 初始化 API
            api = WolframAPI(st.session_state.api_key)
            
            # 顯示選擇的頁面
            if page == "查詢":
                show_query_page(api, auth_manager, st.session_state.user)
            else:
                show_history_page(auth_manager, st.session_state.user)

if __name__ == "__main__":
    main()