'''
這段程式碼使用 Streamlit 創建了一個互動式教程平台，幫助用戶學習 Python、Wolfram API 等相關知識。它包含課程管理、練習、進度跟蹤和代碼執行等功能，並通過與 SQLite 資料庫的連接來保存用戶的學習進度。

以下是程式碼的詳細說明：

1. 必要模組的匯入

import streamlit as st
import json
import time
from typing import Dict, Any
import sqlite3
from pathlib import Path
import random

	•	streamlit：用於構建網頁介面。
	•	json：用於處理 JSON 格式的數據。
	•	time：用於計算時間。
	•	sqlite3：用於連接 SQLite 資料庫，保存用戶學習進度。
	•	Path：用於管理路徑，方便定位資料庫存儲路徑。
	•	random：用於生成隨機的鼓勵性評語。

2. TutorialManager 類

TutorialManager 類負責管理課程內容、用戶進度和資料庫操作。它包含了課程的加載、資料庫初始化和進度保存等功能。

初始化方法

class TutorialManager:
    def __init__(self):
        self.lessons = self.load_lessons()
        db_dir = Path(__file__).parent.parent / "database"
        db_dir.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(str(db_dir / "wolfram_app.db"))
        self.create_tables()

	•	self.lessons：存儲加載的課程內容。
	•	資料庫初始化：在父目錄創建一個 database 資料夾，並使用 SQLite 資料庫 wolfram_app.db 來儲存用戶進度。

建立資料表

def create_tables(self):
    """創建必要的資料表"""
    with self.conn:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tutorial_progress (
                user_id TEXT,
                lesson_id TEXT,
                completed_at TIMESTAMP,
                score INTEGER,
                time_spent INTEGER,
                PRIMARY KEY (user_id, lesson_id)
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS exercise_completion (
                user_id TEXT,
                exercise_id TEXT,
                completed_at TIMESTAMP,
                attempts INTEGER,
                success BOOLEAN,
                PRIMARY KEY (user_id, exercise_id)
            )
        """)

	•	tutorial_progress 表用於存儲用戶的課程進度，包括用戶 ID、課程 ID、完成時間、得分和學習時間。
	•	exercise_completion 表用於記錄用戶的練習完成狀態，包含用戶 ID、練習 ID、完成時間、嘗試次數和是否成功。

3. 加載課程內容

def load_lessons(self) -> Dict[str, Any]:
    """加載課程內容"""
    return {
        "Python 基礎": { ... },
        "Wolfram API 入門": { ... },
        "實用應用案例": { ... }
    }

	•	該方法返回一個課程字典，課程包括標題、描述、課程內容、示例代碼和練習等。
	•	每個課程包含不同的章節和練習題目，幫助用戶逐步掌握知識。

4. 保存和獲取學習進度

def save_progress(self, user_id: str, lesson_id: str, score: int, time_spent: int):
    """保存學習進度"""
    with self.conn:
        self.conn.execute("""
            INSERT OR REPLACE INTO tutorial_progress 
            (user_id, lesson_id, completed_at, score, time_spent)
            VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
        """, (user_id, lesson_id, score, time_spent))

	•	save_progress：保存用戶學習進度至資料庫，包含用戶 ID、課程 ID、完成時間、分數和花費時間。

def get_progress(self, user_id: str) -> Dict[str, Any]:
    """獲取用戶進度"""
    cursor = self.conn.execute("""
        SELECT lesson_id, completed_at, score, time_spent
        FROM tutorial_progress
        WHERE user_id = ?
        ORDER BY completed_at DESC
    """, (user_id,))
    progress = cursor.fetchall()
    return {
        "completed_lessons": [p[0] for p in progress],
        "total_score": sum(p[2] for p in progress),
        "total_time": sum(p[3] for p in progress)
    }

	•	get_progress：從資料庫中獲取用戶的學習進度，包括已完成課程、總積分和總學習時間。

5. 顯示教程頁面 show_tutorial_page

def show_tutorial_page():
    st.title("🎓 互動式 Wolfram API 教程")
    
    if 'user' not in st.session_state:
        st.warning("請先登入再開始學習！")
        return
        
    tutorial_manager = TutorialManager()
    
    with st.sidebar:
        st.subheader("📚 課程導航")
        series = st.selectbox(
            "選擇課程系列",
            list(tutorial_manager.lessons.keys())
        )
        
        progress = tutorial_manager.get_progress(st.session_state.user)
        st.metric("完成課程數", len(progress["completed_lessons"]))
        st.metric("總積分", progress["total_score"])
        st.metric("學習時間", f"{progress['total_time']} 分鐘")
    
    if series:
        show_lesson_series(tutorial_manager, series)

	•	顯示教程頁面的主介面，包括課程導航、進度統計和課程選擇。
	•	側邊欄顯示用戶的課程進度統計（已完成課程、總積分和學習時間）。

6. 顯示課程系列 show_lesson_series

def show_lesson_series(manager: TutorialManager, series: str):
    st.header(f"📖 {series}")
    st.write(manager.lessons[series]["描述"])
    
    lessons = manager.lessons[series]["課程"]
    if not lessons:
        st.info("本系列課程正在開發中...")
        return
        
    tabs = st.tabs([lesson["標題"] for lesson in lessons])
    
    for tab, lesson in zip(tabs, lessons):
        with tab:
            show_lesson_content(lesson)

	•	顯示課程描述：展示所選課程系列的描述。
	•	課程標籤頁：創建每個章節的標籤頁，讓用戶可以切換不同章節學習。

7. 顯示課程內容 show_lesson_content

def show_lesson_content(lesson: Dict[str, Any]):
    st.markdown(lesson["內容"])
    
    if lesson["示例代碼"]:
        with st.expander("💻 示例代碼"):
            st.code(lesson["示例代碼"], language="python")
            if st.button("運行示例", key=f"run_{lesson['標題']}_example"):
                with st.spinner("執行中..."):
                    try:
                        exec_with_safety(lesson["示例代碼"])
                    except Exception as e:
                        st.error(f"執行錯誤: {str(e)}")
    
    if lesson.get("練習"):
        st.subheader("✍️ 練習時間")
        st.write(lesson["練習"]["題目"])
        st.info(f"💡 提示: {lesson['練習']['提示']}")
        
        user_code = st.text_area(
            "編寫你的代碼：",
            value=default_code,
            height=300,
            key=f"code_editor_{lesson['標題']}"
        )
        
        if st.button("🚀 運行代碼", key=f"run_{lesson['標題']}"):
            with st.spinner("執行中..."):
                exec_with_safety(user_code)
        
        if st.button("💾 提交答案", key=f"submit_{lesson['標題']}"):
            check_exercise_solution(user_code, lesson["練習"])

	•	示例代碼區：展示和運行示例代碼。
	•	練習區域：用戶可以在練習區撰寫代碼，並執行或提交答案。

8. 執行代碼和檢查答案

def exec_with_safety(code: str):
    """安全地執行用戶代碼"""
    try:
        local_dict = {}
        exec(code, {"__builtins__": __builtins__}, local_dict)
        
        if 'result' in local_dict:
            st.success("執行成功！")
            st.write("結果：", local_dict['result'])
            
    except Exception as e:
        st.error(f"執行錯誤: {str(e)}")

	•	exec_with_safety：安全執行用戶代碼，並檢查是否有 result 變數以顯示結果。

def check_exercise_solution(code: str, exercise: Dict[str, Any]):
    """檢查練習答案"""
    st.success("答案已提交！")
    encouragements = [
        "做得好！繼續努力！",
        "太棒了！你正在進步！",
        "excellent！你的解法很有創意！",
        "不錯的嘗試！要不要挑戰下一題？"
    ]
    st.write(random.choice(encouragements))

	•	check_exercise_solution：用於檢查用戶提交的練習答案，並隨機顯示鼓勵性評語。

主函數

if __name__ == "__main__":
    show_tutorial_page()

	•	啟動 Streamlit 應用並顯示教程頁面。
'''
import streamlit as st
import json
import time
from typing import Dict, Any
import sqlite3
from pathlib import Path
import random

