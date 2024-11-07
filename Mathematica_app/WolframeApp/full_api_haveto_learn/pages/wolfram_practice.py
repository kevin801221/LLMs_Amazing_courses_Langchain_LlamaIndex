'''
這段程式碼使用 Streamlit 創建了一個網頁應用，並集成了 Wolfram Alpha API，讓用戶可以在不同模式下進行查詢實踐，包含了「引導式練習」、「自由實戰」、「範例庫」和「挑戰模式」等功能。接下來是各個部分的詳細解說：

1. 必要模組的匯入

import streamlit as st
import requests
import json
import time
from typing import Dict, Any

	•	streamlit：用於創建網頁介面。
	•	requests：用於向 API 發送 HTTP 請求。
	•	json：用於解析和生成 JSON 格式數據。
	•	time：用於處理延遲或計時功能。
	•	Dict, Any：用於類型註解，讓函數更易於理解和維護。

2. execute_query 函數

該函數負責向 Wolfram Alpha API 發送查詢請求並返回結果。此函數支持自訂查詢參數，並根據結果格式化顯示內容。

def execute_query(query: str, context: str, params: Dict[str, Any] = None):
    """執行 API 查詢並返回結果"""
    api_key = st.session_state.get("wolfram_api_key")
    if not api_key:
        st.error("請先輸入 API Key!")
        return

    with st.spinner("處理中..."):
        try:
            base_url = "http://api.wolframalpha.com/v2/query"
            default_params = {
                "appid": api_key,
                "input": query,
                "format": "plaintext,image",
                "output": "json",
            }

            if params:
                default_params.update(params)

            response = requests.get(base_url, params=default_params)
            response.raise_for_status()
            result = response.json()

            if "queryresult" in result:
                queryresult = result["queryresult"]

                if queryresult.get("success"):
                    st.success(f"✨ {context}查詢成功!")
                    for pod in queryresult.get("pods", []):
                        st.subheader(pod.get("title", ""))
                        for subpod in pod.get("subpods", []):
                            if subpod.get("plaintext"):
                                st.write(subpod["plaintext"])
                            if "img" in subpod:
                                st.image(
                                    subpod["img"]["src"],
                                    caption=pod.get("title", ""),
                                    use_column_width=True,
                                )
                    st.info(f"計算耗時: {queryresult.get('timing', 'N/A')} 秒")
                    return queryresult
                else:
                    st.warning("未找到結果!")
                    if "tips" in queryresult:
                        st.info(
                            "💡 提示: "
                            + "\n".join(
                                tip.get("text", "") for tip in queryresult["tips"]
                            )
                        )
            else:
                st.error("無效的響應格式!")

        except requests.RequestException as e:
            st.error(f"API 請求錯誤: {str(e)}")
        except json.JSONDecodeError:
            st.error("響應解析錯誤!")
        except Exception as e:
            st.error(f"發生未知錯誤: {str(e)}")

        return None

	•	API Key 驗證：從 st.session_state 中取得 API Key，如果不存在則提示用戶輸入。
	•	API 請求構建與發送：發送查詢請求，並設定預設參數（如格式、輸出方式）。
	•	結果處理：若請求成功，會展示不同類型的內容（文字或圖像）並顯示查詢耗時。
	•	錯誤處理：包括 API 請求錯誤、JSON 解析錯誤和其他未知錯誤。

3. 主頁面函數 show_practice_page

def show_practice_page():
    st.title("🎯 Wolfram Alpha API 實戰演練")

    mode = st.sidebar.radio(
        "選擇練習模式", ["🎨 引導式練習", "🚀 自由實戰", "📚 範例庫", "🏆 挑戰模式"]
    )

    if mode == "🎨 引導式練習":
        show_guided_practice()
    elif mode == "🚀 自由實戰":
        show_free_practice()
    elif mode == "📚 範例庫":
        show_example_library()
    else:
        show_challenge_mode()

	•	顯示頁面標題：「Wolfram Alpha API 實戰演練」。
	•	模式選擇：側邊欄提供四種練習模式，分別是「引導式練習」、「自由實戰」、「範例庫」和「挑戰模式」。依照選擇呼叫對應的處理函數。

4. 各種練習模式函數

4.1 show_guided_practice - 引導式練習

這部分幫助用戶選擇特定的練習主題，如數學計算器、數據分析工具、科學計算助手等。

def show_guided_practice():
    st.header("引導式練習")

    topic = st.selectbox(
        "選擇練習主題",
        ["數學計算器", "數據分析工具", "科學計算助手", "生活應用助手", "教育輔助工具"],
        key="guided_topic",
    )

    if topic == "數學計算器":
        show_math_calculator()
    elif topic == "數據分析工具":
        show_data_analysis()
    elif topic == "科學計算助手":
        show_science_calculator()
    elif topic == "生活應用助手":
        show_life_assistant()
    else:
        show_education_tools()

	•	主題選擇：提供用戶選擇不同的主題，每個主題會進一步引導到更具體的練習內容。

4.2 show_math_calculator - 數學計算器

數學計算器提供不同的數學計算功能，如方程求解、微積分計算、統計分析和幾何圖形生成。

def show_math_calculator():
    st.subheader("🔮 數學魔法計算器")
    # 確保有 API Key
    # 選擇數學計算類型和進行計算
    # 提供可視化選項

這個函數讓用戶選擇數學類型，例如解方程、求導數和積分等。執行查詢並顯示結果時會檢查 API Key 是否已輸入。

4.3 其他工具函數

	•	show_calculus_wizard：微積分魔術師，提供導數、積分和極限的計算。
	•	show_data_analysis：數據分析工具，用於分析特定地點的經濟、人口或氣候數據。
	•	show_science_calculator：科學計算助手，針對物理、化學、生物等領域進行計算。
	•	show_life_assistant：生活應用助手，包括天氣查詢、貨幣轉換等實用工具。
	•	show_education_tools：教育輔助工具，幫助學生學習不同學科的主題。

5. 自由實戰 - show_free_practice

該模式允許用戶自由輸入查詢內容和參數，進行任何類型的 Wolfram Alpha API 測試。

def show_free_practice():
    st.header("自由實戰")
    # 提示用戶自由測試任何查詢
    # 用戶可以設置格式選項和超時
    # 執行查詢並顯示結果

此模式允許高度自訂，適合進行自由查詢測試。

6. 範例庫 - show_example_library

該函數展示不同類型的查詢範例，用戶可以選擇並執行這些範例，了解 API 的使用方式。

def show_example_library():
    st.header("範例庫")
    # 顯示範例分類和具體範例
    # 用戶可以查看範例查詢和說明
    # 點擊執行範例

此功能讓用戶從預定義範例中學習 API 的使用方式和應用範圍。

7. 挑戰模式 - show_challenge_mode

挑戰模式提供不同難度的挑戰，鼓勵用戶逐步完成任務，測試和提高自己的查詢技能。


'''
import streamlit as st
import requests
import json
import time
from typing import Dict, Any


