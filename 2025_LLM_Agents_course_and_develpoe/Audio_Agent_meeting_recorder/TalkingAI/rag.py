import os
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_groq import ChatGroq

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

url="https://www.langchain.com/"
loader = WebBaseLoader(url)

document = loader.load()

# print(document)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function=len,
    separators = ["\n\n", "\n", " ", ""]
)

docs = text_splitter.split_documents(document)
# print(len(docs))

embeddings_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorDB = FAISS.from_documents(docs, embeddings_model)
vectorDB.save_local("vector_db")

prompt = hub.pull("langchain-ai/retrieval-qa-chat")

llm = ChatGroq(
    temperature=0.8,
    model="llama3-70b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

query = "What is langchain?"

combine_docs_chain = create_stuff_documents_chain(llm, prompt)

combine_docs_chain.invoke({
    "input": query,
    "context": docs
})

retriever = FAISS.load_local(
    "vector_db",
    embeddings_model,
    allow_dangerous_deserialization = True
    ).as_retriever()

retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

response = retrieval_chain.invoke({
    "input": query
})

print(response["answer"])