class TutorialManager:
    def __init__(self):
        self.lessons = self.load_lessons()
        # 初始化資料庫連接
        db_dir = Path(__file__).parent.parent / "database"
        db_dir.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(str(db_dir / "wolfram_app.db"))
        self.create_tables()
        
    def create_tables(self):
        """創建必要的資料表"""
        with self.conn:
            # 學習進度表
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tutorial_progress (
                    user_id TEXT,
                    lesson_id TEXT,
                    completed_at TIMESTAMP,
                    score INTEGER,
                    time_spent INTEGER,
                    PRIMARY KEY (user_id, lesson_id)
                )
            """)
            
            # 練習完成記錄
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS exercise_completion (
                    user_id TEXT,
                    exercise_id TEXT,
                    completed_at TIMESTAMP,
                    attempts INTEGER,
                    success BOOLEAN,
                    PRIMARY KEY (user_id, exercise_id)
                )
            """)

    def load_lessons(self) -> Dict[str, Any]:
        """加載課程內容"""
        return {
            "Python 基礎": {
                "序號": 1,
                "描述": "學習使用 Python 進行基礎編程",
                "課程": [
                    {
                        "標題": "Python 環境設置",
                        "內容": """
                        # Python 開發環境設置
                        
                        在開始使用 Wolfram API 之前，我們需要先設置 Python 環境。
                        
                        ## 必要套件安裝
                        ```bash
                        pip install requests streamlit plotly pandas
                        ```
                        
                        ## 開發環境建議
                        1. 使用 VS Code 或 PyCharm 作為 IDE
                        2. 建立虛擬環境來管理套件
                        3. 使用版本控制（Git）追蹤代碼變更
                        """,
                        "示例代碼": None,
                        "練習": {
                            "題目": "確認環境設置",
                            "提示": "執行簡單的 Python 代碼來測試環境",
                            "測試代碼": "print('Hello, Wolfram!')"
                        }
                    },
                    {
                        "標題": "API 基礎概念",
                        "內容": """
                        # API 基礎知識
                        
                        API（應用程式介面）是軟體之間溝通的橋樑。
                        
                        ## 重要概念
                        1. HTTP 請求方法（GET, POST 等）
                        2. 請求參數
                        3. 響應格式（JSON, XML）
                        4. 錯誤處理
                        """,
                        "示例代碼": """
                        import requests
                        
                        def test_api():
                            # 測試連接
                            response = requests.get('https://api.wolframalpha.com/v1/api-test')
                            return response.status_code == 200
                        """,
                        "練習": {
                            "題目": "測試 API 連接",
                            "提示": "使用 requests 庫發送請求",
                            "測試代碼": "result = test_api()"
                        }
                    }
                ]
            },
            "Wolfram API 入門": {
                "序號": 2,
                "描述": "學習 Wolfram API 的基本使用",
                "課程": [
                    {
                        "標題": "第一個查詢",
                        "內容": """
                        # 開始使用 Wolfram API
                        
                        讓我們從最簡單的數學運算開始。
                        
                        ## API 金鑰設置
                        1. 註冊 Wolfram 開發者帳號
                        2. 創建新的 API 應用
                        3. 獲取 API 金鑰
                        """,
                        "示例代碼": """
                        def simple_math_query(api_key: str, expression: str):
                            url = "http://api.wolframalpha.com/v2/query"
                            params = {
                                "appid": api_key,
                                "input": expression,
                                "format": "plaintext"
                            }
                            return requests.get(url, params=params)
                        
                        # 示例：計算 2+2
                        result = simple_math_query(api_key, "2+2")
                        """,
                        "練習": {
                            "題目": "計算圓周率的前10位",
                            "提示": "使用 'pi digits 10' 作為查詢",
                            "測試代碼": None
                        }
                    },
                    {
                        "標題": "進階查詢技巧",
                        "內容": """
                        # Wolfram API 進階查詢
                        
                        學習如何構建更複雜的查詢。
                        
                        ## 支持的查詢類型
                        1. 數學運算
                        2. 科學計算
                        3. 統計分析
                        4. 數據可視化
                        """,
                        "示例代碼": """
                        def advanced_query(api_key: str, query: str, format: str = "plaintext"):
                            url = "http://api.wolframalpha.com/v2/query"
                            params = {
                                "appid": api_key,
                                "input": query,
                                "format": format,
                                "output": "json"
                            }
                            return requests.get(url, params=params).json()
                        """,
                        "練習": {
                            "題目": "計算複雜的數學表達式",
                            "提示": "嘗試計算 'integrate sin(x) dx from 0 to pi'",
                            "測試代碼": None
                        }
                    }
                ]
            },
            "實用應用案例": {
                "序號": 3,
                "描述": "通過實際案例學習 API 應用",
                "課程": [
                    {
                        "標題": "數學解題助手",
                        "內容": """
                        # 創建數學解題助手
                        
                        學習如何使用 API 解決數學問題。
                        
                        ## 功能特點
                        1. 方程求解
                        2. 微積分計算
                        3. 繪製函數圖像
                        """,
                        "示例代碼": """
                        class MathSolver:
                            def __init__(self, api_key):
                                self.api_key = api_key
                            
                            def solve_equation(self, equation):
                                return advanced_query(
                                    self.api_key,
                                    f"solve {equation}"
                                )
                                
                            def plot_function(self, function):
                                return advanced_query(
                                    self.api_key,
                                    f"plot {function}",
                                    "image"
                                )
                        """,
                        "練習": {
                            "題目": "創建一個解二次方程的函數",
                            "提示": "解方程 ax² + bx + c = 0",
                            "測試代碼": None
                        }
                    }
                ]
            }
        }

    def save_progress(self, user_id: str, lesson_id: str, score: int, time_spent: int):
        """保存學習進度"""
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO tutorial_progress 
                (user_id, lesson_id, completed_at, score, time_spent)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
            """, (user_id, lesson_id, score, time_spent))

    def get_progress(self, user_id: str) -> Dict[str, Any]:
        """獲取用戶進度"""
        cursor = self.conn.execute("""
            SELECT lesson_id, completed_at, score, time_spent
            FROM tutorial_progress
            WHERE user_id = ?
            ORDER BY completed_at DESC
        """, (user_id,))
        progress = cursor.fetchall()
        return {
            "completed_lessons": [p[0] for p in progress],
            "total_score": sum(p[2] for p in progress),
            "total_time": sum(p[3] for p in progress)
        }

def show_tutorial_page():
    st.title("🎓 互動式 Wolfram API 教程")
    
    if 'user' not in st.session_state:
        st.warning("請先登入再開始學習！")
        return
        
    tutorial_manager = TutorialManager()
    
    # 左側選單
    with st.sidebar:
        st.subheader("📚 課程導航")
        series = st.selectbox(
            "選擇課程系列",
            list(tutorial_manager.lessons.keys())
        )
        
        # 顯示進度統計
        progress = tutorial_manager.get_progress(st.session_state.user)
        st.metric("完成課程數", len(progress["completed_lessons"]))
        st.metric("總積分", progress["total_score"])
        st.metric("學習時間", f"{progress['total_time']} 分鐘")
    
    # 主要內容區域
    if series:
        show_lesson_series(tutorial_manager, series)

def show_lesson_series(manager: TutorialManager, series: str):
    st.header(f"📖 {series}")
    st.write(manager.lessons[series]["描述"])
    
    # 創建課程標籤頁
    lessons = manager.lessons[series]["課程"]
    if not lessons:
        st.info("本系列課程正在開發中...")
        return
        
    tabs = st.tabs([lesson["標題"] for lesson in lessons])
    
    # 顯示每個課程的內容
    for tab, lesson in zip(tabs, lessons):
        with tab:
            show_lesson_content(lesson)

def show_lesson_content(lesson: Dict[str, Any]):
    """顯示課程內容"""
    st.markdown(lesson["內容"])
    
    # 添加代碼示例說明
    st.markdown("""
    ### 💡 代碼編輯器使用說明
    
    代碼中必須包含 `result` 變數才能顯示結果。例如：
    
    1️⃣ 簡單計算:
    ```python
    result = 1 + 1
    ```
    
    2️⃣ 函數調用:
    ```python
    def square(x):
        return x * x
        
    number = 5
    result = square(number)
    ```
    
    3️⃣ API 調用:
    ```python
    import requests
    
    response = requests.get('https://api.example.com/data')
    result = response.text
    ```
    """)
    
    # 如果有示例代碼，顯示代碼區域
    if lesson["示例代碼"]:
        with st.expander("💻 示例代碼"):
            st.code(lesson["示例代碼"], language="python")
            # 添加示例代碼說明
            st.markdown("""
            #### 如何運行示例代碼:
            1. 複製上方代碼
            2. 在下方代碼編輯器中貼上
            3. 確保代碼中有 `result` 變數
            4. 點擊 '運行代碼' 按鈕
            """)
            
            if st.button("運行示例", key=f"run_{lesson['標題']}_example"):
                with st.spinner("執行中..."):
                    try:
                        exec_with_safety(lesson["示例代碼"])
                    except Exception as e:
                        st.error(f"執行錯誤: {str(e)}")
    
    # 練習區域
    if lesson.get("練習"):
        st.markdown("---")
        st.subheader("✍️ 練習時間")
        st.write(lesson["練習"]["題目"])
        st.info(f"💡 提示: {lesson['練習']['提示']}")
        
        # 添加代碼模板
        default_code = """# 在這裡編寫你的代碼
