import streamlit as st
import requests
from typing import Dict, Any
import json
import time

def show_parameters_page():
    st.title("⚙️ Wolfram Alpha API 參數設置")
    
    # 使用 container 來組織版面
    with st.container():
        st.markdown("""
        <div class='parameter-intro'>
            了解如何使用不同的參數來自定義你的 API 請求，獲得最佳結果。
        </div>
        """, unsafe_allow_html=True)

    # 創建參數實驗室
    tab1, tab2, tab3 = st.tabs([
        "📊 基本參數配置", 
        "🎨 輸出格式設置",
        "⚡ 高級參數選項"
    ])

    with tab1:
        show_basic_parameters()
    
    with tab2:
        show_format_parameters()
        
    with tab3:
        show_advanced_parameters()

def show_basic_parameters():
    st.markdown("### 基本參數配置")
    
    # API 密鑰輸入
    api_key = st.text_input(
        "API Key:",
        type="password",
        key="param_api_key"
    )

    # 查詢輸入
    query = st.text_input(
        "輸入查詢:",
        value="population of France",
        key="param_query"
    )

    # 單位系統選擇
    units = st.radio(
        "選擇單位系統:",
        ["metric", "imperial"],
        key="param_units"
    )

    # 超時設置
    timeout = st.slider(
        "設置超時時間 (秒):",
        1, 20, 5,
        key="param_timeout"
    )

    if st.button("測試基本參數", key="test_basic_params"):
        test_api_call(api_key, {
            "input": query,
            "units": units,
            "timeout": timeout
        })

def show_format_parameters():
    st.markdown("### 輸出格式設置")
    
    # 格式選擇
    formats = st.multiselect(
        "選擇輸出格式:",
        [
            "plaintext",
            "image",
            "mathml",
            "sound",
            "minput",
            "moutput"
        ],
        default=["plaintext", "image"],
        key="param_formats"
    )

    # 圖片設置
    st.markdown("#### 圖片參數")
    col1, col2 = st.columns(2)
    
    with col1:
        width = st.number_input(
            "圖片寬度 (像素):",
            min_value=100,
            max_value=1000,
            value=500,
            key="param_width"
        )
        
    with col2:
        maxwidth = st.number_input(
            "最大寬度 (像素):",
            min_value=100,
            max_value=1500,
            value=900,
            key="param_maxwidth"
        )

    # 放大倍率
    mag = st.slider(
        "放大倍率:",
        0.1, 2.0, 1.0,
        key="param_mag"
    )

    # 測試按鈕
    if st.button("測試格式參數", key="test_format_params"):
        test_api_call(st.session_state.param_api_key, {
            "format": ",".join(formats),
            "width": width,
            "maxwidth": maxwidth,
            "mag": mag
        })

def show_advanced_parameters():
    st.markdown("### 高級參數設置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scanner 選擇
        scanners = st.multiselect(
            "選擇 Scanner:",
            [
                "Numeric",
                "Data",
                "Conversions",
                "Mathematics"
            ],
            key="param_scanners"
        )
        
        # 假設條件
        assumptions = st.text_input(
            "輸入假設條件:",
            placeholder="例如: DateOrder_**Month.Day.Year--",
            key="param_assumptions"
        )
    
    with col2:
        # Pod 選擇
        pods = st.multiselect(
            "選擇要包含的 Pod:",
            [
                "Result",
                "Properties",
                "Definitions",
                "Solutions"
            ],
            key="param_pods"
        )
        
        # 重計算選項
        reinterpret = st.checkbox(
            "允許重新解釋查詢",
            key="param_reinterpret"
        )

    # 位置參數
    st.markdown("#### 位置參數")
    location_type = st.radio(
        "位置指定方式:",
        ["IP", "經緯度", "城市名"],
        key="param_location_type"
    )

    if location_type == "IP":
        ip = st.text_input(
            "輸入 IP 地址:",
            placeholder="例如: 8.8.8.8",
            key="param_ip"
        )
    elif location_type == "經緯度":
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input(
                "緯度:",
                -90.0, 90.0, 0.0,
                key="param_lat"
            )
        with col2:
            lon = st.number_input(
                "經度:",
                -180.0, 180.0, 0.0,
                key="param_lon"
            )
    else:
        city = st.text_input(
            "輸入城市名:",
            placeholder="例如: Tokyo",
            key="param_city"
        )

    # 測試按鈕
    if st.button("測試高級參數", key="test_advanced_params"):
        params = {
            "scanner": ",".join(scanners) if scanners else None,
            "includepodid": ",".join(pods) if pods else None,
            "assumption": assumptions if assumptions else None,
            "reinterpret": reinterpret
        }
        
        # 添加位置參數
        if location_type == "IP":
            params["ip"] = ip
        elif location_type == "經緯度":
            params["latlong"] = f"{lat},{lon}"
        else:
            params["location"] = city
            
        test_api_call(st.session_state.param_api_key, params)

def test_api_call(api_key: str, params: Dict[str, Any]):
    """執行 API 測試調用"""
    if not api_key:
        st.error("請先輸入 API Key！")
        return
        
    with st.spinner("正在測試參數..."):
        try:
            url = "http://api.wolframalpha.com/v2/query"
            params["appid"] = api_key
            
            # 如果沒有指定查詢，使用默認查詢
            if "input" not in params:
                params["input"] = "pi"
                
            response = requests.get(url, params=params)
            
            # 創建結果展示區
            st.markdown("### 測試結果")
            
            # 顯示請求 URL（隱藏 API key）
            safe_url = response.url.replace(api_key, "YOUR_API_KEY")
            with st.expander("查看請求 URL"):
                st.code(safe_url)
            
            # 顯示狀態碼
            st.write(f"狀態碼: {response.status_code}")
            
            # 如果成功，顯示響應內容
            if response.status_code == 200:
                with st.expander("查看響應內容"):
                    st.code(response.text)
            else:
                st.error("請求失敗！")
                
        except Exception as e:
            st.error(f"發生錯誤: {str(e)}")

# 添加自定義樣式
def local_css():
    st.markdown("""
    <style>
    .parameter-intro {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(45deg, #FF6B6B22, #4ECDC422);
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    local_css()
    show_parameters_page()