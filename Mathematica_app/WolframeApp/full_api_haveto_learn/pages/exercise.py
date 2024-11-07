'''
這是一個非常完整的 Streamlit 應用程式，提供了多功能的健身健康管理中心。以下是簡要概述：

**主要功能**

1. **運動記錄**: 提供一個表單讓使用者輸入自己的運動記錄，包括活動類型、距離、時間等。
2. **數據分析**: 顯示所有已經記錄的運動數據，提供趨勢圖和統計摘要。
3. **健康目標**: 設置健身目標，計算進度。

**技術細節**

1. **API Key**: 使用 Wolfram Alpha API 查詢，並提供 API Key 選項讓使用者輸入自己的 API Key。
2. **Streamlit**: 使用 Streamlit 框架建立的網站。
3. **Pandas**: 使用 Pandas 處理和顯示數據。
4. **Plotly**: 使用 Plotly 創建趨勢圖。

**使用者體驗**

1. 運動記錄表單簡單易用，提供選項讓使用者選擇活動類型和輸入相關數據。
2. 數據分析頁面顯示所有已經記錄的運動數據，並提供趨勢圖和統計摘要。
3. 健康目標頁面設置健身目標，計算進度。

**潛在改進**

1. **增加活動類型**: 考慮增加更多的活動類型，如高爾夫球、瑜伽等。
2. **提高數據分析功能**: 考慮增加更多的數據分析功能，如時間趨勢圖、地理分布等。
3. **添加社交分享功能**: 考慮添加社交分享功能，讓使用者可以分享自己的運動記錄和進度。

**程式碼細節**

1. 初始化健身管理器：`manager = FitnessManager()`
2. 主標題：`st.title("🏃‍♂️ 運動健康管理中心")`
3. 創建主要標籤頁：`tab1, tab2, tab3 = st.tabs(["📝 記錄運動", "📊 數據分析", "🎯 健康目標"])]`
4. 運動記錄表單：使用 `st.form()` 和 `st.number_input()` 等來創建表單。
5. 數據分析頁面：使用 `pd.DataFrame()` 來處理數據，然後使用 `px.line()` 和 `st.plotly_chart()` 等來顯示趨勢圖和統計摘要。

**程式碼結構**

1. 主程式：`if __name__ == "__main__":`
2. 主標題：`st.title()`
3. 創建主要標籤頁：`tab1, tab2, tab3 = st.tabs()``
4. 運動記錄表單：`with st.form():`
5. 數據分析頁面：`with tab2:`
6. 健康目標頁面：`with tab3:`
'''
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

