'''
這個統計學習助手包含以下功能：

1. 圖形分析：
   - 直方圖
   - 箱形圖
   - 散點圖
   - 密度圖

2. 描述統計：
   - 集中趨勢
   - 離散程度
   - 分布形狀
   - 位置統計量

3. 機率分布：
   - 常態分布
   - 均勻分布
   - 二項分布
   - 泊松分布

4. 數據關係：
   - 相關係數
   - 散點圖
   - 線性回歸
   - 趨勢分析

5. 機率計算：
   - 各類分布機率
   - 累積機率
   - 區間機率

6. 隨機數生成：
   - 多種分布
   - 可視化結果
   - 統計分析

使用方式：
1. 運行程式
2. 設置 API Key
3. 選擇功能標籤頁
4. 輸入數據
5. 查看分析結果
'''
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from scipy import stats

class WolframStatAPI:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = "http://api.wolframalpha.com/v2/query"

    def query(self, input_text: str) -> dict:
        """執行 Wolfram API 查詢"""
        params = {
            "appid": self.app_id,
            "input": input_text,
            "format": "plaintext,image",
            "output": "json"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def initialize_session_state():
    """初始化 session state"""
    if 'api' not in st.session_state:
        st.session_state.api = None
    if 'wolfram_api_key' not in st.session_state:
        st.session_state.wolfram_api_key = None
    if 'data' not in st.session_state:
        st.session_state.data = None

def main():
    st.set_page_config(page_title="統計學習助手", layout="wide")

    # 初始化 session state
    initialize_session_state()

    # 側邊欄 API 設置
    if not st.session_state.api:
        with st.sidebar:
            st.header("⚙️ API 設置")
            api_key = st.text_input("輸入 Wolfram API Key:", type="password")
            if api_key:
                st.session_state.wolfram_api_key = api_key
                st.session_state.api = WolframStatAPI(api_key)
                st.success("✅ API Key 設置成功！")
                st.rerun()

    # 主標題
    st.title("📊 統計學習助手")

    # 主要功能標籤頁
    tabs = st.tabs([
        "📈 圖形分析",
        "📊 描述統計",
        "🔄 機率分布",
        "🔗 數據關係",
        "🎲 機率計算",
        "🔢 隨機數生成"
    ])

    # 圖形分析標籤頁
    with tabs[0]:
        st.header("圖形分析")
        
        # 數據輸入
        data_input = st.text_area(
            "輸入數據 (每個數字用逗號分隔):",
            "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
        )
        
        if data_input:
            try:
                data = [float(x.strip()) for x in data_input.split(",")]
                st.session_state.data = data
                
                # 選擇圖表類型
                chart_type = st.selectbox(
                    "選擇圖表類型",
                    ["直方圖", "箱形圖", "散點圖", "密度圖"]
                )
                
                if chart_type == "直方圖":
                    fig = px.histogram(data, title="數據分布直方圖")
                    st.plotly_chart(fig)
                    
                elif chart_type == "箱形圖":
                    fig = px.box(data, title="數據箱形圖")
                    st.plotly_chart(fig)
                    
                elif chart_type == "散點圖":
                    fig = px.scatter(x=list(range(len(data))), y=data, title="數據散點圖")
                    st.plotly_chart(fig)
                    
                elif chart_type == "密度圖":
                    fig = ff.create_distplot([data], ["數據"], bin_size=.2)
                    st.plotly_chart(fig)
                
            except Exception as e:
                st.error(f"數據格式錯誤: {str(e)}")

    # 描述統計標籤頁
    with tabs[1]:
        st.header("描述統計")
        
        if st.session_state.data:
            data = st.session_state.data
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("平均值", f"{np.mean(data):.2f}")
                st.metric("標準差", f"{np.std(data):.2f}")
                
            with col2:
                st.metric("中位數", f"{np.median(data):.2f}")
                st.metric("變異係數", f"{(np.std(data)/np.mean(data)):.2f}")
                
            with col3:
                st.metric("最小值", f"{min(data):.2f}")
                st.metric("最大值", f"{max(data):.2f}")
            
            # 百分位數
            st.subheader("百分位數")
            percentiles = [25, 50, 75]
            for p in percentiles:
                st.metric(f"{p}th 百分位數", f"{np.percentile(data, p):.2f}")
            
            # 偏度與峰度
            st.subheader("形狀統計量")
            st.metric("偏度", f"{stats.skew(data):.2f}")
            st.metric("峰度", f"{stats.kurtosis(data):.2f}")

    # 機率分布標籤頁
    with tabs[2]:
        st.header("機率分布")
        
        dist_type = st.selectbox(
            "選擇分布類型",
            ["常態分布", "均勻分布", "二項分布", "泊松分布"]
        )
        
        if dist_type == "常態分布":
            mu = st.number_input("平均值 (μ)", value=0.0)
            sigma = st.number_input("標準差 (σ)", value=1.0, min_value=0.1)
            
            if st.button("生成分布"):
                x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
                y = stats.norm.pdf(x, mu, sigma)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='PDF'))
                fig.update_layout(title="常態分布 PDF")
                st.plotly_chart(fig)
                
                # 計算常用機率
                st.subheader("常用機率")
                st.write(f"P(X < μ+σ) = {stats.norm.cdf(mu+sigma, mu, sigma):.4f}")
                st.write(f"P(X < μ+2σ) = {stats.norm.cdf(mu+2*sigma, mu, sigma):.4f}")
                st.write(f"P(X < μ+3σ) = {stats.norm.cdf(mu+3*sigma, mu, sigma):.4f}")

    # 數據關係標籤頁
    with tabs[3]:
        st.header("數據關係")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_data = st.text_input("X 變數 (逗號分隔):", "1,2,3,4,5")
            
        with col2:
            y_data = st.text_input("Y 變數 (逗號分隔):", "2,4,6,8,10")
            
        try:
            x = [float(i.strip()) for i in x_data.split(",")]
            y = [float(i.strip()) for i in y_data.split(",")]
            
            if len(x) == len(y):
                # 相關係數
                correlation = np.corrcoef(x, y)[0,1]
                st.metric("相關係數", f"{correlation:.4f}")
                
                # 散點圖
                fig = px.scatter(x=x, y=y, trendline="ols")
                st.plotly_chart(fig)
                
                # 線性回歸
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                st.write(f"線性回歸方程: y = {slope:.2f}x + {intercept:.2f}")
                st.write(f"R-squared: {r_value**2:.4f}")
                st.write(f"P-value: {p_value:.4f}")
                
            else:
                st.error("X 和 Y 的數據長度不一致")
                
        except Exception as e:
            st.error(f"數據格式錯誤: {str(e)}")

    # 機率計算標籤頁
    with tabs[4]:
        st.header("機率計算")
        
        prob_type = st.selectbox(
            "選擇計算類型",
            ["二項分布機率", "常態分布機率", "泊松分布機率"]
        )
        
        if prob_type == "二項分布機率":
            n = st.number_input("試驗次數 (n)", min_value=1, value=10)
            p = st.number_input("成功機率 (p)", min_value=0.0, max_value=1.0, value=0.5)
            k = st.number_input("成功次數 (k)", min_value=0, max_value=n, value=5)
            
            if st.button("計算機率"):
                prob = stats.binom.pmf(k, n, p)
                st.success(f"P(X = {k}) = {prob:.4f}")
                
                # 繪製機率分布圖
                x = np.arange(0, n+1)
                y = stats.binom.pmf(x, n, p)
                
                fig = go.Figure(data=go.Bar(x=x, y=y))
                fig.update_layout(title="二項分布機率質量函數")
                st.plotly_chart(fig)

    # 隨機數生成標籤頁
    with tabs[5]:
        st.header("隨機數生成")
        
        random_type = st.selectbox(
            "選擇隨機數類型",
            ["均勻分布", "常態分布", "指數分布"]
        )
        
        size = st.number_input("生成數量", min_value=1, value=100)
        
        if random_type == "均勻分布":
            low = st.number_input("最小值", value=0.0)
            high = st.number_input("最大值", value=1.0)
            
            if st.button("生成"):
                numbers = np.random.uniform(low, high, size)
                
                st.write("生成的隨機數:")
                st.write(numbers)
                
                fig = px.histogram(numbers, title="隨機數分布")
                st.plotly_chart(fig)

if __name__ == "__main__":
    main()
