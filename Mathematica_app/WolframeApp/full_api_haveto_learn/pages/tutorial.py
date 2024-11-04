# pages/tutorial.py

import streamlit as st
import json
import time
from typing import Dict, Any

# 教程管理器類，負責加載課程數據和追踪學習進度
class TutorialManager:
    def __init__(self):
        # 初始化教程管理器並加載課程數據
        self.lessons = self.load_lessons()
        
    def load_lessons(self) -> Dict[str, Any]:
        # 模擬從數據庫或配置文件加載課程數據
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
                    # 可以添加更多課程...
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
        # 模擬從數據庫獲取用戶的學習進度
        return {
            "已完成課程": ["基礎篇-1", "基礎篇-2"],
            "當前課程": "基礎篇-3",
            "學習時間": 120  # 分鐘
        }

# 主函數，顯示教程頁面
def show_tutorial_page():
    st.title("互動式教程")
    
    # 初始化教程管理器
    tutorial_manager = TutorialManager()
    
    # 選擇課程系列
    series = st.selectbox(
        "選擇課程系列",
        list(tutorial_manager.lessons.keys())
    )
    
    # 如果選擇了系列，顯示對應的課程
    if series:
        show_lesson_series(tutorial_manager, series)

def show_lesson_series(manager: TutorialManager, series: str):
    # 顯示選定課程系列中的課程列表
    lessons = manager.lessons[series]["課程"]
    
    # 創建課程選擇框
    lesson_titles = [lesson["標題"] for lesson in lessons]
    current_lesson = st.selectbox("選擇課程", lesson_titles)
    
    # 顯示選定的課程內容
    for lesson in lessons:
        if lesson["標題"] == current_lesson:
            show_lesson_content(lesson)
            break

def show_lesson_content(lesson: Dict[str, Any]):
    # 顯示課程的具體內容，包括文本、示例代碼和練習
    st.markdown(lesson["內容"])
    
    # 顯示示例代碼區域
    with st.expander("查看示例代碼"):
        st.code(lesson["示例代碼"], language="python")
    
    # 如果有練習，顯示練習題
    if lesson.get("練習"):
        st.subheader("練習")
        st.write(lesson["練習"]["題目"])
        st.info(f"💡 提示: {lesson['練習']['提示']}")
        
        # 代碼編輯器讓用戶編寫代碼
        user_code = st.text_area(
            "在這裡編寫你的代碼：",
            height=200,
            key="code_editor"
        )
        
        # 運行用戶代碼按鈕
        if st.button("運行代碼"):
            with st.spinner("正在執行..."):
                try:
                    # 執行用戶代碼，並確保安全
                    exec_with_safety(user_code)
                except Exception as e:
                    st.error(f"執行錯誤: {str(e)}")

def exec_with_safety(code: str):
    """安全地執行用戶代碼"""
    import ast
    
    try:
        # 進行語法檢查
        ast.parse(code)
        
        # 創建一個安全的命名空間
        local_dict = {}
        
        # 執行代碼並顯示結果
        exec(code, {"__builtins__": __builtins__}, local_dict)
        
        if 'result' in local_dict:
            st.success("執行成功！")
            st.write("結果：", local_dict['result'])
            
    except SyntaxError as e:
        st.error(f"語法錯誤: {str(e)}")
    except Exception as e:
        st.error(f"執行錯誤: {str(e)}")

# 檢查練習的正確性
class ExerciseChecker:
    def __init__(self):
        # 定義一些練習題和測試案例
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
                # 執行用戶代碼並檢查結果是否正確
                result = self.run_test(user_code, test["input"])
                results.append(str(result) == test["expected"])
            except Exception as e:
                st.error(f"測試失敗: {str(e)}")
                return False
                
        return all(results)
    
    def run_test(self, code: str, test_input: str):
        # 安全地運行測試用戶代碼
        local_dict = {"test_input": test_input}
        exec(code, {"__builtins__": __builtins__}, local_dict)
        return local_dict.get("result")

# 更新用戶的學習進度
def update_progress(user_id: str, lesson_id: str):
    """更新用戶的學習進度"""
    # 這裡可以添加數據庫操作來記錄進度
    pass

# 主程序入口，顯示教程頁面
if __name__ == "__main__":
    show_tutorial_page()