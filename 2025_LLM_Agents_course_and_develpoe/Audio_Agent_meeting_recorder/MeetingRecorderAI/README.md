# 智能會議記錄助手

自動記錄會議內容，識別說話者，並生成摘要與行動項目。

## 功能特點

- **即時語音轉文字**：使用 Deepgram API 將會議語音轉為文字
- **說話者識別**：自動區分不同的發言者（可選功能）
- **會議摘要生成**：使用 GPT-4o 生成會議內容摘要
- **行動項目提取**：自動提取會議中的任務和責任分配
- **會議記錄儲存**：將會議記錄儲存為結構化 JSON 資料
- **報告匯出**：支援 Markdown 和 JSON 格式匯出完整會議記錄
- **命令行操作**：通過特殊指令控制各項功能

## 環境設定

1. 克隆本專案
2. 安裝依賴套件：

```bash
pip install deepgram-sdk python-dotenv langchain langchain-openai
```

3. 創建 `.env` 檔案，填入你的 API 金鑰：

```
DEEPGRAM_API_KEY=your_deepgram_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## 使用方法

執行主程式：

```bash
python main.py
```

### 命令行參數

可以使用以下命令行參數:

```bash
python main.py [選項]

選項:
  --no-speaker       啟動時預設不啟用說話者識別
  --title TITLE      設定會議標題
  --participants PARTICIPANTS
                     設定參與者列表 (逗號分隔)
  --no-summary       不生成會議摘要和行動項目
```

例如：

```bash
python main.py --title "專案進度會議" --participants "張三,李四,王五" --no-speaker
```

### 互動式命令

程式運行後，可以使用以下指令控制程式：

- `help` - 顯示幫助信息
- `start` - 開始錄音
- `stop` - 停止錄音
- `speaker on/off` - 開啟/關閉說話者識別功能
- `summary on/off` - 開啟/關閉會議摘要生成功能
- `export [markdown/json]` - 匯出會議記錄
- `exit` - 退出程式

### 語音控制

在錄音過程中，你也可以通過說出以下關鍵詞來停止錄音：
- 「停止」
- 「停止錄音」
- 「結束」
- 「結束錄音」
- 「stop」
- 「end」

另外，在錄音時按鍵盤上的 `q` 鍵也可以停止錄音。

## 典型使用流程

1. 啟動程式並設定會議信息
2. 輸入 `speaker on` 開啟說話者識別功能（如需要）
3. 輸入 `start` 開始錄音
4. 進行會議討論
5. 說「停止錄音」或輸入 `stop` 停止錄音
6. 系統自動生成會議摘要和提取行動項目
7. 輸入 `export markdown` 或 `export json` 匯出會議報告
8. 輸入 `exit` 退出程式

## 專案結構

- `core/speech_to_text.py`：語音轉文字元件
- `core/speaker_recognition.py`：說話者識別元件
- `core/database.py`：資料庫操作元件
- `core/ai_processor.py`：AI 處理元件
- `core/command_parser.py`：命令解析元件
- `main.py`：主程式入口點

## 注意事項

- 中文語音識別的準確度可能受環境、口音等因素影響
- 確保麥克風正常工作
- 良好的錄音環境可以提高轉錄準確性
- 每個說話者說話前最好有明顯的停頓，以幫助系統更好地區分不同說話者
- 說話者識別功能需要手動開啟，預設為關閉狀態