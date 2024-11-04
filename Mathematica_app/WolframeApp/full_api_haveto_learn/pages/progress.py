# pages/progress.py

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# 使用相同的數據庫路徑
DB_DIR = Path(__file__).parent.parent / "database"
DB_PATH = DB_DIR / "wolfram_app.db"

# 進度追踪器類，負責跟踪用戶的學習進度和活動
class ProgressTracker:
    def __init__(self):
        # 連接到 SQLite 數據庫
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        # 創建必要的數據表來存儲用戶進度和活動日誌
        with self.conn:
            # 用戶進度表，用來跟踪每個挑戰的完成時間、得分和花費時間
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
            
            # 活動日誌表，用來記錄用戶的活動類型和描述
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
        # 記錄用戶活動，將活動類型和描述插入到活動日誌中
        with self.conn:
            self.conn.execute(
                "INSERT INTO activity_log (user_id, activity_type, description) VALUES (?, ?, ?)",
                (user_id, activity_type, description)
            )

    def get_user_progress(self, user_id: str) -> pd.DataFrame:
        # 獲取用戶的挑戰完成進度數據
        query = """
        SELECT challenge_id, completed_at, score, time_spent
        FROM user_progress
        WHERE user_id = ?
        ORDER BY completed_at DESC
        """
        return pd.read_sql_query(query, self.conn, params=(user_id,))

    def get_recent_activities(self, user_id: str, days: int = 7) -> pd.DataFrame:
        # 獲取用戶最近的活動，預設為過去7天的活動
        query = """
        SELECT activity_type, description, created_at
        FROM activity_log
        WHERE user_id = ? AND created_at >= ?
        ORDER BY created_at DESC
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        return pd.read_sql_query(query, self.conn, params=(user_id, cutoff_date))

# 顯示進度儀表板的主要函數
def show_progress_dashboard():
    st.title("學習進度追踪")
    
    # 檢查用戶是否已登入
    if 'user' not in st.session_state:
        st.warning("請先登入！")
        return

    # 初始化進度追踪器
    tracker = ProgressTracker()
    
    # 創建儀表板的布局
    col1, col2 = st.columns(2)
    
    with col1:
        show_progress_metrics()  # 顯示進度指標
    
    with col2:
        show_achievement_badges()  # 顯示成就徽章
    
    # 顯示進度圖表和最近活動
    show_progress_charts(tracker)
    show_recent_activities(tracker)

def show_progress_metrics():
    # 顯示學習進度的基本指標
    st.subheader("學習指標")
    
    # 示例數據
    completed_challenges = 15
    total_challenges = 30
    total_points = 580
    
    # 顯示已完成挑戰數
    st.metric("已完成挑戰", f"{completed_challenges}/{total_challenges}")
    progress = completed_challenges / total_challenges
    st.progress(progress)  # 顯示完成進度條
    
    # 顯示積分和總學習時間
    st.metric("獲得積分", total_points)
    st.metric("總學習時間", "12小時")

def show_achievement_badges():
    # 顯示用戶成就徽章
    st.subheader("成就徽章")
    
    # 成就徽章和圖標的對應關係
    badges = {
        "初學者": "🌱",
        "探索者": "🔍",
        "解題高手": "🏆",
        "API大師": "👑"
    }
    
    # 以列的方式展示每個徽章
    cols = st.columns(len(badges))
    for col, (badge_name, badge_icon) in zip(cols, badges.items()):
        # 使用 HTML 格式化顯示徽章名稱和圖標
        col.markdown(f"""
            <div style='text-align: center'>
                <div style='font-size: 2em'>{badge_icon}</div>
                <div>{badge_name}</div>
            </div>
        """, unsafe_allow_html=True)

def show_progress_charts(tracker: ProgressTracker):
    # 顯示學習進度的趨勢圖表
    st.subheader("學習進度圖表")
    
    # 獲取用戶進度數據
    progress_data = tracker.get_user_progress(st.session_state.user)
    
    # 創建累計積分的折線圖
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=progress_data['completed_at'],
        y=progress_data['score'].cumsum(),
        mode='lines+markers',
        name='累計積分'
    ))
    
    # 配置圖表的標題和軸標籤
    fig.update_layout(
        title="積分累積趨勢",
        xaxis_title="日期",
        yaxis_title="積分",
        hovermode='x'
    )
    
    # 在 Streamlit 中顯示圖表
    st.plotly_chart(fig)

def show_recent_activities(tracker: ProgressTracker):
    # 顯示用戶的最近活動
    st.subheader("最近活動")
    
    # 獲取最近活動數據
    activities = tracker.get_recent_activities(st.session_state.user)
    
    # 使用 HTML 格式化顯示每個活動項目
    for _, activity in activities.iterrows():
        st.markdown(f"""
        <div style='padding: 10px; margin: 5px 0; background-color: #f0f2f6; border-radius: 5px;'>
            <div style='color: #666; font-size: 0.8em;'>{activity['created_at']}</div>
            <div>{activity['description']}</div>
        </div>
        """, unsafe_allow_html=True)

# 主程序入口，顯示進度儀表板
if __name__ == "__main__":
    show_progress_dashboard()