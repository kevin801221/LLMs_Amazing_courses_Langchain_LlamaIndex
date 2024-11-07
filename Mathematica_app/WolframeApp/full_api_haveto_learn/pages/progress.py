import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import random

# 定義數據庫路徑
DB_DIR = Path(__file__).parent.parent / "database"
DB_DIR.mkdir(exist_ok=True)  # 確保數據庫目錄存在
DB_PATH = DB_DIR / "wolfram_app.db"


class ProgressTracker:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # 用戶進度表
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_progress (
                    user_id TEXT,
                    challenge_id TEXT,
                    completed_at TIMESTAMP,
                    score INTEGER,
                    time_spent INTEGER,
                    category TEXT,
                    difficulty TEXT,
                    PRIMARY KEY (user_id, challenge_id)
                )
            """
            )

            # 活動日誌表
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    activity_type TEXT,
                    description TEXT,
                    points INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # 學習目標表
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS learning_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    goal_type TEXT,
                    target_value INTEGER,
                    current_value INTEGER,
                    deadline DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def add_challenge_completion(
        self,
        user_id: str,
        challenge_id: str,
        score: int,
        time_spent: int,
        category: str,
        difficulty: str,
    ):
        with self.conn:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO user_progress 
                (user_id, challenge_id, completed_at, score, time_spent, category, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    challenge_id,
                    datetime.now(),
                    score,
                    time_spent,
                    category,
                    difficulty,
                ),
            )

    def set_learning_goal(
        self, user_id: str, goal_type: str, target_value: int, deadline: str
    ):
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO learning_goals 
                (user_id, goal_type, target_value, current_value, deadline)
                VALUES (?, ?, ?, 0, ?)
            """,
                (user_id, goal_type, target_value, deadline),
            )

    def update_goal_progress(self, user_id: str, goal_type: str, progress: int):
        with self.conn:
            self.conn.execute(
                """
                UPDATE learning_goals
                SET current_value = current_value + ?
                WHERE user_id = ? AND goal_type = ?
            """,
                (progress, user_id, goal_type),
            )

    def get_learning_goals(self, user_id: str) -> pd.DataFrame:
        return pd.read_sql_query(
            """
            SELECT goal_type, target_value, current_value, deadline
            FROM learning_goals
            WHERE user_id = ?
            ORDER BY deadline ASC
        """,
            self.conn,
            params=(user_id,),
        )

    def get_user_statistics(self, user_id: str, days: int = 30) -> dict:
        """獲取用戶統計數據"""
        start_date = datetime.now() - timedelta(days=days)

        # 獲取總積分
        total_points = self.conn.execute(
            """
            SELECT COALESCE(SUM(score), 0)
            FROM user_progress
            WHERE user_id = ?
        """,
            (user_id,),
        ).fetchone()[0]

        # 獲取完成的挑戰數
        completed_challenges = self.conn.execute(
            """
            SELECT COUNT(*)
            FROM user_progress
            WHERE user_id = ?
        """,
            (user_id,),
        ).fetchone()[0]

        # 獲取最近一次活動時間
        last_activity = self.conn.execute(
            """
            SELECT MAX(completed_at)
            FROM user_progress
            WHERE user_id = ?
        """,
            (user_id,),
        ).fetchone()[0]

        return {
            "total_points": total_points,
            "completed_challenges": completed_challenges,
            "last_activity": last_activity,
        }


def show_progress_dashboard():
    st.title("學習進度追蹤")

    if "user" not in st.session_state:
        st.warning("請先登入！")
        return

    tracker = ProgressTracker()

    # 創建標籤頁
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 總覽", "🎯 學習目標", "📈 詳細統計", "🏆 成就系統"]
    )

    with tab1:
        show_overview_tab(tracker)

    with tab2:
        show_goals_tab(tracker)

    with tab3:
        show_statistics_tab(tracker)

    with tab4:
        show_achievements_tab(tracker)


def show_overview_tab(tracker):
    st.subheader("學習概覽")

    # 互動式時間範圍選擇
    time_range = st.selectbox("選擇時間範圍", ["今天", "本週", "本月", "全部"])

    col1, col2, col3 = st.columns(3)

    # 動態計算統計數據
    with col1:
        points = random.randint(100, 1000)  # 實際應從數據庫獲取
        st.metric(label="總積分", value=points, delta=f"+{random.randint(10, 50)} 本週")

    with col2:
        challenges = random.randint(5, 20)
        st.metric(
            label="完成挑戰數", value=challenges, delta=f"+{random.randint(1, 5)} 本週"
        )

    with col3:
        streak = random.randint(1, 10)
        st.metric(label="連續學習天數", value=f"{streak} 天", delta="繼續保持！")

    # 互動式進度圖表
    show_interactive_progress_chart(tracker)


