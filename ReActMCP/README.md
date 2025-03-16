以下是 ReActMCP Web Search 的 繁體中文 版本 Markdown 文件：

# ReActMCP 網頁搜尋工具

ReActMCP Web Search 是一個 MCP（Model Context Protocol）伺服器，將網頁搜尋功能整合到您的 AI 助理框架中。它利用 **Exa API** 來執行基礎與進階網頁搜尋，並返回即時的 **Markdown 格式結果**，包含標題、URL、發布日期及內容摘要。

這個專案屬於更廣泛的 **ReActMCP** 計畫的一部分，該計畫旨在連接多種 MCP 工具與伺服器，以增強您的 AI 助理的功能。

---

## 📌 目錄

- [功能特色](#功能特色)
- [系統需求](#系統需求)
- [安裝方式](#安裝方式)
- [配置設定](#配置設定)
  - [環境變數](#環境變數)
  - [MCP 設定](#mcp-設定)
  - [系統提示詞](#系統提示詞)
- [使用方式](#使用方式)
  - [啟動網頁搜尋伺服器](#啟動網頁搜尋伺服器)
  - [測試工具](#測試工具)
- [個性化與自訂](#個性化與自訂)
- [疑難排解](#疑難排解)
- [許可證](#許可證)
- [貢獻指南](#貢獻指南)

---

## 📌 功能特色

- **基礎網頁搜尋**：透過 Exa API 進行一般性網頁搜尋。
- **進階網頁搜尋**：可使用篩選條件，例如特定網域、包含關鍵字、日期篩選等。
- **Markdown 格式輸出**：搜尋結果以 Markdown 格式呈現，包含標題、URL、摘要等，方便整合。
- **MCP 整合**：可輕鬆將此工具加入 MCP 伺服器生態系統，打造多功能 AI 助理。

---

## 📌 系統需求

- **Python 3.8+**
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [exa_py](https://github.com/your-org/exa_py)（Exa API 客戶端）
- 其他 MCP 框架所需的相依套件

---

## 📌 安裝方式

### **1. 克隆（Clone）專案**

```bash
git clone https://github.com/mshojaei77/ReActMCP.git
cd ReActMCP

2. 創建虛擬環境（可選，但建議）

python -m venv venv
source venv/bin/activate  # Windows 使用: venv\Scripts\activate

3. 安裝相依套件

pip install -r requirements.txt

📌 配置設定

環境變數

在專案根目錄中建立 .env 文件，並設定以下變數：

EXA_API_KEY=your_exa_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

Exa API 金鑰 (EXA_API_KEY) 是執行網頁搜尋所需的。

MCP 設定

MCP 設定檔 mcp_config.json 定義了可用的工具與伺服器參數，範例如下：

{
  "websearch": {
    "script": "web_search.py",
    "encoding_error_handler": "ignore",
    "description": "透過 Exa API 進行即時網頁搜尋，支援進階篩選（包含特定網域、關鍵字、日期等），返回標題、URL、發布日期與內容摘要。",
    "required_env_vars": ["EXA_API_KEY"],
    "active": true
  },
  "settings": {
    "model": "gpt-4o",
    "system_prompt_path": "system_prompt.txt"
  }
}

您可以修改此配置，例如 調整預設搜尋結果數量，或 新增 MCP 工具。

系統提示詞（System Prompt）

system_prompt.txt 文件設定 AI 助理的行為與語氣，例如讓回應更友善且富有表情符號 😃。

你是一個知識豐富的 AI 助理，擁有網頁搜尋功能，能夠提供準確、完整、最新的資訊。
請使用有趣、活潑的語氣回應，並加入表情符號以增強互動感。

## 可用搜尋工具
- `search_web`: 執行一般網頁搜尋
- `advanced_search_web`: 進階搜尋，可根據關鍵字、網域或日期篩選結果

## 回應指導方針
1. 若問題涉及最新資訊，請先搜尋再回應。
2. `search_web` 適用於一般查詢，而 `advanced_search_web` 適用於特定需求（如限制來源）。
3. 針對近期資訊，請使用 `max_age_days` 限制搜尋範圍。
4. 若需要鎖定特定來源，可使用 `include_domains` 篩選結果。
5. 引用資訊時，請包含來源 URL。
6. 若搜尋結果矛盾或不足，請誠實告知並解釋現有發現。
7. 組織回應內容，並拆解複雜主題以提高可讀性。
8. 若問題涉及爭議，請提供平衡觀點。
9. 若不確定答案，請透明說明，而不是捏造資訊。

## 回應品質標準
所有回應應清晰、準確，並依據使用者的理解程度量身定制。請善用搜尋功能以確保資訊最新且可靠。

此提示詞可根據需求調整，以符合您的 AI 助理的特定風格與用途。

📌 使用方式

啟動網頁搜尋伺服器

web_search.py 是 MCP 伺服器的主程式，啟動方式如下：

python web_search.py

這將會啟動 MCP 伺服器，提供以下工具：
	•	search_web：一般網頁搜尋
	•	advanced_search_web：進階篩選的網頁搜尋

測試工具

在 web_search.py 中，有一個測試函式 test_search()（目前預設為註解）。您可以取消註解並執行以下指令來測試：

if __name__ == "__main__":
    import asyncio
    # 取消註解以下行以進行測試搜尋
    # asyncio.run(test_search())
    mcp.run()

這將執行測試查詢並返回搜尋結果，幫助您驗證工具是否正常運作。

📌 個性化與自訂

您可以根據需求進行以下個性化設定：
	•	新增 MCP 工具：參考 web_search.py，使用 @mcp.tool() 來新增新的 AI 工具。
	•	調整 mcp_config.json：修改預設參數、啟用/停用工具、變更環境變數設定等。
	•	客製化 AI 助理行為：透過 system_prompt.txt 調整回應語氣、風格與搜尋策略。
	•	修改輸出格式：可調整 format_search_results() 來改變 Markdown 輸出樣式。

📌 疑難排解
	•	找不到 EXA_API_KEY：確保 .env 檔案已正確設置 API 金鑰。
	•	相依套件問題：確認已安裝 requirements.txt 內的所有套件，可嘗試重新安裝：

pip install -r requirements.txt


	•	API 錯誤：檢查網絡連線，確保 Exa API 服務正常運作。

📌 許可證

本專案採用 MIT 授權，詳見 LICENSE 文件。

📌 貢獻指南

歡迎貢獻改進！如有建議、錯誤回報或新功能開發，請提交 issue 或 pull request。

🚀 祝您開發順利，享受打造個人化 AI 助理的樂趣！ 😊

