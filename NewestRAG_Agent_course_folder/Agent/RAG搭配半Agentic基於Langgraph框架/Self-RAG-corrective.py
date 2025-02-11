import os
import re
import logging
from typing import Annotated, Literal, TypedDict, Dict, Optional
import requests
import json

from langchain import hub
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage, AIMessage, convert_to_messages
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, StateGraph, add_messages

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API 設置
JINA_API_KEY = "jina_2752307cab7a46e29d16c3fcbcdca7e2VPAObQDS2ER66cFvwpmGVIeIN8TG"
os.environ["ANTHROPIC_API_KEY"] = "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"  # 請替換為您的 API key

# 初始化 LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0,
    anthropic_api_key=os.environ["ANTHROPIC_API_KEY"]  # 明確指定 API key
)

# 狀態定義
class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    question: str
    documents: list[Document]
    candidate_answer: str
    retries: int
    web_fallback: bool

# 評分模型
class GradeHallucinations(BaseModel):
    binary_score: str = Field(description="答案是否有根據，'yes' 或 'no'")

class GradeAnswer(BaseModel):
    binary_score: str = Field(description="答案是否解決問題，'yes' 或 'no'")

# Jina 搜索功能
def jina_web_search(query: str) -> Optional[Dict]:
    """使用 Jina AI 進行網頁搜索"""
    try:
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {JINA_API_KEY}',
            'Content-Type': 'application/json',
            'X-Retain-Images': 'none',
            'X-Return-Format': 'markdown',
            'X-With-Images-Summary': 'true',
            'X-With-Links-Summary': 'true'
        }
        
        # 使用實際的搜索 URL
        search_url = f"https://api.search.jina.ai/v1/search?q={query}"
        response = requests.post(
            'https://r.jina.ai/',
            json={'url': search_url},
            headers=headers
        )
        
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Jina 搜索錯誤: {str(e)}")
        return None

# 節點定義
def document_search(state: GraphState):
    """初始文檔檢索"""
    logger.info("執行文檔檢索")
    question = convert_to_messages(state["messages"])[-1].content
    
    # 使用 Jina 搜索作為初始文檔來源
    search_result = jina_web_search(question)
    documents = []
    
    if search_result and 'data' in search_result:
        content = search_result['data'].get('content', '')
        documents.append(Document(
            page_content=content,
            metadata={"source": "jina_initial_search"}
        ))
    
    if not documents:
        # 如果搜索失敗，使用空文檔
        documents = [Document(
            page_content="No initial content found",
            metadata={"source": "default"}
        )]
    
    return {
        "documents": documents,
        "question": question,
        "web_fallback": True
    }

def generate(state: GraphState):
    """生成答案"""
    logger.info("生成答案")
    question = state["question"]
    documents = state["documents"]
    retries = state.get("retries", -1)

    # 使用 RAG prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一個幫助回答問題的AI助手。使用提供的上下文來回答問題。如果上下文中沒有相關信息，請直接說明。"),
        ("human", "上下文: {context}\n\n問題: {question}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    generation = chain.invoke({
        "context": "\n\n".join([doc.page_content for doc in documents]),
        "question": question
    })
    
    return {
        "retries": retries + 1,
        "candidate_answer": generation
    }

def transform_query(state: GraphState):
    """問題轉換"""
    logger.info("轉換問題")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一個問題重寫專家，將輸入問題轉換為更適合檢索的形式。"),
        ("human", "請重寫這個問題，使其更容易找到相關信息：{question}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    better_question = chain.invoke({"question": state["question"]})
    return {"question": better_question}

def jina_search(state: GraphState):
    """額外的 Jina 網頁搜索"""
    logger.info("執行額外的 Jina 搜索")
    question = state["question"]
    documents = state["documents"]
    
    search_result = jina_web_search(question)
    if search_result and 'data' in search_result:
        content = search_result['data'].get('content', '')
        documents.append(Document(
            page_content=content,
            metadata={"source": "jina_additional_search"}
        ))
    
    return {
        "documents": documents,
        "web_fallback": False
    }

def finalize_response(state: GraphState):
    """完成回應"""
    logger.info("完成回應")
    return {
        "messages": [AIMessage(content=state["candidate_answer"])]
    }

# 評估函數
def grade_generation(state: GraphState, config) -> Literal["generate", "transform_query", "jina_search", "finalize_response"]:
    """評估生成結果並決定下一步"""
    logger.info("評估生成結果")
    web_fallback = state["web_fallback"]
    retries = state.get("retries", -1)
    max_retries = config.get("configurable", {}).get("max_retries", 2)

    if not web_fallback:
        return "finalize_response"

    # 使用 LLM 評估答案品質
    prompt = ChatPromptTemplate.from_messages([
        ("system", "評估答案的品質和相關性。回答 'yes' 如果答案充分解決了問題，否則回答 'no'。"),
        ("human", "問題: {question}\n\n答案: {answer}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    evaluation = chain.invoke({
        "question": state["question"],
        "answer": state["candidate_answer"]
    })

    if evaluation.strip().lower() == "yes":
        return "finalize_response"
    elif retries >= max_retries:
        return "jina_search"
    else:
        return "transform_query"

def main():
    # 創建工作流程圖
    workflow = StateGraph(GraphState)
    
    # 添加節點
    workflow.add_node("document_search", document_search)
    workflow.add_node("generate", generate)
    workflow.add_node("transform_query", transform_query)
    workflow.add_node("jina_search", jina_search)
    workflow.add_node("finalize_response", finalize_response)
    
    # 設置流程
    workflow.set_entry_point("document_search")
    workflow.add_edge("document_search", "generate")
    workflow.add_edge("transform_query", "document_search")
    workflow.add_edge("jina_search", "generate")
    workflow.add_edge("finalize_response", END)
    
    # 添加條件邊
    workflow.add_conditional_edges(
        "generate",
        grade_generation
    )
    
    # 編譯圖
    graph = workflow.compile()
    
    # 測試查詢
    test_questions = [
        "什麼是 pandas DataFrame?",
        "如何在 Python 中處理日期時間?",
        "機器學習中的過擬合是什麼?"
    ]
    
    for question in test_questions:
        logger.info(f"\n處理問題: {question}")
        
        inputs = {
            "messages": [("human", question)]
        }
        
        config = {"configurable": {"max_retries": 2}}
        
        try:
            for output in graph.stream(inputs, config):
                if "messages" in output.get("finalize_response", {}):
                    answer = output["finalize_response"]["messages"][0].content
                    logger.info(f"回答: {answer}\n")
                elif output:
                    logger.info(f"中間輸出: {output}\n")
        except Exception as e:
            logger.error(f"處理問題時發生錯誤: {str(e)}")
            logger.exception("詳細錯誤信息：")

if __name__ == "__main__":
    main()