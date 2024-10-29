# pages/tutorial.py

import streamlit as st
import json
import time
from typing import Dict, Any

class TutorialManager:
    def __init__(self):
        self.lessons = self.load_lessons()
        
    def load_lessons(self) -> Dict[str, Any]:
        # 在實際應用中，這些數據可以從數據庫或配置文件加載
        return {
            "基礎篇": {
                "序號": 1,
                "課程": [
                    {
                        "標題": "Wolfram API 簡介",
                        "內容": """
                        # Wolfram Alpha API 基礎
                        
                        Wolfram Alpha API 是一個強大的知識計算引擎...
                        """,
                        "示例代碼": """
                        import requests
                        
                        def basic_query(api_key, query):
                            url = "http://api.wolframalpha.com/v2/query"
                            params = {
                                "appid": api_key,
                                "input": query,
                                "format": "plaintext"
                            }
                            return requests.get(url, params=params)
                        """,
                        "練習": {
                            "題目": "試著發送一個簡單的 API 請求",
                            "提示": "使用上面的示例代碼，查詢 '2+2' 的結果"
                        }
                    },
                    # 更多課程...
                ]
            },
            "進階篇": {
                "序號": 2,
                "課程": [
                    {
                        "標題": "參數配置與優化",
                        "內容": "...",
                        "示例代碼": "...",
                        "練習": {}
                    }
                ]
            }
        }

    def get_lesson_progress(self, user_id: str) -> Dict[str, Any]:
        # 從數據庫獲取用戶學習進度
        return {
            "已完成課程": ["基礎篇-1", "基礎篇-2"],
            "當前課程": "基礎篇-3",
            "學習時間": 120  # 分鐘
        }

def show_tutorial_page():
    st.title("互動式教程")
    
    # 初始化教程管理器
    tutorial_manager = TutorialManager()
    
    # 選擇課程系列
    series = st.selectbox(
        "選擇課程系列",
        list(tutorial_manager.lessons.keys())
    )
    
    # 顯示當前系列的課程
    if series:
        show_lesson_series(tutorial_manager, series)

def show_lesson_series(manager: TutorialManager, series: str):
    lessons = manager.lessons[series]["課程"]
    
    # 選擇具體課程
    lesson_titles = [lesson["標題"] for lesson in lessons]
    current_lesson = st.selectbox("選擇課程", lesson_titles)
    
    # 顯示課程內容
    for lesson in lessons:
        if lesson["標題"] == current_lesson:
            show_lesson_content(lesson)
            break

def show_lesson_content(lesson: Dict[str, Any]):
    # 顯示課程內容
    st.markdown(lesson["內容"])
    
    # 顯示示例代碼
    with st.expander("查看示例代碼"):
        st.code(lesson["示例代碼"], language="python")
    
    # 互動練習
    if lesson.get("練習"):
        st.subheader("練習")
        st.write(lesson["練習"]["題目"])
        st.info(f"💡 提示: {lesson['練習']['提示']}")
        
        # pages/tutorial.py (續)

        # 代碼編輯器
        user_code = st.text_area(
            "在這裡編寫你的代碼：",
            height=200,
            key="code_editor"
        )
        
        # 運行按鈕
        if st.button("運行代碼"):
            with st.spinner("正在執行..."):
                try:
                    # 這裡可以添加代碼安全檢查
                    exec_with_safety(user_code)
                except Exception as e:
                    st.error(f"執行錯誤: {str(e)}")

def exec_with_safety(code: str):
    """安全地執行用戶代碼"""
    # 這裡可以添加代碼安全性檢查
    # 例如：限制執行時間、限制導入的模組等
    import ast
    
    try:
        # 語法檢查
        ast.parse(code)
        
        # 創建安全的局部命名空間
        local_dict = {}
        
        # 執行代碼
        exec(code, {"__builtins__": __builtins__}, local_dict)
        
        # 顯示結果
        if 'result' in local_dict:
            st.success("執行成功！")
            st.write("結果：", local_dict['result'])
            
    except SyntaxError as e:
        st.error(f"語法錯誤: {str(e)}")
    except Exception as e:
        st.error(f"執行錯誤: {str(e)}")

# 添加互動式練習檢查器
class ExerciseChecker:
    def __init__(self):
        self.test_cases = {
            "基礎API調用": [
                {
                    "input": "2+2",
                    "expected": "4"
                },
                {
                    "input": "sqrt(16)",
                    "expected": "4"
                }
            ]
        }
    
    def check_exercise(self, exercise_name: str, user_code: str) -> bool:
        if exercise_name not in self.test_cases:
            return False
            
        tests = self.test_cases[exercise_name]
        results = []
        
        for test in tests:
            try:
                # 執行用戶代碼
                result = self.run_test(user_code, test["input"])
                results.append(str(result) == test["expected"])
            except Exception as e:
                st.error(f"測試失敗: {str(e)}")
                return False
                
        return all(results)
    
    def run_test(self, code: str, test_input: str):
        # 安全地運行測試
        local_dict = {"test_input": test_input}
        exec(code, {"__builtins__": __builtins__}, local_dict)
        return local_dict.get("result")

# 添加進度追踪
def update_progress(user_id: str, lesson_id: str):
    """更新用戶的學習進度"""
    # 這裡可以添加數據庫操作
    pass

if __name__ == "__main__":
    show_tutorial_page()