# Announcing LangChain v0.3  
**Sep 16, 2024**

We are excited to announce the release of [LangChain v0.3](https://blog.langchain.dev/announcing-langchain-v0-3/) for both Python and JavaScript ecosystems.

## What's Changed

### Python
- All packages have been upgraded to Pydantic 2, allowing user code without the need for bridging packages.
- Pydantic 1 is no longer supported as it reached its end-of-life in June 2024.
- Python 3.8 will no longer be supported as it reaches its end-of-life in October 2024.

### JavaScript
- All LangChain packages now have `@langchain/core` as a peer dependency instead of a direct dependency.
- You now need to explicitly install `@langchain/core`.
- Callbacks are now backgrounded and non-blocking by default, requiring you to await the callbacks to ensure they finish.
- Deprecated document loaders and self-query entry points have been removed in favor of entry points in `@langchain/community` and integration packages.
- Deprecated Google PaLM entry points have been removed in favor of entry points in `@langchain/google-vertexai` and `@langchain/google-genai`.
- Using objects with a "type" as a BaseMessageLike is no longer recommended.

## What's New
- More integrations have been moved from `langchain-community` to independent `langchain-{name}` packages.
- Improved integration documentation and API reference.
- Simplified tool definitions and usage.
- Added utilities for interacting with chat models (Python, JS).
- Added the ability to dispatch custom events (Python, JS).
- Python API reference and JS API Reference.

## How to Update Your Code
Official guides have been written for Python and JS to help you migrate to the latest version.

## Documentation
LangChain documentation is versioned, and documentation for previous versions will remain live at the following URLs:
- [Python 0.1](https://python.langchain.com/v0.1/docs/get_started/introduction/?ref=blog.langchain.dev)
- [Python 0.2](https://python.langchain.com/v0.2/docs/introduction/)
- [JS 0.1](https://js.langchain.com/v0.1/docs/get_started/introduction/?ref=blog.langchain.dev)
- [JS 0.2](https://js.langchain.com/v0.2/docs/introduction/?ref=blog.langchain.dev)

## LangGraph
LangGraph is a library for building stateful multi-actor applications. Since LangChain v0.2, LangGraph has been recommended for building agents. LangGraph comes with a pre-built LangGraph object equivalent to the LangChain AgentExecutor, making it easy to use an out-of-the-box agent solution.

## What’s Coming
We expect to improve LangChain’s multi-modal capabilities during the 0.3 release and continue enhancing documentation and integration reliability.

We would love to hear your feedback on LangChain v0.3 on GitHub. If you're new to LangChain, follow our [quickstart guide](https://python.langchain.com/docs/tutorials/llm_chain/?ref=blog.langchain.dev) (Python, JS) to get started.