class WolframAPI:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = "http://api.wolframalpha.com/v2/query"

    def analyze_fitness(self, query: str) -> dict:
        """調用 Wolfram API 進行健身數據分析"""
        params = {
            "appid": self.app_id,
            "input": query,
            "format": "plaintext,image",
            "output": "json"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class FitnessManager:
    def __init__(self):
        # 初始化狀態
        if 'workout_history' not in st.session_state:
            st.session_state.workout_history = []
        if 'wolfram_api' not in st.session_state and 'wolfram_api_key' in st.session_state:
            st.session_state.wolfram_api = WolframAPI(st.session_state.wolfram_api_key)

    def calculate_metrics(self, activity: str, data: dict) -> dict:
        """計算基本健身指標"""
        metrics = {}
        try:
            if activity == "跑步 🏃‍♂️":
                if 'distance' in data and 'time' in data:
                    pace = data['time'] / data['distance']  # min/km
                    speed = (data['distance'] / data['time']) * 60  # km/h
                    calories = data['distance'] * 60  # 粗略估算
                    
                    metrics.update({
                        "配速": f"{pace:.2f} min/km",
                        "速度": f"{speed:.2f} km/h",
                        "消耗卡路里": f"{calories:.0f} kcal"
                    })
                    
            elif activity == "健身 🏋️‍♂️":
                if 'weight' in data and 'reps' in data:
                    volume = data['weight'] * data['reps']
                    calories = volume * 0.1  # 粗略估算
                    
                    metrics.update({
                        "總重量": f"{volume:.1f} kg",
                        "消耗卡路里": f"{calories:.0f} kcal"
                    })
                    
            elif activity == "游泳 🏊‍♂️":
                if 'distance' in data and 'time' in data:
                    speed = (data['distance'] / data['time'])  # m/min
                    calories = data['time'] * 7  # 粗略估算
                    
                    metrics.update({
                        "速度": f"{speed:.2f} m/min",
                        "消耗卡路里": f"{calories:.0f} kcal"
                    })
                    
        except Exception as e:
            metrics["error"] = str(e)
            
        return metrics

def main():
    st.set_page_config(page_title="運動健康管理", layout="wide")
    
    # 添加自定義CSS
    st.markdown("""
        <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .stButton>button {
            width: 100%;
        }
        .workout-form {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 初始化 Wolfram API key
    if 'wolfram_api_key' not in st.session_state:
        st.sidebar.title("⚙️ API 設置")
        api_key = st.sidebar.text_input("輸入 Wolfram API Key:", type="password")
        if api_key:
            st.session_state.wolfram_api_key = api_key
            st.session_state.wolfram_api = WolframAPI(api_key)
            st.sidebar.success("API Key 設置成功！")
            st.rerun()
    
    # 初始化健身管理器
    manager = FitnessManager()
    
    # 主標題
    st.title("🏃‍♂️ 運動健康管理中心")
    st.markdown("記錄你的運動成果，追蹤你的健康狀態")
    
    # 創建主要標籤頁
    tab1, tab2, tab3 = st.tabs(["📝 記錄運動", "📊 數據分析", "🎯 健康目標"])
    
    # 記錄運動標籤頁
    with tab1:
        st.header("運動記錄")
        
        # 選擇運動類型
        activity_types = {
            "跑步 🏃‍♂️": {
                "distance": {"label": "距離 (km)", "min": 0.0, "max": 100.0},
                "time": {"label": "時間 (分鐘)", "min": 0.0, "max": 300.0}
            },
            "健身 🏋️‍♂️": {
                "weight": {"label": "重量 (kg)", "min": 0.0, "max": 500.0},
                "reps": {"label": "次數", "min": 0, "max": 100},
                "sets": {"label": "組數", "min": 0, "max": 20}
            },
            "游泳 🏊‍♂️": {
                "distance": {"label": "距離 (m)", "min": 0.0, "max": 5000.0},
                "time": {"label": "時間 (分鐘)", "min": 0.0, "max": 180.0}
            }
        }
        
        selected_activity = st.selectbox(
            "選擇運動類型",
            list(activity_types.keys())
        )
        
        # 創建運動記錄表單
        with st.form(key="workout_form", clear_on_submit=True):
            st.markdown(f"### {selected_activity} 數據記錄")
            
            # 動態創建輸入欄位
            values = {}
            cols = st.columns(len(activity_types[selected_activity]))
            
            for col, (field, config) in zip(cols, activity_types[selected_activity].items()):
                with col:
                    values[field] = st.number_input(
                        config["label"],
                        min_value=config["min"],
                        max_value=config["max"],
                        step=0.1 if isinstance(config["min"], float) else 1
                    )
            
            # 添加備註
            notes = st.text_area("運動備註", placeholder="記錄今天的運動感受...")
            
            # 提交按鈕
            submitted = st.form_submit_button("記錄運動", use_container_width=True)
            
            if submitted:
                # 計算基本指標
                metrics = manager.calculate_metrics(selected_activity, values)
                
                # 如果有 Wolfram API，進行進階分析
                if hasattr(st.session_state, 'wolfram_api'):
                    query = f"{selected_activity} workout analysis: {str(values)}"
                    advanced_analysis = st.session_state.wolfram_api.analyze_fitness(query)
                else:
                    advanced_analysis = None
                
                # 保存記錄
                workout_record = {
                    "timestamp": datetime.now().isoformat(),
                    "activity": selected_activity,
                    "values": values,
                    "metrics": metrics,
                    "notes": notes,
                    "advanced_analysis": advanced_analysis
                }
                
                st.session_state.workout_history.append(workout_record)
                st.success("運動記錄已保存！")
                
                # 顯示計算結果
                st.markdown("### 📊 運動指標")
                
                # 顯示基本指標
                cols = st.columns(len(metrics))
                for col, (metric, value) in zip(cols, metrics.items()):
                    col.metric(metric, value)
                
                # 如果有進階分析，顯示結果
                if advanced_analysis and "queryresult" in advanced_analysis:
                    st.markdown("### 🔍 進階分析")
                    with st.expander("查看詳細分析", expanded=True):
                        for pod in advanced_analysis["queryresult"].get("pods", []):
                            st.subheader(pod["title"])
                            for subpod in pod["subpods"]:
                                if "plaintext" in subpod:
                                    st.write(subpod["plaintext"])
                                if "img" in subpod:
                                    st.image(subpod["img"]["src"])
    
    # 數據分析標籤頁
    with tab2:
        st.header("運動數據分析")
        
        if not st.session_state.workout_history:
            st.info("還沒有運動記錄，開始記錄你的第一次運動吧！")
        else:
            # 創建數據框
            df = pd.DataFrame([
                {
                    "日期": datetime.fromisoformat(record["timestamp"]).strftime("%Y-%m-%d %H:%M"),
                    "活動": record["activity"],
                    **record["values"],
                    **{f"指標_{k}": v for k, v in record["metrics"].items() if k != "error"},
                    "備註": record["notes"]
                }
                for record in st.session_state.workout_history
            ])
            
            # 數據篩選
            col1, col2 = st.columns(2)
            with col1:
                selected_activity = st.selectbox(
                    "選擇活動類型",
                    ["全部"] + list(df["活動"].unique())
                )
            
            with col2:
                date_range = st.date_input(
                    "選擇日期範圍",
                    value=(
                        datetime.now() - timedelta(days=30),
                        datetime.now()
                    )
                )
            
            # 篩選數據
            if selected_activity != "全部":
                df = df[df["活動"] == selected_activity]
            
            # 顯示趨勢圖
            if not df.empty:
                st.markdown("### 📈 趨勢分析")
                
                # 選擇要分析的指標
                numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
                selected_metric = st.selectbox(
                    "選擇分析指標",
                    numeric_columns
                )
                
                # 創建趨勢圖
                fig = px.line(
                    df,
                    x="日期",
                    y=selected_metric,
                    title=f"{selected_activity} - {selected_metric} 趨勢"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 顯示統計摘要
                st.markdown("### 📊 統計摘要")
                summary = df[selected_metric].describe()
                cols = st.columns(len(summary))
                for col, (stat, value) in zip(cols, summary.items()):
                    col.metric(stat, f"{value:.2f}")
                
                # 顯示詳細數據
                st.markdown("### 📝 詳細記錄")
                st.dataframe(df, hide_index=True)
                
                # 數據導出選項
                if st.button("導出數據"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "下載 CSV 文件",
                        csv,
                        f"workout_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )
    
    # 健康目標標籤頁
    with tab3:
        st.header("健康目標管理")
        
        # 設置目標
        st.markdown("### 🎯 設定目標")
        with st.form("goal_form"):
            goal_type = st.selectbox(
                "目標類型",
                ["每週運動次數", "每月運動時長", "體重目標"]
            )
            
            goal_value = st.number_input(
                "目標數值",
                min_value=0.0
            )
            
            goal_deadline = st.date_input(
                "目標日期",
                min_value=datetime.now().date()
            )
            
            if st.form_submit_button("設定目標"):
                st.success("目標已設定！")
        
        # 顯示進度
        if st.session_state.workout_history:
            st.markdown("### 📊 目標進度")
            
            # 計算一些基本統計
            total_workouts = len(st.session_state.workout_history)
            total_time = sum(
                record["values"].get("time", 0) 
                for record in st.session_state.workout_history
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("總運動次數", total_workouts)
            with col2:
                st.metric("總運動時間", f"{total_time:.0f} 分鐘")

if __name__ == "__main__":
    main()
