#!/usr/bin/env python3
"""
Simple test script for document processing functionality
"""
import os
from pathlib import Path

from app.document_processor import DocumentProcessorFactory


def create_test_files():
    """Create test files in the current directory"""
    test_files = {}
    
    # Create test directory
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Test 1: Text file
    text_file = test_dir / "test.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("This is a test text file.\n")
        f.write("It contains multiple lines of text.\n")
        f.write("This will be used to test the text processor.\n")
        f.write("The text processor should be able to extract all this content.\n")
        f.write("And split it into appropriate chunks for processing.\n")
    test_files['text'] = str(text_file)
    
    # Test 2: CSV file
    csv_file = test_dir / "test.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("Name,Age,City,Occupation\n")
        f.write("John,25,New York,Engineer\n")
        f.write("Jane,30,Los Angeles,Designer\n")
        f.write("Bob,35,Chicago,Manager\n")
        f.write("Alice,28,Boston,Developer\n")
    test_files['csv'] = str(csv_file)
    
    # Test 3: Markdown file
    md_file = test_dir / "test.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Test Document\n\n")
        f.write("This is a **markdown** file.\n\n")
        f.write("## Features\n\n")
        f.write("- Item 1: Text processing\n")
        f.write("- Item 2: Document chunking\n")
        f.write("- Item 3: Metadata extraction\n\n")
        f.write("## Summary\n\n")
        f.write("This document contains various markdown elements.\n")
    test_files['markdown'] = str(md_file)
    
    print("✅ Test files created in 'test_files' directory!")
    return test_files


def test_document_processing():
    """Test the document processing functionality"""
    print("🧪 Testing Document Processing System")
    print("=" * 50)
    
    # Create test files
    test_files = create_test_files()
    
    # Initialize the processor factory
    factory = DocumentProcessorFactory(chunk_size=200, chunk_overlap=50)
    
    print(f"\n📋 Supported file extensions: {factory.get_supported_extensions()}")
    print(f"\n🔧 Available processors:")
    for name, info in factory.get_processor_info().items():
        print(f"  - {name}: {info['supported_extensions']}")
    
    # Test each file
    for file_type, file_path in test_files.items():
        print(f"\n📄 Testing {file_type.upper()} file: {Path(file_path).name}")
        print("-" * 40)
        
        # Validate file
        validation = factory.validate_file(file_path)
        print(f"  Validation: {validation['can_process']}")
        if validation['error']:
            print(f"  Error: {validation['error']}")
            continue
        
        # Process document
        try:
            chunks = factory.process_document(file_path)
            print(f"  ✅ Successfully processed into {len(chunks)} chunks")
            
            # Show first chunk
            if chunks:
                first_chunk = chunks[0]
                print(f"  📝 First chunk preview:")
                print(f"    Content: {first_chunk.content[:100]}...")
                print(f"    Metadata keys: {list(first_chunk.metadata.keys())}")
            
        except Exception as e:
            print(f"  ❌ Error processing file: {str(e)}")
    
    print(f"\n🎉 Document processing test completed!")


if __name__ == "__main__":
    test_document_processing() 