"""
Main FastAPI application for RAG API
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from app.models import QueryRequest, QueryResponse, UploadResponse
from app.document_service import DocumentService
from app.llm import OpenAIClient, PromptManager, RAGPipeline

# Load environment variables
load_dotenv()

# Initialize services
document_service = DocumentService(
    chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
    chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 200)),
    embedding_model=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
    vector_store_path=os.getenv("VECTOR_STORE_PATH", "./data/vector_store")
)

# Initialize LLM components
try:
    openai_client = OpenAIClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    )
    llm_available = True
except ValueError as e:
    print(f"⚠️  OpenAI client not available: {e}")
    openai_client = None
    llm_available = False

prompt_manager = PromptManager()

# Initialize RAG pipeline only if LLM is available
if llm_available:
    rag_pipeline = RAGPipeline(
        document_service=document_service,
        openai_client=openai_client,
        prompt_manager=prompt_manager
    )
else:
    rag_pipeline = None

# Create FastAPI app
app = FastAPI(
    title="RAG API - Document Q&A System",
    description="A smart Retrieval-Augmented Generation API for document question answering",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": "RAG API - Document Q&A System",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "Document upload and processing",
            "Vector search with FAISS",
            "Question answering with OpenAI",
            "Support for multiple file types"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "RAG API is running successfully",
        "document_service": document_service.get_document_stats(),
        "llm_service": openai_client.get_model_info() if openai_client else {"status": "not_available"},
        "llm_available": llm_available
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file type
        if not document_service.validate_file(file.filename)["can_process"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file.filename}"
            )
        
        # Save file temporarily
        upload_dir = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process and store document
        response = document_service.process_and_store_document(str(file_path))
        
        # Clean up temporary file
        file_path.unlink()
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG pipeline"""
    try:
        if rag_pipeline is None:
            raise HTTPException(
                status_code=503, 
                detail="LLM service not available. Please set OPENAI_API_KEY environment variable."
            )
        
        response = rag_pipeline.answer_question_with_request(request)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "document_service": document_service.get_document_stats(),
        "llm_service": openai_client.get_model_info(),
        "rag_pipeline": rag_pipeline.get_pipeline_info()
    }

@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete a document from the vector store"""
    try:
        result = document_service.delete_document(filename)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    ) 