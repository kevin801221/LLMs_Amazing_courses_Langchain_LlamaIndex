# pages/progress.py

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

class ProgressTracker:
    def __init__(self):
        self.conn = sqlite3.connect('../database/wolfram_app.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # 創建進度表
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    user_id TEXT,
                    challenge_id TEXT,
                    completed_at TIMESTAMP,
                    score INTEGER,
                    time_spent INTEGER,
                    PRIMARY KEY (user_id, challenge_id)
                )
            """)
            
            # 創建活動日誌
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    activity_type TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def log_activity(self, user_id: str, activity_type: str, description: str):
        with self.conn:
            self.conn.execute(
                "INSERT INTO activity_log (user_id, activity_type, description) VALUES (?, ?, ?)",
                (user_id, activity_type, description)
            )

    def get_user_progress(self, user_id: str) -> pd.DataFrame:
        query = """
        SELECT challenge_id, completed_at, score, time_spent
        FROM user_progress
        WHERE user_id = ?
        ORDER BY completed_at DESC
        """
        return pd.read_sql_query(query, self.conn, params=(user_id,))

    def get_recent_activities(self, user_id: str, days: int = 7) -> pd.DataFrame:
        query = """
        SELECT activity_type, description, created_at
        FROM activity_log
        WHERE user_id = ? AND created_at >= ?
        ORDER BY created_at DESC
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        return pd.read_sql_query(query, self.conn, params=(user_id, cutoff_date))

def show_progress_dashboard():
    st.title("學習進度追踪")
    
    if 'user' not in st.session_state:
        st.warning("請先登入！")
        return

    # 初始化進度追踪器
    tracker = ProgressTracker()
    
    # 創建儀表板布局
    col1, col2 = st.columns(2)
    
    with col1:
        show_progress_metrics()
    
    with col2:
        show_achievement_badges()
    
    # 顯示進度圖表
    show_progress_charts(tracker)
    
    # 顯示最近活動
    show_recent_activities(tracker)

def show_progress_metrics():
    st.subheader("學習指標")
    
    # 獲取用戶進度數據
    completed_challenges = 15  # 示例數據
    total_challenges = 30
    total_points = 580
    
    # 顯示進度指標
    st.metric("已完成挑戰", f"{completed_challenges}/{total_challenges}")
    progress = completed_challenges / total_challenges
    st.progress(progress)
    
    # 顯示積分
    st.metric("獲得積分", total_points)
    
    # 顯示學習時間
    st.metric("總學習時間", "12小時")

def show_achievement_badges():
    st.subheader("成就徽章")
    
    badges = {
        "初學者": "🌱",
        "探索者": "🔍",
        "解題高手": "🏆",
        "API大師": "👑"
    }
    
    cols = st.columns(len(badges))
    for col, (badge_name, badge_icon) in zip(cols, badges.items()):
        col.markdown(f"""
            <div style='text-align: center'>
                <div style='font-size: 2em'>{badge_icon}</div>
                <div>{badge_name}</div>
            </div>
        """, unsafe_allow_html=True)

def show_progress_charts(tracker: ProgressTracker):
    st.subheader("學習進度圖表")
    
    # 獲取用戶進度數據
    progress_data = tracker.get_user_progress(st.session_state.user)
    
    # 創建進度趨勢圖
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=progress_data['completed_at'],
        y=progress_data['score'].cumsum(),
        mode='lines+markers',
        name='累計積分'
    ))
    
    fig.update_layout(
        title="積分累積趨勢",
        xaxis_title="日期",
        yaxis_title="積分",
        hovermode='x'
    )
    
    st.plotly_chart(fig)

def show_recent_activities(tracker: ProgressTracker):
    st.subheader("最近活動")
    
    activities = tracker.get_recent_activities(st.session_state.user)
    
    for _, activity in activities.iterrows():
        st.markdown(f"""
        <div style='padding: 10px; margin: 5px 0; background-color: #f0f2f6; border-radius: 5px;'>
            <div style='color: #666; font-size: 0.8em;'>{activity['created_at']}</div>
            <div>{activity['description']}</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_progress_dashboard()