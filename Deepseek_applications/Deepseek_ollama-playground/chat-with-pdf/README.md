# Chat with PDF
A simple RAG (Retrieval-Augmented Generation) system using Deepseek, LangChain, and Streamlit to chat with PDFs and answer complex questions about your local documents.

You can watch the video on how it was built on my [YouTube](https://youtu.be/M6vZ6b75p9k).

# Pre-requisites
Install Ollama on your local machine from the [official website](https://ollama.com/). And then pull the Deepseek model:

```bash
ollama pull deepseek-r1:14b
```

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

# Run
Run the Streamlit app:

```bash
streamlit run pdf_rag.py
```