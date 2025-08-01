"""
Text file processor for plain text files
"""
from typing import List, Dict, Any
from pathlib import Path
import os

from .base_processor import BaseDocumentProcessor


class TextProcessor(BaseDocumentProcessor):
    """Processor for plain text files"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(chunk_size, chunk_overlap)
        self.supported_extensions = {'.txt', '.md', '.rst', '.log', '.csv', '.json', '.xml', '.html', '.htm'}
    
    def can_process(self, file_path: str) -> bool:
        """Check if this processor can handle the given file"""
        if not self.validate_file(file_path):
            return False
        
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_extensions
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Extracted text content
        """
        try:
            # Try to read with UTF-8 encoding first
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                # If UTF-8 fails, try with latin-1 encoding
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
            
            return content
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from file {file_path}: {str(e)}")
    
    def extract_text_with_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text with additional metadata from text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Dictionary containing text and metadata
        """
        try:
            # Get file stats
            stat_info = os.stat(file_path)
            
            # Extract text
            text = self.extract_text(file_path)
            
            # Count lines and words
            lines = text.split('\n')
            words = text.split()
            
            return {
                "text": text,
                "file_size": stat_info.st_size,
                "line_count": len(lines),
                "word_count": len(words),
                "character_count": len(text),
                "created_time": stat_info.st_ctime,
                "modified_time": stat_info.st_mtime,
                "encoding": "utf-8"  # We'll assume UTF-8 for now
            }
            
        except Exception as e:
            raise ValueError(f"Failed to extract text and metadata from file {file_path}: {str(e)}")
    
    def detect_encoding(self, file_path: str) -> str:
        """
        Detect the encoding of a text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Detected encoding
        """
        import chardet
        
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8' 