def execute_query(query: str, context: str, params: Dict[str, Any] = None):
    """執行 API 查詢並返回結果"""
    api_key = st.session_state.get("wolfram_api_key")
    if not api_key:
        st.error("請先輸入 API Key!")
        return

    with st.spinner("處理中..."):
        try:
            # 構建 API 請求
            base_url = "http://api.wolframalpha.com/v2/query"
            default_params = {
                "appid": api_key,
                "input": query,
                "format": "plaintext,image",
                "output": "json",
            }

            # 合併自定義參數
            if params:
                default_params.update(params)

            # 發送請求
            response = requests.get(base_url, params=default_params)
            response.raise_for_status()
            result = response.json()

            # 檢查響應
            if "queryresult" in result:
                queryresult = result["queryresult"]

                if queryresult.get("success"):
                    # 創建結果顯示區
                    st.success(f"✨ {context}查詢成功!")

                    # 顯示結果
                    for pod in queryresult.get("pods", []):
                        st.subheader(pod.get("title", ""))
                        for subpod in pod.get("subpods", []):
                            # 顯示文本結果
                            if subpod.get("plaintext"):
                                st.write(subpod["plaintext"])

                            # 顯示圖片結果
                            if "img" in subpod:
                                st.image(
                                    subpod["img"]["src"],
                                    caption=pod.get("title", ""),
                                    use_column_width=True,
                                )

                    # 顯示計算時間
                    st.info(f"計算耗時: {queryresult.get('timing', 'N/A')} 秒")

                    # 返回完整結果供進一步處理
                    return queryresult
                else:
                    st.warning("未找到結果!")
                    if "tips" in queryresult:
                        st.info(
                            "💡 提示: "
                            + "\n".join(
                                tip.get("text", "") for tip in queryresult["tips"]
                            )
                        )
            else:
                st.error("無效的響應格式!")

        except requests.RequestException as e:
            st.error(f"API 請求錯誤: {str(e)}")
        except json.JSONDecodeError:
            st.error("響應解析錯誤!")
        except Exception as e:
            st.error(f"發生未知錯誤: {str(e)}")

        return None


