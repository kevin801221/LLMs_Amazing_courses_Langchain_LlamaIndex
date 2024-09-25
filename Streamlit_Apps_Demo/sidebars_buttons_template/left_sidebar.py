import streamlit as st
import os
from PIL import Image
# 設置頁面配置
st.set_page_config(page_title="HCMF 汽車市場月報", layout="wide")

# 左側邊欄設置
with st.sidebar:
    # 1. HCMF 汽車市場月報 Logo 和標題
    # st.image("../Data/element_sources/logo.jpg")
    logo = Image.open("/Users/lo-ai/github_items/信昌明芳/hcmf-vp/Data/element_sources/logo.jpg")
    st.image(logo, width=150)
    # st.image("/Users/lo-ai/github_items/信昌明芳/hcmf-vp/Data/element_sources/logo.jpg")
    st.title("HCMF 汽車市場月報")

    # 2. 選擇報告月份的下拉選單
    report_month = st.selectbox(
        "選擇報告月份",
        ["2023年11月", "2023年10月", "2023年9月", "2023年8月"]
    )

    # 3. "Menu" 標題（不具功能）
    st.write("**Menu**")

    # 4. 中國市場負評分析的下拉選單
    with st.expander("中國市場負評分析"):
        page_option = st.radio(
            "",
            ["本月負評總覽", "信昌 ＶＳ 競品比較", "信昌負評摘要", "競品負評摘要"]
        )

    # 5. 中國市場新車功能介紹的下拉選單
    with st.expander("中國市場新車功能介紹"):
        st.radio(
            "設計特色",
            ["整體設計特色摘要", "各車型設計特色總覽表"]
        )

    # 6. 試駕與新科技影片（無子項目）
    st.write("**試駕與新科技影片**")

    # 7. 新科技/技術新聞（無子項目）
    st.write("**新科技/技術新聞**")

# 主介面區域，展示根據 sidebar 選擇的內容
st.title("歡迎來到 HCMF 汽車市場月報")
st.write("這裡將根據您的選擇顯示對應的內容。")

if page_option == "本月負評總覽":
    st.write("您已選擇 **本月負評總覽**")
elif page_option == "信昌 ＶＳ 競品比較":
    st.write("您已選擇 **信昌 ＶＳ 競品比較**")
elif page_option == "信昌負評摘要":
    st.write("您已選擇 **信昌負評摘要**")
elif page_option == "競品負評摘要":
    st.write("您已選擇 **競品負評摘要**")

# 使用本地圖片作為主畫面展示區
image_path = "/Users/lo-ai/github_items/信昌明芳/hcmf-vp/Data/element_sources/image.png"  # 使用本地圖片作為占位圖
if os.path.exists(image_path):
    st.image(image_path, caption="主畫面展示區", use_column_width=True)
else:
    st.write("找不到主畫面圖片，請檢查圖片路徑是否正確。")