def show_goals_tab(tracker):
    st.subheader("學習目標設定")

    # 新增學習目標
    with st.expander("設定新目標"):
        col1, col2 = st.columns(2)
        with col1:
            goal_type = st.selectbox("目標類型", ["每日積分", "完成挑戰數", "學習時間"])
            target_value = st.number_input("目標值", min_value=1, value=100)

        with col2:
            deadline = st.date_input("完成期限", min_value=datetime.now().date())

        if st.button("添加目標"):
            tracker.set_learning_goal(
                st.session_state.user,
                goal_type,
                target_value,
                deadline.strftime("%Y-%m-%d"),
            )
            st.success("目標設定成功！")

    # 顯示現有目標
    goals = tracker.get_learning_goals(st.session_state.user)
    if not goals.empty:
        for _, goal in goals.iterrows():
            progress = (goal["current_value"] / goal["target_value"]) * 100
            st.write(f"### {goal['goal_type']}")
            st.progress(min(progress / 100, 1.0))
            st.write(
                f"進度: {goal['current_value']}/{goal['target_value']} ({progress:.1f}%)"
            )
            st.write(f"截止日期: {goal['deadline']}")


def show_statistics_tab(tracker):
    st.subheader("詳細統計")

    # 類別選擇
    category = st.selectbox(
        "選擇分析類別", ["挑戰完成情況", "學習時間分布", "積分獲得趨勢"]
    )

    # 時間範圍選擇
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "開始日期", value=datetime.now().date() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input("結束日期", value=datetime.now().date())

    # 根據選擇顯示不同圖表
    if category == "挑戰完成情況":
        show_challenge_completion_chart()
    elif category == "學習時間分布":
        show_learning_time_chart()
    else:
        show_points_trend_chart()


def show_achievements_tab(tracker):
    st.subheader("成就系統")

    # 成就分類
    achievement_type = st.selectbox("成就類別", ["基礎成就", "挑戰成就", "特殊成就"])

    # 展示成就
    col1, col2 = st.columns(2)

    achievements = {
        "基礎成就": [
            ("初心者", "完成首次查詢", True),
            ("勤奮學習", "連續學習7天", False),
            ("積分達人", "累計獲得1000積分", False),
        ],
        "挑戰成就": [
            ("解題高手", "完成10個困難挑戰", False),
            ("速度之王", "在30秒內完成挑戰", True),
            ("完美解答", "獲得3個滿分評價", False),
        ],
        "特殊成就": [
            ("探索者", "使用所有API功能", False),
            ("創新者", "創建自定義查詢", True),
            ("幫助者", "分享學習心得", False),
        ],
    }

    for name, desc, unlocked in achievements[achievement_type]:
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                if unlocked:
                    st.markdown("🌟")
                else:
                    st.markdown("⭐")
            with col2:
                st.markdown(f"**{name}**")
                st.caption(desc)
                if unlocked:
                    st.success("已解鎖")
                else:
                    st.info("未解鎖")


def show_interactive_progress_chart(tracker):
    # 創建示例數據
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    points = [random.randint(50, 200) for _ in range(30)]

    # 創建互動式圖表
    fig = go.Figure()

    # 添加積分線
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=points,
            mode="lines+markers",
            name="每日積分",
            hovertemplate="日期: %{x}<br>積分: %{y}<extra></extra>",
        )
    )

    # 更新布局
    fig.update_layout(
        title="積分趨勢",
        xaxis_title="日期",
        yaxis_title="積分",
        hovermode="x unified",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)


def show_challenge_completion_chart():
    # 創建示例數據
    categories = ["簡單", "中等", "困難"]
    completed = [random.randint(5, 15) for _ in range(3)]
    total = [15, 12, 8]

    fig = go.Figure()

    # 添加完成的挑戰
    fig.add_trace(
        go.Bar(
            name="已完成", x=categories, y=completed, marker_color="rgb(26, 118, 255)"
        )
    )

    # 添加總挑戰數
    fig.add_trace(
        go.Bar(name="總數", x=categories, y=total, marker_color="rgb(158, 158, 158)")
    )

    fig.update_layout(
        title="挑戰完成情況", barmode="group", xaxis_title="難度", yaxis_title="數量"
    )

    st.plotly_chart(fig, use_container_width=True)


def show_learning_time_chart():
    # 創建示例數據
    days = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    morning = [random.randint(30, 90) for _ in range(7)]
    afternoon = [random.randint(30, 90) for _ in range(7)]
    evening = [random.randint(30, 90) for _ in range(7)]

    fig = go.Figure()

    fig.add_trace(go.Bar(name="早上", x=days, y=morning))
    fig.add_trace(go.Bar(name="下午", x=days, y=afternoon))
    fig.add_trace(go.Bar(name="晚上", x=days, y=evening))

    fig.update_layout(
        title="學習時間分布",
        barmode="stack",
        xaxis_title="星期",
        yaxis_title="學習時間（分鐘）",
    )

    st.plotly_chart(fig, use_container_width=True)


def show_points_trend_chart():
    # 創建示例數據
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    daily_points = [random.randint(50, 200) for _ in range(30)]
    cumulative_points = np.cumsum(daily_points)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=dates, y=daily_points, name="每日積分", mode="lines+markers")
    )

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=cumulative_points,
            name="累計積分",
            mode="lines",
            line=dict(dash="dash"),
        )
    )

    fig.update_layout(title="積分趨勢分析", xaxis_title="日期", yaxis_title="積分")

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    show_progress_dashboard()
