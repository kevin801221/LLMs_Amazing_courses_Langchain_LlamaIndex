import os
from termcolor import colored
from dotenv.main import load_dotenv

from llama_index.core.llama_dataset import download_llama_dataset

from llama_index.llms.openai import OpenAI
from llama_index.core import (
    Settings,
    VectorStoreIndex,
)

from llama_index.embeddings.jinaai import JinaEmbedding

load_dotenv()

rag_dataset, documents = download_llama_dataset(
    "PaulGrahamEssayDataset",
    "./data",
)

openai_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")
jinaai_api_key = os.getenv("JINA_API_KEY")

llm = OpenAI(
    api_key=openai_key,
    api_base=openai_base_url
)
Settings.llm = llm

embed_model = JinaEmbedding(
    model="jina-embeddings-v3",
    api_key=jinaai_api_key,
    task="retrieval.passage",
    embed_batch_size=16,
)

index = VectorStoreIndex.from_documents(
    documents=documents,
    embed_model=embed_model,
)
query_engine = index.as_query_engine()

response = query_engine.query("論文發表之後發生了什麼事情？ 用中文回答我")
print(colored(response, "magenta"))

# print(colored(os.getenv("OPENAI_BASE_URL"), "cyan"))