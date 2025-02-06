# AI Scraper
A simple AI web scraper using Ollama, LangChain, and Streamlit by building a RAG(Retrieval-Augmented Generation) system to chat with websites and answer complex questions about the content.

You can watch the video on how it was built on my [YouTube](https://youtu.be/eLV1R6ORRyU).

# Pre-requisites
Install Ollama on your local machine from the [official website](https://ollama.com/). And then pull the llama model:

```bash
ollama pull llama3.2
```

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

# Run
Run the Streamlit app:

```bash
streamlit run ai_scraper.py
```