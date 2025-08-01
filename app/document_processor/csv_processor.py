"""
CSV processor for handling CSV files and extracting structured data
"""
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
import os

from .base_processor import BaseDocumentProcessor


class CSVProcessor(BaseDocumentProcessor):
    """Processor for CSV files"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(chunk_size, chunk_overlap)
        self.supported_extensions = {'.csv', '.tsv'}
    
    def can_process(self, file_path: str) -> bool:
        """Check if this processor can handle the given file"""
        if not self.validate_file(file_path):
            return False
        
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_extensions
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Extracted text content
        """
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Convert DataFrame to text representation
            text_content = []
            
            # Add column headers
            headers = " | ".join(df.columns.tolist())
            text_content.append(f"Headers: {headers}")
            text_content.append("")
            
            # Add data rows
            for index, row in df.iterrows():
                row_text = " | ".join([str(value) for value in row.values])
                text_content.append(f"Row {index + 1}: {row_text}")
            
            return "\n".join(text_content)
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from CSV file {file_path}: {str(e)}")
    
    def extract_text_with_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text with additional metadata from CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dictionary containing text and metadata
        """
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            stat_info = os.stat(file_path)
            
            # Get DataFrame info
            shape = df.shape
            columns = df.columns.tolist()
            dtypes = df.dtypes.to_dict()
            
            # Convert DataFrame to text
            text_content = []
            text_content.append(f"CSV File: {Path(file_path).name}")
            text_content.append(f"Dimensions: {shape[0]} rows x {shape[1]} columns")
            text_content.append("")
            
            # Add column information
            text_content.append("Columns:")
            for col in columns:
                text_content.append(f"  - {col} ({dtypes[col]})")
            text_content.append("")
            
            # Add sample data
            text_content.append("Sample Data:")
            headers = " | ".join(columns)
            text_content.append(f"Headers: {headers}")
            
            # Add first few rows
            for index, row in df.head(10).iterrows():
                row_text = " | ".join([str(value) for value in row.values])
                text_content.append(f"Row {index + 1}: {row_text}")
            
            if len(df) > 10:
                text_content.append(f"... and {len(df) - 10} more rows")
            
            return {
                "text": "\n".join(text_content),
                "file_size": stat_info.st_size,
                "row_count": shape[0],
                "column_count": shape[1],
                "columns": columns,
                "data_types": {str(k): str(v) for k, v in dtypes.items()},
                "created_time": stat_info.st_ctime,
                "modified_time": stat_info.st_mtime
            }
            
        except Exception as e:
            raise ValueError(f"Failed to extract text and metadata from CSV file {file_path}: {str(e)}")
    
    def get_dataframe_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get detailed information about the CSV DataFrame
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dictionary with DataFrame information
        """
        try:
            df = pd.read_csv(file_path)
            
            return {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "null_counts": df.isnull().sum().to_dict(),
                "unique_counts": {col: df[col].nunique() for col in df.columns},
                "sample_values": {col: df[col].dropna().head(3).tolist() for col in df.columns}
            }
            
        except Exception as e:
            raise ValueError(f"Failed to get DataFrame info for {file_path}: {str(e)}")
    
    def extract_structured_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract structured data from CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dictionary with structured data
        """
        try:
            df = pd.read_csv(file_path)
            
            return {
                "data": df.to_dict('records'),
                "columns": df.columns.tolist(),
                "shape": df.shape,
                "summary_stats": df.describe().to_dict()
            }
            
        except Exception as e:
            raise ValueError(f"Failed to extract structured data from {file_path}: {str(e)}") 