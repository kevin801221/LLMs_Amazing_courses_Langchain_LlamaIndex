# pages/wolfram_response.py
import streamlit as st
import json
from typing import Dict, Any

def show_response_page():
    st.title("Wolfram Alpha API 響應解析")
    
    # 確保有 API Key
    if "wolfram_api_key" not in st.session_state:
        api_key = st.text_input(
            "請輸入你的 Wolfram API Key:",
            type="password",
            key="api_key_input"
        )
        if api_key:
            st.session_state.wolfram_api_key = api_key
        else:
            st.warning("請先輸入 API Key 才能繼續")
            return

    # 創建示範響應
    st.header("響應格式解析")
    
    tabs = st.tabs(["JSON 響應", "XML 響應", "錯誤響應"])
    
    with tabs[0]:
        show_json_response()
    
    with tabs[1]:
        show_xml_response()
        
    with tabs[2]:
        show_error_response()

def show_json_response():
    st.subheader("JSON 響應格式")
    
    example_json = {
        "queryresult": {
            "success": True,
            "error": False,
            "numpods": 2,
            "pods": [
                {
                    "title": "Input",
                    "scanner": "Identity",
                    "id": "Input",
                    "subpods": [
                        {
                            "plaintext": "2 + 2",
                            "img": {
                                "src": "example.com/image.gif",
                                "alt": "2 + 2",
                                "title": "2 + 2"
                            }
                        }
                    ]
                },
                {
                    "title": "Result",
                    "scanner": "Numeric",
                    "id": "Result",
                    "subpods": [
                        {
                            "plaintext": "4",
                            "img": {
                                "src": "example.com/result.gif",
                                "alt": "4",
                                "title": "4"
                            }
                        }
                    ]
                }
            ]
        }
    }
    
    # 顯示示例
    st.json(example_json)
    
    # 解析說明
    st.markdown("""
    ### JSON 響應結構說明
    
    1. `queryresult`: 主要響應對象
        - `success`: 查詢是否成功
        - `error`: 是否有錯誤
        - `numpods`: 返回的 pod 數量
        
    2. `pods`: 包含查詢結果的數組
        - `title`: Pod 標題
        - `scanner`: 使用的掃描器類型
        - `id`: Pod 唯一標識符
        
    3. `subpods`: 包含實際內容的數組
        - `plaintext`: 純文本格式的結果
        - `img`: 圖片格式的結果
    """)

def show_xml_response():
    st.subheader("XML 響應格式")
    
    example_xml = """
    <?xml version='1.0' encoding='UTF-8'?>
    <queryresult success='true' error='false' numpods='2'>
        <pod title='Input' scanner='Identity' id='Input'>
            <subpod>
                <plaintext>2 + 2</plaintext>
                <img src="example.com/image.gif" alt="2 + 2" title="2 + 2"/>
            </subpod>
        </pod>
        <pod title='Result' scanner='Numeric' id='Result'>
            <subpod>
                <plaintext>4</plaintext>
                <img src="example.com/result.gif" alt="4" title="4"/>
            </subpod>
        </pod>
    </queryresult>
    """
    
    st.code(example_xml, language="xml")
    
    st.markdown("""
    ### XML 響應結構說明
    
    1. `<queryresult>`: 根元素
        - `success`: 查詢是否成功
        - `error`: 是否有錯誤
        - `numpods`: Pod 數量
        
    2. `<pod>`: 結果容器
        - `title`: Pod 標題
        - `scanner`: 掃描器類型
        - `id`: 唯一標識符
        
    3. `<subpod>`: 具體內容
        - `<plaintext>`: 文本結果
        - `<img>`: 圖片結果
    """)

def show_error_response():
    st.subheader("錯誤響應格式")
    
    error_json = {
        "queryresult": {
            "success": False,
            "error": True,
            "tips": [
                {
                    "text": "Check your input for spelling mistakes"
                },
                {
                    "text": "Make sure you are using the correct API endpoint"
                }
            ],
            "error": {
                "code": 1,
                "msg": "Invalid input"
            }
        }
    }
    
    st.json(error_json)
    
    st.markdown("""
    ### 錯誤響應說明
    
    1. 通用錯誤格式
        - `success`: 始終為 `false`
        - `error`: 始終為 `true`
        - `tips`: 可能的解決建議
        - `error.code`: 錯誤代碼
        - `error.msg`: 錯誤描述
        
    2. 常見錯誤代碼
        - `1`: 無效輸入
        - `2`: API 密鑰錯誤
        - `3`: 超出配額限制
        - `4`: 超時
    """)

if __name__ == "__main__":
    show_response_page()