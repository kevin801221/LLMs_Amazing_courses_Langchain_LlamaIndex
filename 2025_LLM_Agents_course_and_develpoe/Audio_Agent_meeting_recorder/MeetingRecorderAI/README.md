# 智能會議記錄助手

一個功能強大的會議記錄工具，能夠自動識別不同說話者，生成會議摘要，並提取行動項目。

## 功能特點

- 🎙️ 實時語音轉文字
- 👥 自動識別不同說話者
- 📝 生成會議摘要
- ✅ 提取行動項目
- 📊 生成說話者統計
- 💾 匯出會議記錄 (Markdown 或 JSON 格式)

## 安裝說明

1. 克隆此存儲庫
2. 安裝所需依賴項：

```bash
pip install -r requirements.txt
```

3. 創建 `.env` 文件並添加您的 API 密鑰：

```
DEEPGRAM_API_KEY=your_deepgram_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## 使用方法

1. 運行應用程序：

```bash
streamlit run meeting_recorder.py
```

2. 在瀏覽器中打開顯示的 URL（通常是 http://localhost:8501）
3. 在側邊欄設置會議標題和參與者
4. 點擊「開始記錄」按鈕
5. 開始您的會議
6. 完成後點擊「停止記錄」
7. 點擊「生成報告」獲取會議摘要和行動項目
8. 可以匯出會議記錄為 Markdown 或 JSON 格式

## 系統要求

- Python 3.8 或更高版本
- 麥克風
- 互聯網連接（用於 API 調用）
- FFplay（用於音頻播放，可選）

## API 密鑰

此應用程序需要以下 API 密鑰：

- [Deepgram API](https://deepgram.com/) - 用於語音識別和說話者區分
- [OpenAI API](https://openai.com/) - 用於生成摘要和提取行動項目

## 技術細節

- **語音識別**：使用 Deepgram 的 Nova-2 模型進行實時語音轉文字和說話者區分
- **AI 處理**：使用 OpenAI 的 GPT-4o 模型生成會議摘要和提取行動項目
- **前端**：使用 Streamlit 構建用戶界面
- **數據處理**：使用 LangChain 處理和分析文本數據

## 注意事項

- 說話者識別的準確性取決於音頻質量和說話者之間的聲音差異
- 為獲得最佳效果，請使用高質量麥克風並確保每個說話者聲音清晰
- 在嘈雜環境中，說話者識別的準確性可能會降低
