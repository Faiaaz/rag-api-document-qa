"""
Pydantic models for API request and response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    """Request model for querying documents"""
    question: str = Field(..., description="The question to ask about the documents")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image for image-based questions")
    top_k: int = Field(default=5, description="Number of top similar documents to retrieve")

class QueryResponse(BaseModel):
    """Response model for query results"""
    answer: str = Field(..., description="The generated answer")
    sources: List[Dict[str, Any]] = Field(..., description="Source documents used for the answer")
    confidence: float = Field(..., description="Confidence score of the answer")
    processing_time: float = Field(..., description="Time taken to process the query")

class UploadResponse(BaseModel):
    """Response model for file upload"""
    file_id: str = Field(..., description="Unique identifier for the uploaded file")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="Type of the uploaded file")
    status: str = Field(..., description="Processing status")
    message: str = Field(..., description="Additional information")
    chunks_processed: int = Field(..., description="Number of text chunks processed")

class DocumentChunk(BaseModel):
    """Model for document chunks"""
    content: str = Field(..., description="Text content of the chunk")
    metadata: Dict[str, Any] = Field(..., description="Metadata about the chunk")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the chunk")

class ProcessingStatus(BaseModel):
    """Model for processing status"""
    status: str = Field(..., description="Current processing status")
    progress: float = Field(..., description="Progress percentage (0-100)")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now) 