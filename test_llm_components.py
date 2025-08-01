#!/usr/bin/env python3
"""
Test script for LLM components only
"""
import os

from app.llm import OpenAIClient, PromptManager


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


def test_qa_with_context():
    """Test Q&A with context functionality"""
    print("\n🧪 Testing Q&A with Context")
    print("=" * 40)
    
    try:
        # Initialize OpenAI client
        client = OpenAIClient(model="gpt-3.5-turbo")
        
        # Test Q&A with context
        question = "What is the main benefit of machine learning?"
        context = """
        Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.
        The main benefits include:
        1. Automation of complex tasks
        2. Pattern recognition in large datasets
        3. Predictive capabilities
        4. Continuous improvement over time
        """
        
        print(f"\nQuestion: {question}")
        print(f"Context: {context.strip()}")
        
        response = client.generate_answer_with_context(
            question=question,
            context=context,
            max_tokens=100
        )
        
        print(f"\nAnswer: {response['content']}")
        print(f"Usage: {response['usage']}")
        print(f"Processing time: {response['processing_time']:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Q&A with context test failed: {str(e)}")
        return False


def main():
    """Run LLM component tests"""
    print("🚀 LLM Components Test Suite")
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
        ("Q&A with Context", test_qa_with_context)
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