"""
Image processor with OCR capabilities using pytesseract
"""
import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import List, Dict, Any
from pathlib import Path
import os

from .base_processor import BaseDocumentProcessor


class ImageProcessor(BaseDocumentProcessor):
    """Processor for images with OCR text extraction"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(chunk_size, chunk_overlap)
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
    
    def can_process(self, file_path: str) -> bool:
        """Check if this processor can handle the given file"""
        if not self.validate_file(file_path):
            return False
        
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_extensions
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from image using OCR
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Extracted text content
        """
        try:
            # Open image using PIL
            image = Image.open(file_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(image)
            
            return text
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from image {file_path}: {str(e)}")
    
    def extract_text_with_preprocessing(self, file_path: str) -> str:
        """
        Extract text from image with preprocessing for better OCR results
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Extracted text content
        """
        try:
            # Read image using OpenCV
            image = cv2.imread(file_path)
            
            if image is None:
                raise ValueError(f"Could not read image file: {file_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply preprocessing for better OCR
            # 1. Noise reduction
            denoised = cv2.medianBlur(gray, 3)
            
            # 2. Thresholding to get binary image
            _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # 3. Morphological operations to remove noise
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # Extract text using pytesseract with custom configuration
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed, config=custom_config)
            
            return text
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from image with preprocessing {file_path}: {str(e)}")
    
    def extract_text_with_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text with additional metadata from image
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dictionary containing text and metadata
        """
        try:
            # Get image info
            image = Image.open(file_path)
            stat_info = os.stat(file_path)
            
            # Extract text
            text = self.extract_text(file_path)
            
            # Get image metadata
            width, height = image.size
            format_name = image.format
            mode = image.mode
            
            return {
                "text": text,
                "file_size": stat_info.st_size,
                "image_width": width,
                "image_height": height,
                "image_format": format_name,
                "image_mode": mode,
                "text_length": len(text),
                "word_count": len(text.split()),
                "created_time": stat_info.st_ctime,
                "modified_time": stat_info.st_mtime
            }
            
        except Exception as e:
            raise ValueError(f"Failed to extract text and metadata from image {file_path}: {str(e)}")
    
    def get_image_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get basic information about the image
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dictionary with image information
        """
        try:
            image = Image.open(file_path)
            stat_info = os.stat(file_path)
            
            return {
                "width": image.size[0],
                "height": image.size[1],
                "format": image.format,
                "mode": image.mode,
                "file_size": stat_info.st_size,
                "dpi": image.info.get('dpi', (None, None))
            }
            
        except Exception as e:
            raise ValueError(f"Failed to get image info for {file_path}: {str(e)}")
    
    def is_image_readable(self, file_path: str) -> bool:
        """
        Check if the image file is readable and valid
        
        Args:
            file_path: Path to the image file
            
        Returns:
            True if image is readable
        """
        try:
            with Image.open(file_path) as image:
                image.verify()
            return True
        except Exception:
            return False 