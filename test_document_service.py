#!/usr/bin/env python3
"""
Test script for unified document service
"""
import os
from pathlib import Path

from app.document_service import DocumentService


def create_test_documents():
    """Create test documents for the service"""
    test_dir = Path("test_service_docs")
    test_dir.mkdir(exist_ok=True)
    
    documents = {}
    
    # Create a technical document
    tech_file = test_dir / "python_programming.txt"
    with open(tech_file, 'w', encoding='utf-8') as f:
        f.write("Python Programming Guide\n")
        f.write("Python is a high-level programming language known for its simplicity.\n")
        f.write("It supports multiple programming paradigms including procedural and object-oriented programming.\n")
        f.write("Python has extensive libraries for data science, web development, and automation.\n")
        f.write("The language emphasizes code readability with its clean syntax.\n")
    documents['python'] = str(tech_file)
    
    # Create a business document
    business_file = test_dir / "project_management.txt"
    with open(business_file, 'w', encoding='utf-8') as f:
        f.write("Project Management Best Practices\n")
        f.write("Effective project management requires clear goals and timelines.\n")
        f.write("Team collaboration and communication are essential for project success.\n")
        f.write("Risk management helps identify and mitigate potential issues.\n")
        f.write("Regular progress tracking ensures projects stay on schedule.\n")
    documents['project'] = str(business_file)
    
    print("✅ Test documents created successfully!")
    return documents


def test_document_service():
    """Test the unified document service"""
    print("🧪 Testing Unified Document Service")
    print("=" * 50)
    
    # Create test documents
    documents = create_test_documents()
    
    # Initialize document service
    print("\n🔧 Initializing document service...")
    service = DocumentService(
        chunk_size=200,
        chunk_overlap=50,
        embedding_model="all-MiniLM-L6-v2"
    )
    
    # Get initial stats
    print(f"\n📊 Initial stats: {service.get_document_stats()}")
    
    # Process and store documents
    print("\n📄 Processing and storing documents...")
    for doc_type, file_path in documents.items():
        print(f"\n  Processing {doc_type}: {Path(file_path).name}")
        
        # Process document
        response = service.process_and_store_document(file_path)
        
        print(f"    Status: {response.status}")
        print(f"    Message: {response.message}")
        print(f"    Chunks processed: {response.chunks_processed}")
    
    # Get updated stats
    print(f"\n📊 Updated stats: {service.get_document_stats()}")
    
    # Test search functionality
    print("\n🔍 Testing search functionality...")
    
    test_queries = [
        "python programming language",
        "project management practices",
        "data science libraries",
        "team collaboration",
        "code readability"
    ]
    
    for query in test_queries:
        print(f"\n  Query: '{query}'")
        results = service.search_documents(query, top_k=3, threshold=0.1)
        
        if results:
            for i, result in enumerate(results, 1):
                score = result['score']
                content = result['content'][:80] + "..."
                filename = result['metadata']['filename']
                print(f"    {i}. Score: {score:.3f} | File: {filename}")
                print(f"       Content: {content}")
        else:
            print("    No results found")
    
    # Test document deletion
    print(f"\n🗑️ Testing document deletion...")
    test_filename = "python_programming.txt"
    deletion_result = service.delete_document(test_filename)
    print(f"  Deletion result: {deletion_result}")
    
    # Get final stats
    print(f"\n📊 Final stats: {service.get_document_stats()}")
    
    # Test processing status
    print(f"\n📈 Processing status: {service.get_processing_status()}")
    
    print(f"\n🎉 Document service test completed!")


if __name__ == "__main__":
    test_document_service() 