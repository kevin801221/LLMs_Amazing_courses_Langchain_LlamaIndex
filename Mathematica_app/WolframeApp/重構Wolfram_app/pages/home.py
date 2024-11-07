import streamlit as st
from typing import Tuple

def show_home_page(auth_manager):
    """顯示首頁"""
    st.title("Wolfram Alpha API 工具")
    
    tab1, tab2 = st.tabs(["登入", "註冊"])
    
    with tab1:
        username = st.text_input("用戶名", key="login_username")
        password = st.text_input("密碼", type="password", key="login_password")
        
        if st.button("登入", key="login_button"):
            api_key = auth_manager.login(username, password)
            if api_key:
                return username, api_key
            st.error("登入失敗！")
            
    with tab2:
        reg_username = st.text_input("用戶名", key="reg_username")
        reg_password = st.text_input("密碼", type="password", key="reg_password")
        api_key = st.text_input("Wolfram API Key", type="password", key="reg_api_key")
        
        if st.button("註冊", key="register_button"):
            if auth_manager.register(reg_username, reg_password, api_key):
                st.success("註冊成功！請登入。")
            else:
                st.error("註冊失敗！用戶名可能已存在。")
    
    return None, None