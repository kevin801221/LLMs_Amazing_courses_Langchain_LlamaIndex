import os
from dotenv.main import load_dotenv

from llama_index.llms.ollama import Ollama
# from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.postprocessor.jinaai_rerank import JinaRerank
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import requests
from termcolor import colored
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
)

load_dotenv()

jinaai_api_key = os.getenv("JINA_API_KEY")

llm = Ollama(
    model="llama3.2:latest",
)

# jina_embeddings = JinaEmbedding(
#     api_key=jinaai_api_key,
#     model="jina-embeddings-v3",
#     embed_batch_size=16,
#     task="retrieval.passage",
# )
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

jina_rerank = JinaRerank(
    model="jina-reranker-v1-base-en",
    api_key=jinaai_api_key,
    top_n=3,
)

url = "https://niketeam-asset-download.nike.net/catalogs/2024/2024_Nike%20Kids_02_09_24.pdf?cb=09302022"
full_url = f"https://r.jina.ai/{url}"
headers = {
    'Content-Type': "application/json",
    'X-Return-Format': "markdown",
}

response = requests.get(full_url, headers=headers)

if response.status_code == 200:
    with open("Nike_Catelog.md", "wb") as file:
        file.write(response.content)
else:
    print(colored("Failed to download the file.", "red"))
    
reader = SimpleDirectoryReader(input_files=["Nike_Catelog.md"])

documents = reader.load_data()
index = VectorStoreIndex.from_documents(
    documents=documents,
    embed_model=embed_model,
)
query_engine = index.as_query_engine(
    llm=llm,
    similarity_top_k = 25,
)
answer = query_engine.query("What are the best padded pants that Nike sells?")

print(colored(answer.source_nodes[0].text, "cyan"))
print(colored(answer.source_nodes[0].score, "cyan"))
print("\n\n================================================\n\n")
print(colored(answer.source_nodes[1].text, "cyan"))
print(colored(answer.source_nodes[1].score, "cyan"))

rerank_query_engine = index.as_query_engine(
    llm=llm,
    node_postprocessors=[jina_rerank],
)
rerank_answer = rerank_query_engine.query("What are the best padded pants that Nike sells?")

print(colored(rerank_answer.source_nodes[0].text, "green"))
print(colored(rerank_answer.source_nodes[0].score, "green"))
print("\n\n================================================\n\n")
print(colored(rerank_answer.source_nodes[1].text, "green"))
print(colored(rerank_answer.source_nodes[1].score, "green"))