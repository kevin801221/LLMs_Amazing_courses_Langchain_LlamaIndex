# pages/export.py

import streamlit as st
import pandas as pd
import json
import csv
from datetime import datetime
from io import StringIO
import plotly.express as px
from typing import Dict, Any, List

class DataExporter:
    def __init__(self):
        self.supported_formats = ["CSV", "JSON", "PDF"]
        
    def export_data(self, data: Any, format: str) -> bytes:
        """根據選擇的格式導出數據"""
        if format == "CSV":
            return self.to_csv(data)
        elif format == "JSON":
            return self.to_json(data)
        elif format == "PDF":
            return self.to_pdf(data)
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def to_csv(self, data: pd.DataFrame) -> bytes:
        return data.to_csv(index=False).encode('utf-8')
    
    def to_json(self, data: pd.DataFrame) -> bytes:
        return data.to_json(orient='records').encode('utf-8')
    
    def to_pdf(self, data: pd.DataFrame) -> bytes:
        # 需要安裝 pdfkit
        import pdfkit
        
        # 創建 HTML
        html = data.to_html()
        
        # 轉換為 PDF
        pdf = pdfkit.from_string(html, False)
        return pdf

class ReportGenerator:
    def __init__(self):
        self.report_types = {
            "學習進度報告": self.generate_progress_report,
            "練習完成報告": self.generate_exercise_report,
            "API 使用報告": self.generate_api_usage_report
        }
    
    def generate_report(self, report_type: str, user_id: str) -> pd.DataFrame:
        """生成指定類型的報告"""
        if report_type not in self.report_types:
            raise ValueError(f"不支持的報告類型: {report_type}")
            
        return self.report_types[report_type](user_id)
    
    def generate_progress_report(self, user_id: str) -> pd.DataFrame:
        """生成學習進度報告"""
        # 這裡應該從數據庫獲取實際數據
        data = {
            "日期": pd.date_range(start="2024-01-01", periods=10),
            "完成課程": range(1, 11),
            "獲得積分": [10, 20, 15, 25, 30, 35, 20, 25, 30, 40]
        }
        return pd.DataFrame(data)
    
    def generate_exercise_report(self, user_id: str) -> pd.DataFrame:
        """生成練習完成報告"""
        # 示例數據
        data = {
            "練習名稱": ["基礎API調用", "參數配置", "結果解析"],
            "完成時間": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "得分": [90, 85, 95],
            "用時(分鐘)": [20, 30, 25]
        }
        return pd.DataFrame(data)
    
    def generate_api_usage_report(self, user_id: str) -> pd.DataFrame:
        """生成 API 使用報告"""
        # 示例數據
        data = {
            "日期": pd.date_range(start="2024-01-01", periods=7),
            "調用次數": [50, 45, 60, 55, 70, 65, 80],
            "平均響應時間": [0.5, 0.6, 0.4, 0.5, 0.3, 0.4, 0.5]
        }
        return pd.DataFrame(data)

def show_export_page():
    st.title("數據導出")
    
    # 初始化導出器和報告生成器
    exporter = DataExporter()
    report_generator = ReportGenerator()
    
    # 選擇報告類型
    report_type = st.selectbox(
        "選擇報告類型",
        list(report_generator.report_types.keys())
    )
    
    # 選擇導出格式
    export_format = st.selectbox(
        "選擇導出格式",
        exporter.supported_formats
    )
    
    # 日期範圍選擇
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("開始日期")
    with col2:
        end_date = st.date_input("結束日期")
    
    # 生成預覽
    if st.button("生成報告預覽"):
        try:
            # 生成報告數據
            data = report_generator.generate_report(
                report_type, 
                st.session_state.get("user")
            )
            
            # 顯示預覽
            st.subheader("報告預覽")
            st.dataframe(data)
            
            # 顯示圖表
            show_report_visualization(data, report_type)
            
            # 創建下載按鈕
            st.download_button(
                label=f"下載 {export_format} 報告",
                data=exporter.export_data(data, export_format),
                file_name=f"report_{datetime.now().strftime('%Y%m%d')}.{export_format.lower()}",
                mime=f"text/{export_format.lower()}"
            )
            
        except Exception as e:
            st.error(f"生成報告時發生錯誤: {str(e)}")

def show_report_visualization(data: pd.DataFrame, report_type: str):
    """根據報告類型顯示相應的可視化"""
    if report_type == "學習進度報告":
        fig = px.line(
            data,
            x="日期",
            y="獲得積分",
            title="學習進度趨勢"
        )
        st.plotly_chart(fig)
        
    elif report_type == "練習完成報告":
        fig = px.bar(
            data,
            x="練習名稱",
            y="得分",
            title="練習得分分布"
        )
        st.plotly_chart(fig)
        
    elif report_type == "API 使用報告":
        fig = px.line(
            data,
            x="日期",
            y="調用次數",
            title="API 調用趨勢"
        )
        st.plotly_chart(fig)

if __name__ == "__main__":
    show_export_page()