def show_practice_page():
    st.title("🎯 Wolfram Alpha API 實戰演練")

    # 選擇練習模式
    mode = st.sidebar.radio(
        "選擇練習模式", ["🎨 引導式練習", "🚀 自由實戰", "📚 範例庫", "🏆 挑戰模式"]
    )

    if mode == "🎨 引導式練習":
        show_guided_practice()
    elif mode == "🚀 自由實戰":
        show_free_practice()
    elif mode == "📚 範例庫":
        show_example_library()
    else:
        show_challenge_mode()


def show_guided_practice():
    st.header("引導式練習")

    # 練習主題選擇
    topic = st.selectbox(
        "選擇練習主題",
        ["數學計算器", "數據分析工具", "科學計算助手", "生活應用助手", "教育輔助工具"],
        key="guided_topic",
    )

    # 根據主題顯示不同的練習內容
    if topic == "數學計算器":
        show_math_calculator()
    elif topic == "數據分析工具":
        show_data_analysis()
    elif topic == "科學計算助手":
        show_science_calculator()
    elif topic == "生活應用助手":
        show_life_assistant()
    else:
        show_education_tools()


def show_math_calculator():
    st.subheader("🔮 數學魔法計算器")

    # 確保有 API Key
    if "wolfram_api_key" not in st.session_state:
        api_key = st.text_input(
            "請輸入你的 Wolfram API Key:", type="password", key="api_key_input"
        )
        if api_key:
            st.session_state.wolfram_api_key = api_key
        else:
            st.warning("請先輸入 API Key 才能使用計算器")
            return
    # 添加創意介紹
    st.markdown(
        """
    <div class='magic-intro'>
        歡迎來到數學魔法世界！在這裡，複雜的數學問題將變得簡單而有趣。
        讓我們一起探索數學的奧秘吧！
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 使用動態效果選擇數學類型
    math_type = st.selectbox(
        "✨ 選擇你的數學魔法",
        ["🎯 神奇方程求解器", "📊 微積分魔術師", "🎲 統計預言家", "📐 幾何圖形生成器"],
        key="math_type",
    )

    if math_type == "🎯 神奇方程求解器":
        show_equation_solver()
    elif math_type == "📊 微積分魔術師":
        show_calculus_wizard()
    elif math_type == "🎲 統計預言家":
        show_statistics_prophet()
    else:
        show_geometry_generator()


def show_equation_solver():
    st.markdown(
        """
    ### 🎯 神奇方程求解器
    
    讓我們來解決一些有趣的方程！以下是一些魔法咒語（方程示例）：
    
    1. `solve x^2 + 5x + 6 = 0`  (二次方程)
    2. `solve system {x + y = 5, 2x - y = 3}`  (方程組)
    3. `solve x^3 - 6x^2 + 11x - 6 = 0`  (三次方程)
    """
    )

    example_type = st.radio(
        "選擇方程類型", ["基礎方程", "方程組", "高次方程"], key="eq_type"
    )

    if example_type == "基礎方程":
        equation = st.text_input(
            "輸入你的方程:", value="x^2 + 5x + 6 = 0", key="basic_eq"
        )
    elif example_type == "方程組":
        col1, col2 = st.columns(2)
        with col1:
            eq1 = st.text_input("方程 1:", value="x + y = 5", key="eq1")
        with col2:
            eq2 = st.text_input("方程 2:", value="2x - y = 3", key="eq2")
        equation = f"solve system {{{eq1}, {eq2}}}"
    else:
        equation = st.text_input(
            "輸入高次方程:", value="x^3 - 6x^2 + 11x - 6 = 0", key="high_eq"
        )

    # 添加可視化選項
    show_visual = st.checkbox("顯示圖形解釋", value=True)

    if st.button("✨ 施展解方程魔法", key="solve_eq"):
        with st.spinner("魔法正在生效..."):
            # 執行 API 調用
            execute_query(equation, "方程求解")

            if show_visual:
                if example_type == "基礎方程":
                    # 添加二次函數圖像
                    visual_query = f"plot {equation.split('=')[0]} from x=-10 to 10"
                    execute_query(visual_query, "函數圖像")


def show_calculus_wizard():
    st.markdown(
        """
    ### 📊 微積分魔術師
    
    探索微積分的神奇世界！試試這些魔法：
    
    1. 🔄 導數：了解函數的變化率
    2. ∫ 積分：計算曲線下的面積
    3. 🎯 極限：探索無窮的奧秘
    """
    )

    calc_type = st.radio(
        "選擇微積分魔法", ["🔄 求導數", "∫ 計算積分", "🎯 求極限"], key="calc_type"
    )

    # 提供常用函數示例
    examples = {
        "🔄 求導數": {
            "簡單函數": "d/dx(x^2)",
            "三角函數": "d/dx(sin(x))",
            "複合函數": "d/dx(e^x * sin(x))",
        },
        "∫ 計算積分": {
            "基本積分": "integrate x^2 dx",
            "定積分": "integrate x^2 from 0 to 1",
            "三角積分": "integrate sin(x) dx",
        },
        "🎯 求極限": {
            "基本極限": "limit(sin(x)/x) as x->0",
            "無窮極限": "limit(1/x) as x->infinity",
            "分式極限": "limit((x^2-1)/(x-1)) as x->1",
        },
    }

    example = st.selectbox(
        "選擇一個示例", examples[calc_type].keys(), key="calc_example"
    )

    expression = st.text_input(
        "輸入表達式:", value=examples[calc_type][example], key="calc_expression"
    )

    col1, col2 = st.columns(2)

    with col1:
        show_steps = st.checkbox("顯示計算步驟", value=True)

    with col2:
        show_graph = st.checkbox("顯示函數圖像", value=True)

    if st.button("🌟 施展微積分魔法", key="calc_magic"):
        with st.spinner("正在施展魔法..."):
            # 執行主要計算
            execute_query(expression, "微積分計算")

            # 顯示步驟（如果選擇了的話）
            if show_steps:
                if calc_type == "🔄 求導數":
                    step_query = f"step-by-step derivative of {expression}"
                elif calc_type == "∫ 計算積分":
                    step_query = f"step-by-step integration of {expression}"
                else:
                    step_query = f"step-by-step limit of {expression}"
                execute_query(step_query, "計算步驟")

            # 顯示圖像（如果選擇了的話）
            if show_graph:
                # 從表達式中提取函數部分並繪圖
                plot_query = f"plot {expression} from -5 to 5"
                execute_query(plot_query, "函數圖像")


def show_data_analysis():
    st.subheader("數據分析工具")

    data_type = st.selectbox(
        "選擇數據類型",
        ["經濟數據", "人口統計", "氣候數據", "社會指標"],
        key="data_type",
    )

    location = st.text_input("輸入地點:", key="location")

    time_range = st.select_slider(
        "選擇時間範圍",
        options=["1年", "5年", "10年", "20年", "50年"],
        value="5年",
        key="time_range",
    )

    if st.button("分析數據", key="analyze_data"):
        query = f"{data_type} of {location} over {time_range}"
        execute_query(query, "數據分析")


def show_science_calculator():
    st.subheader("科學計算助手")

    science_type = st.selectbox(
        "選擇科學領域", ["物理", "化學", "生物", "天文"], key="science_type"
    )

    if science_type == "物理":
        physics_calc = st.selectbox(
            "選擇計算類型", ["力學", "電磁學", "熱力學", "光學"], key="physics_calc"
        )

        values = st.text_input("輸入計算值 (用逗號分隔):", key="physics_values")

        if st.button("計算", key="physics_calc_button"):
            execute_query(f"{physics_calc} calculation {values}", "物理計算")


def show_life_assistant():
    st.subheader("生活應用助手")

    app_type = st.selectbox(
        "選擇應用類型", ["天氣查詢", "貨幣轉換", "時區轉換", "營養計算"], key="app_type"
    )

    if app_type == "天氣查詢":
        location = st.text_input("輸入地點:", key="weather_location")
        days = st.slider("預測天數", 1, 7, 3, key="weather_days")

        if st.button("查詢天氣", key="weather_button"):
            execute_query(f"weather forecast {location} {days} days", "天氣查詢")

    elif app_type == "貨幣轉換":
        amount = st.number_input(
            "輸入金額:", min_value=0.0, value=100.0, key="currency_amount"
        )
        from_currency = st.selectbox(
            "從:", ["USD", "EUR", "JPY", "TWD"], key="from_currency"
        )
        to_currency = st.selectbox(
            "轉換至:", ["EUR", "USD", "JPY", "TWD"], key="to_currency"
        )

        if st.button("轉換", key="convert_button"):
            execute_query(
                f"convert {amount} {from_currency} to {to_currency}", "貨幣轉換"
            )


def show_education_tools():
    st.subheader("教育輔助工具")

    subject = st.selectbox("選擇學科", ["數學", "物理", "化學", "生物"], key="subject")

    level = st.select_slider(
        "選擇難度等級", options=["初級", "中級", "高級"], value="中級", key="level"
    )

    topic = st.text_input("輸入具體主題:", key="edu_topic")

    if st.button("生成練習", key="generate_practice"):
        execute_query(f"{subject} {topic} {level} level", "教育輔助")


def show_free_practice():
    st.header("自由實戰")
    if "wolfram_api_key" not in st.session_state:
        api_key = st.text_input(
            "請輸入你的 Wolfram API Key:", type="password", key="api_key_input"
        )
        if api_key:
            st.session_state.wolfram_api_key = api_key
        else:
            st.warning("請先輸入 API Key 才能使用")
            return

    st.markdown(
        """
   在這裡，你可以自由發揮，測試任何 Wolfram Alpha API 的功能。
   
   ### 提示：
   1. 注意參數的使用
   2. 嘗試不同的查詢格式
   3. 觀察返回結果
   """
    )

    # API Key 輸入
    api_key = st.text_input("API Key:", type="password", key="free_api_key")

    # 查詢輸入
    query = st.text_area("輸入你的查詢:", height=100, key="free_query")

    # 參數設置
    with st.expander("高級參數設置"):
        format_option = st.multiselect(
            "選擇輸出格式",
            ["plaintext", "image", "mathml", "sound"],
            default=["plaintext", "image"],
            key="free_format",
        )

        units = st.radio("單位系統", ["metric", "imperial"], key="free_units")

        timeout = st.slider("超時設置 (秒)", 1, 20, 5, key="free_timeout")

    if st.button("執行查詢", key="free_execute"):
        params = {
            "appid": api_key,
            "input": query,
            "format": ",".join(format_option),
            "units": units,
            "timeout": timeout,
        }
        execute_query(query, "自由實戰", params)


def show_example_library():
    st.header("範例庫")

    # 範例分類
    category = st.selectbox(
        "選擇範例分類",
        ["數學計算範例", "科學計算範例", "數據分析範例", "生活應用範例"],
        key="example_category",
    )

    examples = get_examples(category)

    # 顯示範例
    example = st.selectbox("選擇範例", examples.keys(), key="example_select")

    # 顯示範例詳情
    st.markdown("### 範例詳情")
    st.code(examples[example]["query"], language="python")
    st.markdown(examples[example]["description"])

    if st.button("運行範例", key="run_example"):
        execute_query(
            examples[example]["query"], "範例執行", examples[example].get("params", {})
        )


def show_challenge_mode():
    st.header("挑戰模式")

    st.markdown(
        """
   在挑戰模式中，你將面對一系列逐漸增加難度的任務。
   完成每個任務將獲得積分，解鎖新的挑戰！
   """
    )

    # 選擇挑戰級別
    level = st.selectbox(
        "選擇挑戰級別",
        ["初級挑戰", "中級挑戰", "高級挑戰", "專家挑戰"],
        key="challenge_level",
    )

    challenges = get_challenges(level)

    # 顯示當前挑戰
    current_challenge = st.selectbox(
        "選擇挑戰", challenges.keys(), key="current_challenge"
    )

    # 顯示挑戰詳情
    st.markdown("### 挑戰詳情")
    st.markdown(challenges[current_challenge]["description"])
    st.markdown("**目標：**")
    st.markdown(challenges[current_challenge]["goal"])

    # 提交解答
    solution = st.text_area("輸入你的解答:", height=100, key="challenge_solution")

    if st.button("提交解答", key="submit_challenge"):
        check_challenge_solution(solution, challenges[current_challenge])


def get_examples(category: str) -> Dict[str, Dict[str, str]]:
    """獲取範例庫"""
    # 這裡可以從配置文件或數據庫讀取範例
    return {
        "基礎例子": {"query": "2 + 2", "description": "基礎數學計算示例", "params": {}},
        # 更多範例...
    }


def get_challenges(level: str) -> Dict[str, Dict[str, str]]:
    """獲取挑戰題目"""
    # 這裡可以從配置文件或數據庫讀取挑戰
    return {
        "挑戰 1": {
            "description": "使用 API 計算複雜的數學表達式",
            "goal": "計算 (sin(x) + cos(x))^2 在 x = π/4 時的值",
            "solution": "1",
        },
        # 更多挑戰...
    }


def check_challenge_solution(solution: str, challenge: Dict[str, str]):
    """檢查挑戰解答"""
    # 實現解答檢查邏輯
    st.info("解答已提交，正在評估...")
    time.sleep(1)
    if solution.strip() == challenge["solution"]:
        st.success("恭喜！解答正確！")
    else:
        st.error("解答不正確，請重試！")


if __name__ == "__main__":
    show_practice_page()
