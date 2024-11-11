from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os
import logging

# Import the necessary functions from utils.py
from utils import process_pdf, send_to_qdrant, qdrant_client, qa_ret, OpenAIEmbeddings

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF file"""
    try:
        logger.info(f"Processing PDF file: {file.filename}")

        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Process PDF
            document_chunks = process_pdf(temp_file_path)
            logger.info(f"PDF processed into {len(document_chunks)} chunks")

            # Create embedding model
            embedding_model = OpenAIEmbeddings(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                model="text-embedding-ada-002"
            )
            logger.info("Embedding model created")

            # Send to Qdrant
            success = send_to_qdrant(document_chunks, embedding_model)
            if not success:
                raise Exception("Failed to store vectors in Qdrant")

            return {"message": "PDF successfully processed and stored"}

        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logger.info("Temporary file cleaned up")

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask-question/")
async def ask_question(question_request: QuestionRequest):
    """Handle question answering"""
    try:
        vector_store = qdrant_client()
        response = qa_ret(vector_store, question_request.question)
        return {"answer": response}
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}