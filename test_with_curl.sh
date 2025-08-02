#!/bin/bash

# Manual API testing with curl commands
BASE_URL="http://localhost:8000"

echo "🧪 Manual API Testing with curl"
echo "================================"

# Test health endpoint
echo "🏥 Testing Health Endpoint..."
curl -s -X GET "$BASE_URL/health" | jq '.'

# Test stats endpoint
echo -e "\n📊 Testing Stats Endpoint..."
curl -s -X GET "$BASE_URL/stats" | jq '.'

# Test upload endpoint (if you have a test file)
echo -e "\n📤 Testing Upload Endpoint..."
if [ -f "manual_test_files/sample_text.txt" ]; then
    curl -s -X POST "$BASE_URL/upload" \
        -F "file=@manual_test_files/sample_text.txt" | jq '.'
else
    echo "No test file found. Create test files first with: python create_test_files.py"
fi

# Test query endpoint
echo -e "\n🔍 Testing Query Endpoint..."
curl -s -X POST "$BASE_URL/query" \
    -H "Content-Type: application/json" \
    -d '{
        "question": "What is machine learning?",
        "top_k": 3
    }' | jq '.'

# Test another query
echo -e "\n🔍 Testing Another Query..."
curl -s -X POST "$BASE_URL/query" \
    -H "Content-Type: application/json" \
    -d '{
        "question": "What are the features of the RAG API?",
        "top_k": 3
    }' | jq '.'

echo -e "\n✅ Testing completed!"
echo "🌐 API Documentation: $BASE_URL/docs" 