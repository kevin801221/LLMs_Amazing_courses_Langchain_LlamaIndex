from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient, models
from qdrant_client.http import models
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  # 添加這個導入
import os
import logging
from typing import List
import time

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()

# 設置常數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "xeven_chatbot"


def batch_documents(documents: List, batch_size: int = 20):
    """將文檔分批處理"""
    for i in range(0, len(documents), batch_size):
        yield documents[i:i + batch_size]


def send_to_qdrant(documents, embedding_model):
    """分批發送文檔到 Qdrant"""
    try:
        # 創建新的集合
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=300)  # 增加超時時間

        # 檢查並刪除舊的集合
        try:
            client.delete_collection(COLLECTION_NAME)
            logger.info(f"Deleted existing collection: {COLLECTION_NAME}")
        except Exception:
            pass

        # 創建新集合
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Created new collection: {COLLECTION_NAME}")

        # 分批處理文檔
        total_batches = (len(documents) + 19) // 20  # 計算總批次數
        for batch_num, doc_batch in enumerate(batch_documents(documents), 1):
            try:
                logger.info(f"Processing batch {batch_num}/{total_batches}")

                # 為每個批次創建一個新的向量存儲
                vector_store = Qdrant.from_documents(
                    doc_batch,
                    embedding_model,
                    url=QDRANT_URL,
                    api_key=QDRANT_API_KEY,
                    collection_name=COLLECTION_NAME,
                    force_recreate=False,  # 不要重新創建集合
                    batch_size=20,  # 設置批次大小
                    prefer_grpc=True,  # 使用 gRPC 可能會更快
                )

                logger.info(f"Successfully stored batch {batch_num}")

                # 在批次之間添加小的延遲
                if batch_num < total_batches:
                    time.sleep(1)

            except Exception as e:
                logger.error(f"Error processing batch {batch_num}: {str(e)}")
                raise

        logger.info("Successfully stored all documents in Qdrant")
        return True

    except Exception as e:
        logger.error(f"Failed to store data in vector DB: {str(e)}")
        raise


def process_pdf(pdf_path):
    """處理 PDF 文件"""
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        document_text = "".join([page.page_content for page in pages])

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=40
        )
        chunks = text_splitter.create_documents([document_text])
        logger.info(f"Successfully processed PDF into {len(chunks)} chunks")
        return chunks
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise


def qdrant_client():
    """初始化 Qdrant client"""
    try:
        embedding_model = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model="text-embedding-ada-002"
        )

        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=300)
        vector_store = Qdrant(
            client=client,
            collection_name=COLLECTION_NAME,
            embeddings=embedding_model
        )

        return vector_store
    except Exception as e:
        logger.error(f"Error initializing Qdrant client: {str(e)}")
        raise


def qa_ret(qdrant_store, input_query):
    """處理問答檢索"""
    try:
        template = """
        Instructions:
            You are trained to extract answers from the given Context and the User's Question. Your response must be based on semantic understanding, which means even if the wording is not an exact match, infer the closest possible meaning from the Context. 

            Key Points to Follow:
            - **Precise Answer Length**: The answer must be between a minimum of 40 words and a maximum of 100 words.
            - **Strict Answering Rules**: Do not include any unnecessary text. The answer should be concise and focused directly on the question.
            - **Professional Language**: Do not use any abusive or prohibited language. Always respond in a polite and gentle tone.
            - **No Personal Information Requests**: Do not ask for personal information from the user at any point.
            - **Concise & Understandable**: Provide the most concise, clear, and understandable answer possible.
            - **Semantic Similarity**: If exact wording isn't available in the Context, use your semantic understanding to infer the answer. If there are semantically related phrases, use them to generate a precise response. Use natural language understanding to interpret closely related words or concepts.
            - **Unavailable Information**: If the answer is genuinely not found in the Context, politely apologize and inform the user that the specific information is not available in the provided context.

            Context:
            {context}

            **User's Question:** {question}

            Respond in a polite, professional, and concise manner.
        """
        prompt = ChatPromptTemplate.from_template(template)
        retriever = qdrant_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        setup_and_retrieval = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        )

        model = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
            max_tokens=150
        )

        output_parser = StrOutputParser()
        rag_chain = setup_and_retrieval | prompt | model | output_parser
        response = rag_chain.invoke(input_query)
        return response

    except Exception as e:
        logger.error(f"Error in QA retrieval: {str(e)}")
        raise