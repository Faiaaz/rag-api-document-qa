#!/usr/bin/env python3
"""
Manual API testing script for RAG API
"""
import requests
import json
import time
import os
from pathlib import Path
from create_test_files import create_test_files

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_stats():
    """Test stats endpoint"""
    print("\n📊 Testing Stats Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Stats check failed: {e}")
        return False

def upload_file(file_path):
    """Upload a file to the API"""
    print(f"\n📤 Uploading: {file_path.name}")
    print("-" * 30)
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'application/octet-stream')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful!")
            print(f"   File ID: {result.get('file_id')}")
            print(f"   Chunks processed: {result.get('chunks_processed')}")
            print(f"   Message: {result.get('message')}")
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def test_query(question, expected_topics=None):
    """Test query endpoint"""
    print(f"\n🔍 Query: '{question}'")
    print("-" * 40)
    
    try:
        payload = {
            "question": question,
            "top_k": 3
        }
        
        response = requests.post(f"{BASE_URL}/query", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Query successful!")
            print(f"   Answer: {result.get('answer', 'No answer')}")
            print(f"   Confidence: {result.get('confidence', 0):.3f}")
            print(f"   Processing time: {result.get('processing_time', 0):.2f}s")
            print(f"   Sources found: {len(result.get('sources', []))}")
            
            # Show sources
            sources = result.get('sources', [])
            if sources:
                print("   Sources:")
                for i, source in enumerate(sources, 1):
                    print(f"     {i}. {source.get('filename')} (score: {source.get('similarity_score', 0):.3f})")
            
            return True
        else:
            print(f"❌ Query failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False

def test_different_file_types():
    """Test uploading different file types"""
    print("\n📁 Testing Different File Types")
    print("=" * 50)
    
    # Create test files
    test_dir = create_test_files()
    
    # Test each file type
    file_types = [
        "sample_text.txt",
        "sample_markdown.md", 
        "sample_data.csv",
        "sample_config.json",
        "sample_webpage.html",
        "sample_log.log"
    ]
    
    uploaded_files = []
    
    for filename in file_types:
        file_path = test_dir / filename
        if file_path.exists():
            success = upload_file(file_path)
            if success:
                uploaded_files.append(filename)
            time.sleep(1)  # Small delay between uploads
    
    return uploaded_files

def test_various_queries():
    """Test various types of questions"""
    print("\n❓ Testing Various Queries")
    print("=" * 50)
    
    test_questions = [
        "What is machine learning?",
        "What are the features of the RAG API?",
        "What products are available and their prices?",
        "What technical content is discussed?",
        "What is the application version?",
        "What are the key features mentioned?",
        "What programming languages are discussed?",
        "What is the chunk size setting?",
        "What does the log show about the application startup?",
        "What web development topics are covered?"
    ]
    
    successful_queries = 0
    total_queries = len(test_questions)
    
    for question in test_questions:
        success = test_query(question)
        if success:
            successful_queries += 1
        time.sleep(2)  # Delay between queries
    
    print(f"\n📈 Query Results: {successful_queries}/{total_queries} successful")
    return successful_queries, total_queries

def test_error_handling():
    """Test error handling"""
    print("\n⚠️ Testing Error Handling")
    print("=" * 40)
    
    # Test invalid file upload
    print("\n📤 Testing invalid file upload...")
    try:
        files = {'file': ('invalid.xyz', b'fake content', 'application/octet-stream')}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test invalid query
    print("\n🔍 Testing invalid query...")
    try:
        payload = {"invalid_field": "test"}
        response = requests.post(f"{BASE_URL}/query", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all manual tests"""
    print("🧪 Manual API Testing Suite")
    print("=" * 60)
    
    # Check if API is running
    print("🔍 Checking if API is running...")
    if not test_health():
        print("❌ API is not running. Please start the API first:")
        print("   python -m uvicorn app.main:app --reload")
        return
    
    # Test stats
    test_stats()
    
    # Test file uploads
    uploaded_files = test_different_file_types()
    print(f"\n📁 Successfully uploaded {len(uploaded_files)} files")
    
    # Wait a moment for processing
    print("\n⏳ Waiting for files to be processed...")
    time.sleep(3)
    
    # Test queries
    successful, total = test_various_queries()
    
    # Test error handling
    test_error_handling()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    print(f"✅ Health Check: {'PASS' if test_health() else 'FAIL'}")
    print(f"📁 Files Uploaded: {len(uploaded_files)}")
    print(f"❓ Queries Successful: {successful}/{total}")
    print(f"🎯 Success Rate: {(successful/total)*100:.1f}%" if total > 0 else "N/A")
    
    print(f"\n🌐 API Documentation: {BASE_URL}/docs")
    print(f"📊 API Stats: {BASE_URL}/stats")

if __name__ == "__main__":
    main() 