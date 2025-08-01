#!/usr/bin/env python3
"""
Test script for vector storage functionality
"""
import os
from pathlib import Path

from app.document_processor import DocumentProcessorFactory
from app.vector_store import EmbeddingManager, FAISSVectorStore


def create_test_documents():
    """Create test documents for vector storage testing"""
    test_dir = Path("test_vector_docs")
    test_dir.mkdir(exist_ok=True)
    
    # Create different types of test documents
    documents = {}
    
    # Document 1: Technical content
    tech_file = test_dir / "ai_technology.txt"
    with open(tech_file, 'w', encoding='utf-8') as f:
        f.write("Artificial Intelligence and Machine Learning\n")
        f.write("AI technology has revolutionized many industries.\n")
        f.write("Machine learning algorithms can process vast amounts of data.\n")
        f.write("Deep learning models use neural networks for complex tasks.\n")
        f.write("Natural language processing enables computers to understand human language.\n")
    documents['ai_tech'] = str(tech_file)
    
    # Document 2: Business content
    business_file = test_dir / "business_strategy.txt"
    with open(business_file, 'w', encoding='utf-8') as f:
        f.write("Business Strategy and Management\n")
        f.write("Effective business strategy requires careful planning.\n")
        f.write("Market analysis helps identify opportunities and threats.\n")
        f.write("Customer satisfaction is crucial for business success.\n")
        f.write("Innovation drives competitive advantage in the market.\n")
    documents['business'] = str(business_file)
    
    # Document 3: Science content
    science_file = test_dir / "climate_science.txt"
    with open(science_file, 'w', encoding='utf-8') as f:
        f.write("Climate Science and Environmental Studies\n")
        f.write("Climate change is a significant global challenge.\n")
        f.write("Greenhouse gas emissions affect global temperatures.\n")
        f.write("Renewable energy sources reduce environmental impact.\n")
        f.write("Sustainable practices help protect our planet.\n")
    documents['climate'] = str(science_file)
    
    print("✅ Test documents created successfully!")
    return documents


def test_vector_storage():
    """Test the complete vector storage system"""
    print("🧪 Testing Vector Storage System")
    print("=" * 50)
    
    # Create test documents
    documents = create_test_documents()
    
    # Initialize components
    print("\n🔧 Initializing components...")
    
    # Document processor
    processor_factory = DocumentProcessorFactory(chunk_size=150, chunk_overlap=50)
    
    # Embedding manager
    embedding_manager = EmbeddingManager(model_name="all-MiniLM-L6-v2")
    print(f"Embedding model: {embedding_manager.get_model_info()}")
    
    # Vector store
    vector_store = FAISSVectorStore(
        embedding_manager=embedding_manager,
        index_path="./data/vector_store",
        index_name="test_index"
    )
    
    print(f"Vector store stats: {vector_store.get_stats()}")
    
    # Process and add documents
    print("\n📄 Processing and adding documents...")
    all_chunks = []
    
    for doc_type, file_path in documents.items():
        print(f"\n  Processing {doc_type}: {Path(file_path).name}")
        
        # Process document
        chunks = processor_factory.process_document(file_path)
        print(f"    Created {len(chunks)} chunks")
        
        # Add to vector store
        chunk_ids = vector_store.add_documents(chunks)
        print(f"    Added to vector store with IDs: {chunk_ids}")
        
        all_chunks.extend(chunks)
    
    # Save vector store
    vector_store.save()
    print(f"\n💾 Vector store saved. Total chunks: {len(all_chunks)}")
    
    # Test similarity search
    print("\n🔍 Testing similarity search...")
    
    test_queries = [
        "machine learning algorithms",
        "business strategy planning", 
        "climate change impact",
        "artificial intelligence technology",
        "customer satisfaction importance"
    ]
    
    for query in test_queries:
        print(f"\n  Query: '{query}'")
        results = vector_store.search(query, top_k=3, threshold=0.1)
        
        if results:
            for i, result in enumerate(results, 1):
                score = result['score']
                content = result['content'][:100] + "..."
                filename = result['metadata']['filename']
                print(f"    {i}. Score: {score:.3f} | File: {filename}")
                print(f"       Content: {content}")
        else:
            print("    No results found")
    
    # Test specific document retrieval
    print(f"\n📋 Vector store statistics:")
    stats = vector_store.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n🎉 Vector storage test completed!")


def test_embedding_similarity():
    """Test embedding similarity calculations"""
    print("\n🧮 Testing Embedding Similarity")
    print("=" * 40)
    
    embedding_manager = EmbeddingManager()
    
    # Test similar texts
    similar_texts = [
        "machine learning algorithms",
        "ML algorithms and models",
        "artificial intelligence systems"
    ]
    
    # Test different texts
    different_texts = [
        "machine learning algorithms",
        "business strategy planning",
        "climate change science"
    ]
    
    print("\n  Testing similar texts:")
    embeddings = embedding_manager.generate_embeddings(similar_texts)
    for i in range(len(similar_texts)):
        for j in range(i+1, len(similar_texts)):
            sim = embedding_manager.similarity(embeddings[i], embeddings[j])
            print(f"    '{similar_texts[i][:20]}...' vs '{similar_texts[j][:20]}...': {sim:.3f}")
    
    print("\n  Testing different texts:")
    embeddings = embedding_manager.generate_embeddings(different_texts)
    for i in range(len(different_texts)):
        for j in range(i+1, len(different_texts)):
            sim = embedding_manager.similarity(embeddings[i], embeddings[j])
            print(f"    '{different_texts[i][:20]}...' vs '{different_texts[j][:20]}...': {sim:.3f}")


if __name__ == "__main__":
    test_vector_storage()
    test_embedding_similarity() 