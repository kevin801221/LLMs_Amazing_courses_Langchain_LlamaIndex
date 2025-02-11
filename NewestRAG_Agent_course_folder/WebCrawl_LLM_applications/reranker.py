# import os
# from dotenv.main import load_dotenv

# from llama_index.llms.ollama import Ollama
# # from llama_index.embeddings.jinaai import JinaEmbedding
# from llama_index.postprocessor.jinaai_rerank import JinaRerank
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# import requests
# from termcolor import colored
# from llama_index.core import (
#     SimpleDirectoryReader,
#     VectorStoreIndex,
# )

# load_dotenv()

# jinaai_api_key = os.getenv("JINA_API_KEY")

# llm = Ollama(
#     model="llama3.2:latest",
# )

# # jina_embeddings = JinaEmbedding(
# #     api_key=jinaai_api_key,
# #     model="jina-embeddings-v3",
# #     embed_batch_size=16,
# #     task="retrieval.passage",
# # )
# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# jina_rerank = JinaRerank(
#     model="jina-reranker-v1-base-en",
#     api_key=jinaai_api_key,
#     top_n=3,
# )

# url = "https://niketeam-asset-download.nike.net/catalogs/2024/2024_Nike%20Kids_02_09_24.pdf?cb=09302022"
# full_url = f"https://r.jina.ai/{url}"
# headers = {
#     'Content-Type': "application/json",
#     'X-Return-Format': "markdown",
# }

# response = requests.get(full_url, headers=headers)

# if response.status_code == 200:
#     with open("Nike_Catelog.md", "wb") as file:
#         file.write(response.content)
# else:
#     print(colored("Failed to download the file.", "red"))
    
# reader = SimpleDirectoryReader(input_files=["Nike_Catelog.md"])

# documents = reader.load_data()
# index = VectorStoreIndex.from_documents(
#     documents=documents,
#     embed_model=embed_model,
# )
# query_engine = index.as_query_engine(
#     llm=llm,
#     similarity_top_k = 25,
# )
# answer = query_engine.query("What are the best padded pants that Nike sells?")

# print(colored(answer.source_nodes[0].text, "cyan"))
# print(colored(answer.source_nodes[0].score, "cyan"))
# print("\n\n================================================\n\n")
# print(colored(answer.source_nodes[1].text, "cyan"))
# print(colored(answer.source_nodes[1].score, "cyan"))

# rerank_query_engine = index.as_query_engine(
#     llm=llm,
#     node_postprocessors=[jina_rerank],
# )
# rerank_answer = rerank_query_engine.query("What are the best padded pants that Nike sells?")

# print(colored(rerank_answer.source_nodes[0].text, "green"))
# print(colored(rerank_answer.source_nodes[0].score, "green"))
# print("\n\n================================================\n\n")
# print(colored(rerank_answer.source_nodes[1].text, "green"))
# print(colored(rerank_answer.source_nodes[1].score, "green"))

import os
from dotenv.main import load_dotenv
from llama_index.llms.ollama import Ollama
from llama_index.postprocessor.jinaai_rerank import JinaRerank
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import requests
from termcolor import colored
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from datetime import datetime
import json

def save_results(results, filename):
    """保存查詢結果到文件"""
    output = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'results': []
    }
    
    for idx, node in enumerate(results.source_nodes):
        output['results'].append({
            'rank': idx + 1,
            'text': node.text,
            'score': float(node.score)  # 轉換為float以便JSON序列化
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

def process_pdf(pdf_path, query_text):
    """處理PDF文件並執行查詢"""
    load_dotenv()
    jinaai_api_key = os.getenv("JINA_API_KEY")
    
    # 初始化模型
    llm = Ollama(
        model="llama3.2:latest",
    )
    
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    
    jina_rerank = JinaRerank(
        model="jina-reranker-v1-base-en",
        api_key=jinaai_api_key,
        top_n=3,
    )
    
    # 如果是URL，下載PDF
    if pdf_path.startswith('http'):
        print(colored("正在下載PDF...", "yellow"))
        full_url = f"https://r.jina.ai/{pdf_path}"
        headers = {
            'Content-Type': "application/json",
            'X-Return-Format': "markdown",
        }
        response = requests.get(full_url, headers=headers)
        
        if response.status_code == 200:
            output_md = "downloaded_catalog.md"
            with open(output_md, "wb") as file:
                file.write(response.content)
            pdf_path = output_md
        else:
            raise Exception("下載PDF失敗")
    
    # 讀取並處理文件
    print(colored("正在處理文件...", "yellow"))
    reader = SimpleDirectoryReader(input_files=[pdf_path])
    documents = reader.load_data()
    
    # 建立索引
    print(colored("建立索引...", "yellow"))
    index = VectorStoreIndex.from_documents(
        documents=documents,
        embed_model=embed_model,
    )
    
    # 執行基本查詢
    print(colored("執行基本查詢...", "yellow"))
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=25,
    )
    answer = query_engine.query(query_text)
    
    # 保存基本查詢結果
    save_results(answer, "basic_query_results.json")
    
    # 執行重排序查詢
    print(colored("執行重排序查詢...", "yellow"))
    rerank_query_engine = index.as_query_engine(
        llm=llm,
        node_postprocessors=[jina_rerank],
    )
    rerank_answer = rerank_query_engine.query(query_text)
    
    # 保存重排序查詢結果
    save_results(rerank_answer, "reranked_query_results.json")
    
    # 打印結果
    print("\n基本查詢結果:")
    for idx, node in enumerate(answer.source_nodes[:2]):
        print(colored(f"\n結果 {idx+1}:", "cyan"))
        print(colored(node.text, "cyan"))
        print(colored(f"分數: {node.score}", "cyan"))
    
    print("\n重排序查詢結果:")
    for idx, node in enumerate(rerank_answer.source_nodes[:2]):
        print(colored(f"\n結果 {idx+1}:", "green"))
        print(colored(node.text, "green"))
        print(colored(f"分數: {node.score}", "green"))

# 使用示例
if __name__ == "__main__":
    # 使用 Nike 的 PDF URL
    pdf_source = "https://niketeam-asset-download.nike.net/catalogs/2024/2024_Nike%20Kids_02_09_24.pdf?cb=09302022"
    # 或者使用本地 PDF，例如：
    # pdf_source = "C:/Users/YourName/Documents/your_pdf.pdf"
    query = "What are the best padded pants that Nike sells?"
    
    try:
        process_pdf(pdf_source, query)
        print(colored("\n處理完成！結果已保存到 basic_query_results.json 和 reranked_query_results.json", "yellow"))
    except Exception as e:
        print(colored(f"發生錯誤: {str(e)}", "red"))