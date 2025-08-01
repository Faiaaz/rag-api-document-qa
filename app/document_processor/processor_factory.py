"""
Document processor factory
Automatically selects the appropriate processor based on file type
"""
from typing import List, Dict, Any, Optional
from pathlib import Path

from .base_processor import BaseDocumentProcessor
from .pdf_processor import PDFProcessor
from .docx_processor import DOCXProcessor
from .text_processor import TextProcessor
from .image_processor import ImageProcessor
from .csv_processor import CSVProcessor


class DocumentProcessorFactory:
    """Factory for creating document processors"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the factory with processors
        
        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize all processors
        self.processors = {
            PDFProcessor(chunk_size, chunk_overlap),
            DOCXProcessor(chunk_size, chunk_overlap),
            TextProcessor(chunk_size, chunk_overlap),
            ImageProcessor(chunk_size, chunk_overlap),
            CSVProcessor(chunk_size, chunk_overlap)
        }
        
        # Create a mapping of extensions to processors
        self.extension_processor_map = {}
        for processor in self.processors:
            for extension in processor.get_supported_extensions():
                self.extension_processor_map[extension] = processor
    
    def get_processor(self, file_path: str) -> Optional[BaseDocumentProcessor]:
        """
        Get the appropriate processor for a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Appropriate processor or None if no processor found
        """
        extension = Path(file_path).suffix.lower()
        return self.extension_processor_map.get(extension)
    
    def can_process(self, file_path: str) -> bool:
        """
        Check if the factory can process a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if a processor is available for this file type
        """
        processor = self.get_processor(file_path)
        return processor is not None and processor.can_process(file_path)
    
    def process_document(self, file_path: str) -> List[Any]:
        """
        Process a document using the appropriate processor
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            List of document chunks
        """
        processor = self.get_processor(file_path)
        
        if processor is None:
            raise ValueError(f"No processor available for file type: {Path(file_path).suffix}")
        
        if not processor.can_process(file_path):
            raise ValueError(f"Processor cannot handle file: {file_path}")
        
        return processor.process_document(file_path)
    
    def get_supported_extensions(self) -> List[str]:
        """
        Get all supported file extensions
        
        Returns:
            List of supported file extensions
        """
        return list(self.extension_processor_map.keys())
    
    def get_processor_info(self) -> Dict[str, Any]:
        """
        Get information about all available processors
        
        Returns:
            Dictionary with processor information
        """
        info = {}
        for processor in self.processors:
            processor_name = processor.__class__.__name__
            info[processor_name] = {
                "supported_extensions": processor.get_supported_extensions(),
                "chunk_size": processor.chunk_size,
                "chunk_overlap": processor.chunk_overlap
            }
        return info
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a file and get processing information
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with validation results
        """
        path = Path(file_path)
        
        result = {
            "file_path": file_path,
            "filename": path.name,
            "extension": path.suffix.lower(),
            "exists": path.exists(),
            "is_file": path.is_file() if path.exists() else False,
            "file_size": path.stat().st_size if path.exists() else 0,
            "can_process": False,
            "processor": None,
            "error": None
        }
        
        if not result["exists"]:
            result["error"] = "File does not exist"
            return result
        
        if not result["is_file"]:
            result["error"] = "Path is not a file"
            return result
        
        processor = self.get_processor(file_path)
        if processor is None:
            result["error"] = f"No processor available for extension: {result['extension']}"
            return result
        
        result["processor"] = processor.__class__.__name__
        result["can_process"] = processor.can_process(file_path)
        
        if not result["can_process"]:
            result["error"] = f"Processor cannot handle this file"
        
        return result 