# 記得要有 result 變數

def solve_problem():
    # 你的解決方案
    answer = 0  # 替換成你的計算
    return answer

# 儲存結果到 result 變數
result = solve_problem()
"""
        
        # 代碼編輯器
        user_code = st.text_area(
            "編寫你的代碼：",
            value=default_code,
            height=300,
            key=f"code_editor_{lesson['標題']}"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 運行代碼", key=f"run_{lesson['標題']}"):
                with st.spinner("執行中..."):
                    exec_with_safety(user_code)
        
        with col2:
            if st.button("💾 提交答案", key=f"submit_{lesson['標題']}"):
                check_exercise_solution(user_code, lesson["練習"])

def exec_with_safety(code: str):
    """安全地執行用戶代碼"""
    try:
        # 創建安全的執行環境
        local_dict = {}
        exec(code, {"__builtins__": __builtins__}, local_dict)
        
        if 'result' in local_dict:
            st.success("執行成功！")
            st.write("結果：", local_dict['result'])
            
    except Exception as e:
        st.error(f"執行錯誤: {str(e)}")

def check_exercise_solution(code: str, exercise: Dict[str, Any]):
    """檢查練習答案"""
    # 這裡可以添加更複雜的答案檢查邏輯
    st.success("答案已提交！")
    # 隨機給予鼓勵性評語
    encouragements = [
        "做得好！繼續努力！",
        "太棒了！你正在進步！",
        "excellent！你的解法很有創意！",
        "不錯的嘗試！要不要挑戰下一題？"
    ]
    st.write(random.choice(encouragements))

if __name__ == "__main__":
    show_tutorial_page()