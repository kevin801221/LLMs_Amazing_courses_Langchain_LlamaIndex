import streamlit as st
from pathlib import Path

# 原有的導入
from pages.wolfram_full_basic import show_basic_page
from pages.wolfram_parameters import show_parameters_page
from pages.wolfram_practice import show_practice_page

# 新增的導入
from pages.auth import check_auth, show_auth_page
from pages.progress import show_progress_dashboard
from pages.tutorial import show_tutorial_page
from pages.export import show_export_page
from pages.wolfram_llm import show_llm_page  # 新的 LLM 頁面

def main():
    st.set_page_config(
        page_title="Wolfram Full API 教學",
        page_icon="🧮",
        layout="wide"
    )

    # 初始化側邊欄
    st.sidebar.title("🚀 Wolfram API 學習平台")
    st.sidebar.markdown("---")

    # 檢查用戶認證
    if not check_auth():
        return

    # 使用 columns 來創建更好的布局
    menu_col1, menu_col2 = st.sidebar.columns([1, 3])
    
    with menu_col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/20/WolframAlpha_icon.png", width=50)
    
    with menu_col2:
        if st.session_state.get("user"):
            st.markdown(f"### 👤 {st.session_state.user}")
    
    st.sidebar.markdown("---")

    # 主選單分類
    MENU_ITEMS = {
        "基礎課程": {
            "icon": "📚",
            "items": {
                "API 基礎入門": show_basic_page,
                "參數設置教學": show_parameters_page,
                "實戰練習": show_practice_page,
                "LLM API 實驗室": show_llm_page  # 新增的 LLM 頁面
            }
        },
        "學習工具": {
            "icon": "🛠️",
            "items": {
                "學習進度追踪": show_progress_dashboard,
                "互動式教程": show_tutorial_page,
                "成果匯出": show_export_page
            }
        }
    }

    # 選擇主分類
    category = st.sidebar.selectbox(
        "選擇學習領域",
        list(MENU_ITEMS.keys()),
        format_func=lambda x: f"{MENU_ITEMS[x]['icon']} {x}"
    )

    # 選擇子項目
    if category:
        sub_item = st.sidebar.selectbox(
            "選擇功能",
            list(MENU_ITEMS[category]['items'].keys()),
        )

        # 執行選擇的功能
        if sub_item:
            MENU_ITEMS[category]['items'][sub_item]()

    # 側邊欄底部資訊
    st.sidebar.markdown("---")
    
    if st.session_state.get("user"):
        if st.sidebar.button("🚪 登出"):
            st.session_state.clear()
            st.rerun()

    # 版權信息
    st.sidebar.markdown("""
        <div style='position: fixed; bottom: 0; width: 17%;'>
            <p style='text-align: center; color: #666; font-size: 0.8em;'>
                © 2024 Wolfram API Learning Platform
                <br/>Version 1.0.0
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()