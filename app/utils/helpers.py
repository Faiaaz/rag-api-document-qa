"""
Utility functions for the RAG API
"""
import os
import re
import uuid
import base64
from typing import List, Dict, Any, Optional
from pathlib import Path
import mimetypes

def generate_file_id() -> str:
    """Generate a unique file ID"""
    return str(uuid.uuid4())

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return Path(filename).suffix.lower()

def is_supported_file_type(filename: str) -> bool:
    """Check if file type is supported"""
    supported_extensions = {
        '.pdf', '.docx', '.txt', '.jpg', '.jpeg', '.png', 
        '.csv', '.db', '.sqlite', '.sqlite3'
    }
    return get_file_extension(filename) in supported_extensions

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If this is not the first chunk, include some overlap
        if start > 0:
            start = start - overlap
        
        # Extract the chunk
        chunk = text[start:end]
        
        # Clean the chunk
        chunk = clean_text(chunk)
        
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        # Move to next chunk
        start = end
    
    return chunks

def save_base64_image(base64_string: str, save_path: str) -> str:
    """
    Save base64 encoded image to file
    
    Args:
        base64_string: Base64 encoded image string
        save_path: Path where to save the image
    
    Returns:
        Path to saved image
    """
    try:
        # Remove data URL prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        # Decode and save
        image_data = base64.b64decode(base64_string)
        
        with open(save_path, 'wb') as f:
            f.write(image_data)
        
        return save_path
    except Exception as e:
        raise ValueError(f"Failed to save base64 image: {str(e)}")

def get_mime_type(filename: str) -> str:
    """Get MIME type for a file"""
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def create_directory_if_not_exists(directory_path: str) -> None:
    """Create directory if it doesn't exist"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def extract_metadata_from_filename(filename: str) -> Dict[str, Any]:
    """Extract metadata from filename"""
    path = Path(filename)
    return {
        "filename": filename,
        "name": path.stem,
        "extension": path.suffix.lower(),
        "size": 0,  # Will be updated when file is processed
        "upload_time": None  # Will be updated when file is uploaded
    } 