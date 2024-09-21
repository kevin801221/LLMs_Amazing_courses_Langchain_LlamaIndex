# Announcing LangChain v0.3  
**Sep 16, 2024**

[LangChain v0.3](https://blog.langchain.dev/announcing-langchain-v0-3/) 的釋出，適用於 Python 和 Javascript 生態系統。

## What's Changed

### Python
- 所有套件已升級至 Pydantic 2，支持用戶代碼無需使用橋接包。
- Pydantic 1 不再支持，因為其已於 2024 年 6 月達到生命終止。
- Python 3.8 將不再支持，因為其於 2024 年 10 月達到生命終止。

### JavaScript
- 所有 LangChain 套件現在將 `@langchain/core` 作為 peer dependency，而非直接依賴。
- 現在需要顯式安裝 `@langchain/core`。
- 回調現在預設為背景非阻塞，需等待回調結束。
- 移除了過時的文檔加載器和自查詢入口點，並優先考慮在 `@langchain/community` 和集成包中的入口點。
- 移除過時的 Google PaLM 入口點，轉向 `@langchain/google-vertexai` 和 `@langchain/google-genai`。
- 不推薦使用具有 "type" 的物件作為 BaseMessageLike。

## What's New
- 將更多集成從 `langchain-community` 移至獨立的 `langchain-{name}` 套件。
- 改進的集成文檔和 API 參考。
- 簡化的工具定義和使用。
- 新增與聊天模型互動的工具（Python、JS）。
- 新增自定義事件分派能力（Python、JS）。
-  Python API reference and JS API Reference.
## How to Update Your Code
官方已為 Python 和 JS 寫了如何遷移到最新版本的指南。

## Documentation
LangChain 文檔已版本化，舊版本文檔仍可訪問：
- [Python 0.1](https://python.langchain.com/v0.1/docs/get_started/introduction/?ref=blog.langchain.dev)
- [Python 0.2](https://python.langchain.com/v0.2/docs/introduction/)
- [JS 0.1](https://js.langchain.com/v0.1/docs/get_started/introduction/?ref=blog.langchain.dev)
- [JS 0.2](https://js.langchain.com/v0.2/docs/introduction/?ref=blog.langchain.dev)

## LangGraph
LangGraph 是一個用於構建狀態多演員應用的庫，自 LangChain v0.2 開始推薦使用 LangGraph 建立代理。LangGraph 內建與 LangChain AgentExecutor 等效的 LangGraph 物件，便於使用即時解決方案。

## What’s Coming
預期在 0.3 版本中改進 LangChain 的多模態能力，並持續改進文檔和集成的可靠性。

我們期待在 GitHub 上聽取您對 LangChain v0.3 的所有反饋。如果您是 LangChain 的新手，請遵循我們的 [快速入門指南](https://python.langchain.com/docs/tutorials/llm_chain/?ref=blog.langchain.dev)（Python、JS）開始。
