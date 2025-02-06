# Image Search
A local image search engine using Ollama, LangChain, and Streamlit. This image search engine can search images using text queries or perform reverse image searches by uploading an image to find similar results.

You can watch the video on how it was built on my [YouTube](https://youtu.be/S9ugRzGjFtA).

# Pre-requisites
Install Ollama on your local machine from the [official website](https://ollama.com/). And then pull the Llava model:

```bash
ollama pull llava:34b
```

And then also pull the llama model:

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
streamlit run app.py
```