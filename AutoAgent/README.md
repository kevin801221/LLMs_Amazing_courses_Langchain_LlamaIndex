# AutoAgent

AutoAgent 是一個強大的自主代理框架，旨在簡化 AI 代理的創建、配置和部署過程。它提供了一套全面的工具和接口，使開發者能夠輕鬆構建複雜的 AI 代理系統。

## 主要特點

- **多代理協作**：支持多個代理之間的協作，以解決複雜任務
- **工具整合**：輕鬆整合各種外部工具和 API
- **可定制工作流**：根據特定需求創建和調整代理工作流
- **元代理架構**：使用元代理來協調和管理其他代理
- **高度可擴展**：從簡單應用擴展到複雜系統

## 快速開始

### 安裝

```bash
pip install autoagent
```

### 基本用法

```python
from autoagent import Agent, Workflow

# 創建一個簡單的代理
agent = Agent("my_agent")

# 配置代理
agent.configure(
    model="gpt-4",
    temperature=0.7,
    tools=["web_search", "calculator"]
)

# 創建工作流
workflow = Workflow("simple_workflow")
workflow.add_agent(agent)

# 運行工作流
result = workflow.run("分析最近的 AI 發展趨勢")
print(result)
```

## 文檔

完整文檔可在 [docs/](./docs/) 目錄中找到。

## 貢獻

歡迎貢獻！請查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解如何開始。

## 許可證

本項目採用 MIT 許可證 - 詳見 [LICENSE](./LICENSE) 文件。
