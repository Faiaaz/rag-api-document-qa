#!/usr/bin/env python3
"""
Test script for LLM integration and RAG pipeline
"""
import os
from pathlib import Path

from app.document_service import DocumentService
from app.llm import OpenAIClient, PromptManager, RAGPipeline


def create_test_documents():
    """Create test documents for LLM testing"""
    test_dir = Path("test_llm_docs")
    test_dir.mkdir(exist_ok=True)
    
    documents = {}
    
    # Create a technical document about AI
    ai_file = test_dir / "artificial_intelligence.txt"
    with open(ai_file, 'w', encoding='utf-8') as f:
        f.write("Artificial Intelligence: A Comprehensive Overview\n")
        f.write("Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines.\n")
        f.write("Machine learning is a subset of AI that enables computers to learn and improve from experience.\n")
        f.write("Deep learning uses neural networks with multiple layers to process complex data patterns.\n")
        f.write("Natural Language Processing (NLP) allows computers to understand and generate human language.\n")
        f.write("AI applications include virtual assistants, recommendation systems, and autonomous vehicles.\n")
    documents['ai'] = str(ai_file)
    
    # Create a business document
    business_file = test_dir / "business_analytics.txt"
    with open(business_file, 'w', encoding='utf-8') as f:
        f.write("Business Analytics and Data-Driven Decision Making\n")
        f.write("Business analytics involves analyzing data to make informed business decisions.\n")
        f.write("Data visualization helps present complex information in an understandable format.\n")
        f.write("Predictive analytics uses historical data to forecast future trends.\n")
        f.write("Key performance indicators (KPIs) measure business success and progress.\n")
        f.write("Business intelligence tools help organizations gain insights from their data.\n")
    documents['business'] = str(business_file)
    
    print("✅ Test documents created successfully!")
    return documents


def test_openai_client():
    """Test OpenAI client functionality"""
    print("🧪 Testing OpenAI Client")
    print("=" * 40)
    
    try:
        # Initialize OpenAI client
        client = OpenAIClient(model="gpt-3.5-turbo")
        
        # Test connection
        print("\n🔗 Testing OpenAI connection...")
        connection_test = client.test_connection()
        print(f"Connection test: {connection_test}")
        
        # Test simple response generation
        print("\n💬 Testing response generation...")
        messages = [{"role": "user", "content": "What is artificial intelligence in one sentence?"}]
        response = client.generate_response(messages, max_tokens=50)
        print(f"Response: {response['content']}")
        print(f"Usage: {response['usage']}")
        
        # Test model info
        print(f"\n📋 Model info: {client.get_model_info()}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI client test failed: {str(e)}")
        return False


def test_prompt_manager():
    """Test prompt manager functionality"""
    print("\n🧪 Testing Prompt Manager")
    print("=" * 40)
    
    try:
        # Initialize prompt manager
        prompt_manager = PromptManager()
        
        # Test available templates
        print(f"\n📝 Available templates: {prompt_manager.get_available_templates()}")
        
        # Test Q&A prompt formatting
        print("\n🔤 Testing Q&A prompt formatting...")
        question = "What is machine learning?"
        context = "Machine learning is a subset of AI that enables computers to learn from data."
        
        qa_prompt = prompt_manager.format_qa_prompt(question, context)
        print(f"Q&A Prompt:\n{qa_prompt}")
        
        # Test source formatting
        print("\n📚 Testing source formatting...")
        search_results = [
            {
                "content": "Machine learning algorithms can process vast amounts of data.",
                "metadata": {"filename": "ai_document.txt"},
                "score": 0.85
            }
        ]
        
        formatted_sources = prompt_manager.format_search_results_for_prompt(search_results)
        print(f"Formatted sources:\n{formatted_sources}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt manager test failed: {str(e)}")
        return False


def test_rag_pipeline():
    """Test complete RAG pipeline"""
    print("\n🧪 Testing RAG Pipeline")
    print("=" * 50)
    
    try:
        # Create test documents
        documents = create_test_documents()
        
        # Initialize components
        print("\n🔧 Initializing components...")
        
        # Document service
        document_service = DocumentService(
            chunk_size=200,
            chunk_overlap=50,
            embedding_model="all-MiniLM-L6-v2"
        )
        
        # Process documents
        print("\n📄 Processing documents...")
        for doc_type, file_path in documents.items():
            print(f"  Processing {doc_type}: {Path(file_path).name}")
            response = document_service.process_and_store_document(file_path)
            print(f"    Status: {response.status}, Chunks: {response.chunks_processed}")
        
        # OpenAI client
        openai_client = OpenAIClient(model="gpt-3.5-turbo")
        
        # Prompt manager
        prompt_manager = PromptManager()
        
        # RAG pipeline
        rag_pipeline = RAGPipeline(
            document_service=document_service,
            openai_client=openai_client,
            prompt_manager=prompt_manager
        )
        
        # Test pipeline
        print("\n🔍 Testing RAG pipeline...")
        test_questions = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "What are the applications of business analytics?",
            "What is deep learning?"
        ]
        
        for question in test_questions:
            print(f"\n  Question: '{question}'")
            response = rag_pipeline.answer_question(question, top_k=3)
            
            print(f"    Answer: {response.answer[:150]}...")
            print(f"    Confidence: {response.confidence:.3f}")
            print(f"    Processing time: {response.processing_time:.2f}s")
            print(f"    Sources: {len(response.sources)} found")
        
        # Test pipeline info
        print(f"\n📊 Pipeline info: {rag_pipeline.get_pipeline_info()}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG pipeline test failed: {str(e)}")
        return False


def main():
    """Run all LLM integration tests"""
    print("🚀 LLM Integration Test Suite")
    print("=" * 60)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in environment variables.")
        print("   Please set your OpenAI API key to test LLM functionality.")
        print("   You can set it with: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Run tests
    tests = [
        ("OpenAI Client", test_openai_client),
        ("Prompt Manager", test_prompt_manager),
        ("RAG Pipeline", test_rag_pipeline)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 Test Results Summary:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")


if __name__ == "__main__":
    main() 