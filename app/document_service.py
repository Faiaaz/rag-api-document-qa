"""
Unified document service combining processing and vector storage
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import time

from app.document_processor import DocumentProcessorFactory
from app.vector_store import EmbeddingManager, FAISSVectorStore
from app.models import DocumentChunk, UploadResponse, ProcessingStatus


class DocumentService:
    """Unified service for document processing and vector storage"""
    
    def __init__(self, 
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 embedding_model: str = "all-MiniLM-L6-v2",
                 vector_store_path: str = "./data/vector_store"):
        """
        Initialize the document service
        
        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
            embedding_model: Name of the sentence transformer model
            vector_store_path: Path to store vector database
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.vector_store_path = vector_store_path
        
        # Initialize components
        self.processor_factory = DocumentProcessorFactory(chunk_size, chunk_overlap)
        self.embedding_manager = EmbeddingManager(embedding_model)
        self.vector_store = FAISSVectorStore(
            embedding_manager=self.embedding_manager,
            index_path=vector_store_path,
            index_name="document_index"
        )
        
        print(f"Document service initialized with {len(self.processor_factory.get_supported_extensions())} supported file types")
    
    def process_and_store_document(self, file_path: str) -> UploadResponse:
        """
        Process a document and store it in the vector database
        
        Args:
            file_path: Path to the document file
            
        Returns:
            UploadResponse with processing results
        """
        start_time = time.time()
        
        try:
            # Validate file
            if not self.processor_factory.can_process(file_path):
                raise ValueError(f"Unsupported file type: {Path(file_path).suffix}")
            
            # Process document
            chunks = self.processor_factory.process_document(file_path)
            
            if not chunks:
                raise ValueError("No content extracted from document")
            
            # Add to vector store
            chunk_ids = self.vector_store.add_documents(chunks)
            
            # Save vector store
            self.vector_store.save()
            
            processing_time = time.time() - start_time
            
            # Create response
            response = UploadResponse(
                file_id=str(chunk_ids[0]) if chunk_ids else "unknown",
                filename=Path(file_path).name,
                file_type=Path(file_path).suffix.lower(),
                status="success",
                message=f"Document processed and stored successfully in {processing_time:.2f}s",
                chunks_processed=len(chunks)
            )
            
            print(f"✅ Processed {response.filename}: {len(chunks)} chunks in {processing_time:.2f}s")
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Failed to process document: {str(e)}"
            print(f"❌ Error processing {Path(file_path).name}: {error_msg}")
            
            return UploadResponse(
                file_id="error",
                filename=Path(file_path).name,
                file_type=Path(file_path).suffix.lower(),
                status="error",
                message=error_msg,
                chunks_processed=0
            )
    
    def search_documents(self, 
                        query: str, 
                        top_k: int = 5, 
                        threshold: float = 0.1) -> List[Dict[str, Any]]:
        """
        Search for documents based on query
        
        Args:
            query: Search query
            top_k: Number of top results
            threshold: Minimum similarity threshold
            
        Returns:
            List of search results
        """
        try:
            results = self.vector_store.search(query, top_k, threshold)
            print(f"🔍 Search for '{query}': found {len(results)} results")
            return results
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Get statistics about stored documents"""
        stats = self.vector_store.get_stats()
        stats.update({
            "supported_extensions": self.processor_factory.get_supported_extensions(),
            "embedding_model": self.embedding_manager.get_model_info(),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        })
        return stats
    
    def delete_document(self, filename: str) -> Dict[str, Any]:
        """
        Delete a document from the vector store
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            Deletion result
        """
        try:
            deleted_count = self.vector_store.delete_by_filename(filename)
            if deleted_count > 0:
                self.vector_store.save()
                return {
                    "success": True,
                    "message": f"Deleted {deleted_count} chunks for {filename}",
                    "deleted_chunks": deleted_count
                }
            else:
                return {
                    "success": False,
                    "message": f"File {filename} not found in vector store",
                    "deleted_chunks": 0
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting document: {str(e)}",
                "deleted_chunks": 0
            }
    
    def get_chunk_by_id(self, chunk_id: int) -> Optional[DocumentChunk]:
        """Get a specific document chunk by ID"""
        return self.vector_store.get_chunk_by_id(chunk_id)
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate if a file can be processed"""
        return self.processor_factory.validate_file(file_path)
    
    def get_processing_status(self) -> ProcessingStatus:
        """Get current processing status"""
        stats = self.get_document_stats()
        
        return ProcessingStatus(
            status="ready",
            progress=100.0,
            message=f"Service ready. {stats['total_chunks']} chunks stored."
        )
    
    def clear_all_documents(self) -> Dict[str, Any]:
        """Clear all documents from the vector store"""
        try:
            self.vector_store.clear()
            self.vector_store.save()
            return {
                "success": True,
                "message": "All documents cleared from vector store"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error clearing documents: {str(e)}"
            } 