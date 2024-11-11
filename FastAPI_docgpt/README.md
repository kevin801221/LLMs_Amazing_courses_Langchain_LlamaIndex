📄 文件 GPT - FastAPI 後端

此 FastAPI 後端服務為核心 API，用於處理文件上傳、處理 PDF 檔案、將文件內容嵌入向量資料庫（Qdrant），並允許使用者根據上傳的文件提問。AI 模型使用 OpenAI 的嵌入技術，從文件內容中生成智能回應。

🛠️ 功能特色

	•	PDF 上傳：上傳 PDF 檔案，進行處理並儲存在 Qdrant 向量資料庫中以供查詢。
	•	問答系統：使用者可根據上傳的 PDF 內容提出問題。
	•	API 文件：透過 /docs 提供自動化的 API 文件（Swagger）。

📦 使用的函式庫

	•	FastAPI：用於建立 Web API。
	•	Qdrant Client：用於儲存和檢索文件嵌入資料。
	•	LangChain：用於處理 PDF 和嵌入。
	•	OpenAI：用於生成嵌入和 AI 模型回應。
	•	PyPDFLoader：用於從 PDF 檔案中提取文字。
	•	CORS Middleware：處理跨域資源共享（CORS），允許來自不同網域的前端請求。
	•	dotenv：用於管理環境變數（例如 API 金鑰）。

🗂️ 專案結構

	•	app.py：主要的 FastAPI 應用程式檔案，包含 PDF 上傳和問答系統的 API 端點。
	•	utils.py：包含處理 PDF 檔案、將嵌入發送至向量資料庫，以及從嵌入中檢索答案的實用功能。
	•	環境變數：透過 .env 檔案管理 OpenAI 和 Qdrant 的 API 金鑰。

🚀 快速開始

🔧 先決條件

在設置 FastAPI 後端之前，請確保您已安裝以下內容：

	•	Python 3.7+
	•	Pip（Python 套件管理器）
	•	Qdrant（向量資料庫，可本地運行或使用託管服務）
	•	OpenAI API 金鑰（用於生成嵌入和回應）
	•	虛擬環境（可選但推薦）

🛠️ 安裝與設定

請按照以下步驟在本地機器上設置 FastAPI 後端：

步驟 1：複製儲存庫

git clone <你的儲存庫網址>
cd <你的儲存庫名稱>

步驟 2：建立虛擬環境

建議建立虛擬環境來管理相依性：

python3 -m venv venv
source venv/bin/activate  # Windows 平台使用：venv\Scripts\activate

步驟 3：安裝相依套件

使用 pip 安裝所需的相依套件：

pip install -r requirements.txt

如果沒有 requirements.txt 檔案，請手動安裝以下套件：

pip install fastapi qdrant-client langchain pydantic uvicorn python-dotenv openai

步驟 4：設置環境變數

在根目錄下建立一個 .env 檔案，並添加 OpenAI 和 Qdrant 所需的 API 金鑰：

OPENAI_API_KEY=你的-openai-api-金鑰
QDRANT_URL=你的-qdrant-網址
QDRANT_API_KEY=你的-qdrant-api-金鑰

	•	OPENAI_API_KEY：用於訪問 OpenAI 服務的 API 金鑰。
	•	QDRANT_URL：你的 Qdrant 實例的網址。
	•	QDRANT_API_KEY：Qdrant 的 API 金鑰（如果需要）。

步驟 5：運行 FastAPI 應用程式

透過以下命令在本地啟動 FastAPI 伺服器：

uvicorn app:app --reload

這將在 http://127.0.0.1:8000/ 啟動伺服器。

步驟 6：在 Swagger UI 上測試 API

FastAPI 會自動生成 API 文件，可透過瀏覽器訪問 http://127.0.0.1:8000/docs。

在這裡，您可以直接測試以下兩個 API 端點：

	•	/upload-pdf/：上傳要處理並儲存在 Qdrant 的 PDF 檔案。
	•	/ask-question/：根據上傳的 PDF 內容提出問題。

📄 API 端點

	1.	上傳 PDF - /upload-pdf/ [POST]
上傳 PDF 檔案，進行處理，創建嵌入，並儲存在 Qdrant 中。
請求：
	•	方法：POST
	•	內容類型：multipart/form-data
	•	主體：要上傳的 PDF 檔案。
回應：
	•	成功：{ "message": "PDF 已成功處理並儲存在向量資料庫中" }
	•	錯誤：{ "detail": "處理 PDF 失敗：<錯誤訊息>" }
	2.	提出問題 - /ask-question/ [POST]
接受一個問題，並根據從上傳的 PDF 儲存在向量資料庫中的內容返回答案。
請求：
	•	方法：POST
	•	內容類型：application/json
	•	主體：

{
  "question": "這份文件的摘要是什麼？"
}


回應：
	•	成功：{ "answer": "<來自文件的回應>" }
	•	錯誤：{ "detail": "檢索答案失敗：<錯誤訊息>" }

	3.	健康檢查 - / [GET]
一個簡單的健康檢查端點，用於驗證 API 是否正常運行。
回應：
	•	成功：{ "status": "Success" }

🧑‍💻 實用工具概述

utils.py 檔案包含處理 PDF、將嵌入發送至 Qdrant，以及從儲存的文件中檢索答案的實用函式。

utils.py 中的主要函式：

	•	process_pdf(pdf_path)
	•	從 PDF 中提取文字並將其拆分為較小的片段。
	•	輸入：PDF 檔案的路徑。
	•	回傳：PDF 的文字片段列表。
	•	send_to_qdrant(documents, embedding_model)
	•	在創建嵌入後，將處理過的文件片段發送至 Qdrant 進行儲存。
	•	輸入：文件片段列表和嵌入模型。
	•	回傳：成功時為 True，失敗時為 False。
	•	qdrant_client()
	•	初始化並回傳一個 Qdrant 客戶端，用於與向量資料庫交互。
	•	回傳：配置好的 Qdrant 向量存儲。
	•	qa_ret(qdrant_store, input_query)
	•	處理問答，透過從 Qdrant 檢索相關內容，並使用 OpenAI 的 GPT 模型生成回應。
	•	輸入：Qdrant 向量存儲和使用者的問題。
	•	回傳：基於文件上下文生成的回應。

🧪 測試應用程式

測試 PDF 上傳

	1.	啟動 FastAPI 伺服器（uvicorn app:app --reload）。
	2.	使用 http://127.0.0.1:8000/docs 上的 Swagger 上傳 PDF。
	3.	PDF 處理完成後，使用 /ask-question/ 端點，根據上傳的內容提出問題。

⚙️ 部署考量

	•	確保在生產環境中正確設置了 API 金鑰的環境變數。
	•	使用可擴展的部署方法，如 Docker，或部署到雲服務如 AWS、Google Cloud 或 Heroku。
	•	根據需求，您可以將 Qdrant 部署為託管服務，或自行託管實例。
- 寫了一個 test_api_key.py 專門來測試我們的api key 是不是有效的。