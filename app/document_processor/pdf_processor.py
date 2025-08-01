"""
PDF document processor using PyMuPDF
"""
import fitz  # PyMuPDF (pymupdf)
from typing import List, Dict, Any
from pathlib import Path

from .base_processor import BaseDocumentProcessor


class PDFProcessor(BaseDocumentProcessor):
    """Processor for PDF documents"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(chunk_size, chunk_overlap)
        self.supported_extensions = {'.pdf'}
    
    def can_process(self, file_path: str) -> bool:
        """Check if this processor can handle the given file"""
        if not self.validate_file(file_path):
            return False
        
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_extensions
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            # Open the PDF file
            doc = fitz.open(file_path)
            text_content = []
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Get text from the page
                page_text = page.get_text()
                
                # Add page number to the text for context
                page_content = f"Page {page_num + 1}:\n{page_text}\n"
                text_content.append(page_content)
            
            # Close the document
            doc.close()
            
            # Join all text content
            full_text = "\n".join(text_content)
            
            return full_text
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF {file_path}: {str(e)}")
    
    def extract_text_with_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text with additional metadata from PDF
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing text and metadata
        """
        try:
            doc = fitz.open(file_path)
            
            # Get document metadata
            metadata = doc.metadata
            page_count = len(doc)
            
            # Extract text
            text_content = []
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                page_content = f"Page {page_num + 1}:\n{page_text}\n"
                text_content.append(page_content)
            
            doc.close()
            
            return {
                "text": "\n".join(text_content),
                "page_count": page_count,
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", "")
            }
            
        except Exception as e:
            raise ValueError(f"Failed to extract text and metadata from PDF {file_path}: {str(e)}") 