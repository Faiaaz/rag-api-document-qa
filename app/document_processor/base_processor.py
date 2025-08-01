"""
Base document processor class
Defines the interface for all document processors
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path
import os

from app.models import DocumentChunk
from app.utils.helpers import chunk_text, clean_text, extract_metadata_from_filename


class BaseDocumentProcessor(ABC):
    """Abstract base class for document processors"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor
        
        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.supported_extensions = set()
    
    @abstractmethod
    def can_process(self, file_path: str) -> bool:
        """
        Check if this processor can handle the given file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the processor can handle this file type
        """
        pass
    
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """
        Extract text content from the file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text content
        """
        pass
    
    def process_document(self, file_path: str) -> List[DocumentChunk]:
        """
        Process a document and return chunks with metadata
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            List of document chunks with metadata
        """
        if not self.can_process(file_path):
            raise ValueError(f"Cannot process file: {file_path}")
        
        # Extract text from the file
        text = self.extract_text(file_path)
        
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Split into chunks
        text_chunks = chunk_text(cleaned_text, self.chunk_size, self.chunk_overlap)
        
        # Get file metadata
        file_metadata = extract_metadata_from_filename(file_path)
        file_metadata.update({
            "size": os.path.getsize(file_path),
            "processor": self.__class__.__name__,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        })
        
        # Create document chunks
        chunks = []
        for i, chunk_content in enumerate(text_chunks):
            chunk_metadata = file_metadata.copy()
            chunk_metadata.update({
                "chunk_index": i,
                "total_chunks": len(text_chunks),
                "chunk_length": len(chunk_content)
            })
            
            chunk = DocumentChunk(
                content=chunk_content,
                metadata=chunk_metadata,
                embedding=None  # Will be added later by vector store
            )
            chunks.append(chunk)
        
        return chunks
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions"""
        return list(self.supported_extensions)
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate that the file exists and is readable
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is valid
        """
        path = Path(file_path)
        return path.exists() and path.is_file() and os.access(file_path, os.R_OK) 