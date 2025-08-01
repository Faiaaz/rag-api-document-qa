#!/usr/bin/env python3
"""
Test script for document processing functionality
"""
import os
import tempfile
from pathlib import Path

from app.document_processor import DocumentProcessorFactory


def create_test_files():
    """Create test files for different document types"""
    test_files = {}
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test 1: Text file
        text_file = temp_path / "test.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("This is a test text file.\n")
            f.write("It contains multiple lines of text.\n")
            f.write("This will be used to test the text processor.\n")
        test_files['text'] = str(text_file)
        
        # Test 2: CSV file
        csv_file = temp_path / "test.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Name,Age,City\n")
            f.write("John,25,New York\n")
            f.write("Jane,30,Los Angeles\n")
            f.write("Bob,35,Chicago\n")
        test_files['csv'] = str(csv_file)
        
        # Test 3: Markdown file
        md_file = temp_path / "test.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Test Document\n\n")
            f.write("This is a **markdown** file.\n\n")
            f.write("- Item 1\n")
            f.write("- Item 2\n")
            f.write("- Item 3\n")
        test_files['markdown'] = str(md_file)
        
        print("✅ Test files created successfully!")
        return test_files


def test_document_processing():
    """Test the document processing functionality"""
    print("🧪 Testing Document Processing System")
    print("=" * 50)
    
    # Create test files
    test_files = create_test_files()
    
    # Initialize the processor factory
    factory = DocumentProcessorFactory(chunk_size=500, chunk_overlap=100)
    
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
                print(f"    Metadata: {first_chunk.metadata}")
            
        except Exception as e:
            print(f"  ❌ Error processing file: {str(e)}")
    
    print(f"\n🎉 Document processing test completed!")


def test_processor_validation():
    """Test processor validation with invalid files"""
    print("\n🔍 Testing Processor Validation")
    print("=" * 40)
    
    factory = DocumentProcessorFactory()
    
    # Test cases
    test_cases = [
        "nonexistent_file.txt",
        "test.unsupported",
        "/invalid/path/file.pdf"
    ]
    
    for test_file in test_cases:
        print(f"\n📄 Testing: {test_file}")
        validation = factory.validate_file(test_file)
        
        print(f"  Can process: {validation['can_process']}")
        print(f"  Processor: {validation['processor']}")
        if validation['error']:
            print(f"  Error: {validation['error']}")


if __name__ == "__main__":
    test_document_processing()
    test_processor_validation() 