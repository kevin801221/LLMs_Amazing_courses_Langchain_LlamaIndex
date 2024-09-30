import streamlit as st
from PIL import Image
import pandas as pd

# 設置頁面配置
st.set_page_config(page_title="HCMF 汽車市場月報", layout="wide")

# 左側邊欄設置
with st.sidebar:
    # 1. HCMF 汽車市場月報 Logo 和標題
    logo = Image.open("/Users/lo-ai/github_items/信昌明芳/hcmf-vp/Data/element_sources/logo.jpg")  # 使用本地圖片作為 logo
    st.image(logo, width=100)
    st.markdown("<h3 style='font-family:sans-serif; color:#E74C3C;'>HCMF 汽車市場月報</h3>", unsafe_allow_html=True)

    # 2. 選擇報告月份的下拉選單
    report_month = st.selectbox(
        "選擇報告月份", 
        ["2023年11月", "2023年10月", "2023年9月", "2023年8月"],
        key="month_selection"
    )

    st.markdown("<h4 style='font-family:sans-serif;'>MENU</h4>", unsafe_allow_html=True)

    # 3. 中國市場負評分析的下拉選單
    with st.expander("中國市場負評分析", expanded=True):
        st.markdown('<p style="font-family:sans-serif; color:#000;">本月負評總覽</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:sans-serif; color:grey;">信昌VS. 競品比較</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:sans-serif; color:grey;">信昌負評摘要</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:sans-serif; color:grey;">競品負評摘要</p>', unsafe_allow_html=True)

    # 4. 中國市場新車功能介紹的下拉選單
    with st.expander("中國市場新車功能介紹", expanded=False):
        st.markdown('<p style="font-family:sans-serif; color:grey;">整體設計特色摘要</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:sans-serif; color:grey;">個車型設計特色總覽表</p>', unsafe_allow_html=True)

    # 5. 試駕與新科技影片
    with st.expander("試駕與新科技影片", expanded=False):
        st.markdown('<p style="font-family:sans-serif; color:grey;">影片預覽</p>', unsafe_allow_html=True)

    # 6. 新科技/技術新聞
    with st.expander("新科技/技術新聞", expanded=False):
        st.markdown('<p style="font-family:sans-serif; color:grey;">最新技術更新</p>', unsafe_allow_html=True)

# 主畫面內容
st.title("HCMF 汽車市場月報")

# 本月負評總覽的表格
st.markdown("### 本月負評總覽")
data = {
    '系統': ['車頂系統', '門與開閉系統', '機構與機電系統', '舒適開閉系統', '座椅系統', '多個系統'],
    '信昌': [22, 51, 2, 0, 0, 0],
    '競品': [100, 357, 4, 7, 1, 3]
}
df = pd.DataFrame(data)
st.table(df)

# 信昌 VS 競品比較的圖表
st.markdown("### 信昌 VS 競品比較")

# 天窗產品負評比較數據
tianchuang_data = {
    '類別': ['漏水', '炎熱', '異響', '玻璃破碎', '開關故障', '其他'],
    '信昌': [43, 22, 47, 9, 8, 10],
    '競品': [20, 10, 11, 8, 5, 10]
}
df_tianchuang = pd.DataFrame(tianchuang_data)

# 車窗產品負評比較數據
chechuang_data = {
    '類別': ['異響', '升降異常', '按鈕故障', '漏雨', '漏風', '其他'],
    '信昌': [43, 22, 47, 9, 8, 10],
    '競品': [20, 10, 11, 8, 5, 10]
}
df_chechuang = pd.DataFrame(chechuang_data)

# 繪製第一個圖表：天窗產品負評比較
st.markdown("#### 天窗產品負評比較")
st.write("負評總數：信昌 22則，競品 100則")
st.bar_chart(df_tianchuang.set_index('類別'))

# 繪製第二個圖表：車窗產品負評比較
st.markdown("#### 車窗產品負評比較")
st.write("負評總數：信昌 22則，競品 100則")
st.bar_chart(df_chechuang.set_index('類別'))

# 樣式改進建議：可以使用 Streamlit 的自定義 CSS 功能美化 Sidebar 和主畫面顯示
st.markdown("""
    <style>
    /* 自定義左側邊欄樣式 */
    .css-1d391kg { background-color: #f5f5f5; } /* 邊欄背景 */
    .css-hxt7ib { color: #000000; } /* 字體顏色 */
    .st-c1 { padding: 20px; } /* 調整邊欄內部的空隙 */
    
    /* 主頁面標題顏色與字體 */
    .css-10trblm { color: #E74C3C; font-family: sans-serif; }
    
    /* 表格樣式 */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)