# import streamlit as st

# from langchain_community.document_loaders import PDFPlumberLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_ollama import OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama.llms import OllamaLLM

# template = """
# You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
# Question: {question} 
# Context: {context} 
# Answer:
# """

# pdfs_directory = 'chat-with-pdf/pdfs/'

# embeddings = OllamaEmbeddings(model="deepseek-r1:14b")
# vector_store = InMemoryVectorStore(embeddings)

# model = OllamaLLM(model="deepseek-r1:8b")

# def upload_pdf(file):
#     with open(pdfs_directory + file.name, "wb") as f:
#         f.write(file.getbuffer())

# def load_pdf(file_path):
#     loader = PDFPlumberLoader(file_path)
#     documents = loader.load()

#     return documents

# def split_text(documents):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         add_start_index=True
#     )

#     return text_splitter.split_documents(documents)

# def index_docs(documents):
#     vector_store.add_documents(documents)

# def retrieve_docs(query):
#     return vector_store.similarity_search(query)

# def answer_question(question, documents):
#     context = "\n\n".join([doc.page_content for doc in documents])
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model

#     return chain.invoke({"question": question, "context": context})

# uploaded_file = st.file_uploader(
#     "Upload PDF",
#     type="pdf",
#     accept_multiple_files=False
# )

# if uploaded_file:
#     upload_pdf(uploaded_file)
#     documents = load_pdf(pdfs_directory + uploaded_file.name)
#     chunked_documents = split_text(documents)
#     index_docs(chunked_documents)

#     question = st.chat_input()

#     if question:
#         st.chat_message("user").write(question)
#         related_documents = retrieve_docs(question)
#         answer = answer_question(question, related_documents)
#         st.chat_message("assistant").write(answer)


import os
import streamlit as st
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.documents import Document

# Configuration
class Config:
    PDF_DIR = "pdfs"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "deepseek-r1:8b"
    LLM_MODEL = "deepseek-r1:8b"
    
    @classmethod
    def init_directories(cls):
        """Initialize necessary directories"""
        Path(cls.PDF_DIR).mkdir(parents=True, exist_ok=True)

# Initialize streamlit state
def init_state():
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = InMemoryVectorStore(
            OllamaEmbeddings(model=Config.EMBEDDING_MODEL)
        )
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()

# PDF Processing
class PDFProcessor:
    @staticmethod
    def save_pdf(uploaded_file) -> Optional[str]:
        """Save uploaded PDF file"""
        try:
            file_path = os.path.join(Config.PDF_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            st.error(f"Error saving PDF: {str(e)}")
            return None

    @staticmethod
    def load_pdf(file_path: str) -> List[Document]:
        """Load PDF file"""
        try:
            loader = PDFPlumberLoader(file_path)
            return loader.load()
        except Exception as e:
            st.error(f"Error loading PDF: {str(e)}")
            return []

    @staticmethod
    def split_documents(documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=Config.CHUNK_SIZE,
                chunk_overlap=Config.CHUNK_OVERLAP,
                add_start_index=True
            )
            return splitter.split_documents(documents)
        except Exception as e:
            st.error(f"Error splitting documents: {str(e)}")
            return []

# Chat functionality
class ChatBot:
    def __init__(self):
        self.template = """
        You are a helpful assistant for answering questions based on PDF documents. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer or can't find relevant information in the context, just say so.
        Use three sentences maximum and keep the answer concise and precise.

        Question: {question} 
        Context: {context} 
        Answer:
        """
        self.model = OllamaLLM(model=Config.LLM_MODEL)
        self.prompt = ChatPromptTemplate.from_template(self.template)

    def retrieve_context(self, question: str, top_k: int = 4) -> List[Document]:
        """Retrieve relevant documents for the question"""
        try:
            return st.session_state.vector_store.similarity_search(question, k=top_k)
        except Exception as e:
            st.error(f"Error retrieving context: {str(e)}")
            return []

    def answer_question(self, question: str, documents: List[Document]) -> str:
        """Generate answer based on question and context"""
        try:
            context = "\n\n".join([doc.page_content for doc in documents])
            chain = self.prompt | self.model
            return chain.invoke({"question": question, "context": context})
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
            return "I apologize, but I encountered an error while trying to generate an answer."

def main():
    st.title("PDF Chat Assistant")
    
    # Initialize
    Config.init_directories()
    init_state()
    chatbot = ChatBot()

    # File upload
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf",
        accept_multiple_files=False
    )

    if uploaded_file:
        # Process only if file hasn't been processed before
        if uploaded_file.name not in st.session_state.processed_files:
            with st.spinner("Processing PDF..."):
                file_path = PDFProcessor.save_pdf(uploaded_file)
                if file_path:
                    documents = PDFProcessor.load_pdf(file_path)
                    if documents:
                        chunks = PDFProcessor.split_documents(documents)
                        if chunks:
                            st.session_state.vector_store.add_documents(chunks)
                            st.session_state.processed_files.add(uploaded_file.name)
                            st.success(f"Successfully processed {uploaded_file.name}")

    # Chat interface
    question = st.chat_input("Ask a question about your PDF(s)")
    
    if question:
        st.chat_message("user").write(question)
        with st.spinner("Thinking..."):
            related_docs = chatbot.retrieve_context(question)
            if related_docs:
                answer = chatbot.answer_question(question, related_docs)
                st.chat_message("assistant").write(answer)
            else:
                st.chat_message("assistant").write("I couldn't find relevant information in the uploaded documents.")

if __name__ == "__main__":
    main()