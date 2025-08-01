"""
RAG (Retrieval-Augmented Generation) pipeline
Combines document retrieval with LLM generation
"""
import time
from typing import List, Dict, Any, Optional

from app.models import QueryResponse, QueryRequest
from app.document_service import DocumentService
from .openai_client import OpenAIClient
from .prompt_manager import PromptManager


class RAGPipeline:
    """RAG pipeline for question answering"""
    
    def __init__(self, 
                 document_service: DocumentService,
                 openai_client: OpenAIClient,
                 prompt_manager: Optional[PromptManager] = None):
        """
        Initialize RAG pipeline
        
        Args:
            document_service: Document service for retrieval
            openai_client: OpenAI client for generation
            prompt_manager: Prompt manager (optional, will create default if None)
        """
        self.document_service = document_service
        self.openai_client = openai_client
        self.prompt_manager = prompt_manager or PromptManager()
        
        print("RAG pipeline initialized successfully")
    
    def answer_question(self, 
                       question: str, 
                       top_k: int = 5,
                       threshold: float = 0.1,
                       max_tokens: int = 1000,
                       temperature: float = 0.7,
                       include_sources: bool = True) -> QueryResponse:
        """
        Answer a question using RAG pipeline
        
        Args:
            question: User's question
            top_k: Number of top documents to retrieve
            threshold: Minimum similarity threshold
            max_tokens: Maximum tokens for LLM response
            temperature: Sampling temperature
            include_sources: Whether to include source information
            
        Returns:
            QueryResponse with answer and metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Retrieve relevant documents
            print(f"🔍 Retrieving documents for: '{question}'")
            search_results = self.document_service.search_documents(
                query=question,
                top_k=top_k,
                threshold=threshold
            )
            
            if not search_results:
                # No relevant documents found
                answer = "I couldn't find any relevant information in the documents to answer your question."
                confidence = 0.0
                sources = []
            else:
                # Step 2: Generate answer using LLM
                print(f"🤖 Generating answer using {len(search_results)} sources")
                llm_response = self.openai_client.generate_answer_with_sources(
                    question=question,
                    search_results=search_results,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                answer = llm_response["content"]
                confidence = self._calculate_confidence(search_results)
                sources = self._format_sources(search_results)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create response
            response = QueryResponse(
                answer=answer,
                sources=sources,
                confidence=confidence,
                processing_time=processing_time
            )
            
            print(f"✅ Question answered in {processing_time:.2f}s with confidence {confidence:.3f}")
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Error processing question: {str(e)}"
            print(f"❌ {error_msg}")
            
            return QueryResponse(
                answer=f"I encountered an error while processing your question: {error_msg}",
                sources=[],
                confidence=0.0,
                processing_time=processing_time
            )
    
    def answer_question_with_request(self, request: QueryRequest) -> QueryResponse:
        """
        Answer a question using QueryRequest object
        
        Args:
            request: QueryRequest object
            
        Returns:
            QueryResponse with answer
        """
        return self.answer_question(
            question=request.question,
            top_k=request.top_k,
            threshold=0.1,  # Default threshold
            include_sources=True
        )
    
    def _calculate_confidence(self, search_results: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score based on search results
        
        Args:
            search_results: List of search results
            
        Returns:
            Confidence score (0-1)
        """
        if not search_results:
            return 0.0
        
        # Use average similarity score as confidence
        scores = [result.get('score', 0) for result in search_results]
        avg_score = sum(scores) / len(scores)
        
        # Normalize to 0-1 range (assuming scores are already in this range)
        return min(avg_score, 1.0)
    
    def _format_sources(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format search results for response
        
        Args:
            search_results: List of search results
            
        Returns:
            List of formatted source information
        """
        sources = []
        for result in search_results:
            metadata = result.get('metadata', {})
            source_info = {
                "filename": metadata.get('filename', 'Unknown'),
                "chunk_index": metadata.get('chunk_index', 0),
                "total_chunks": metadata.get('total_chunks', 1),
                "processor": metadata.get('processor', 'Unknown'),
                "similarity_score": result.get('score', 0),
                "content_preview": result.get('content', '')[:200] + "..."
            }
            sources.append(source_info)
        
        return sources
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """Get information about the RAG pipeline"""
        return {
            "document_service_stats": self.document_service.get_document_stats(),
            "openai_model_info": self.openai_client.get_model_info(),
            "available_prompts": self.prompt_manager.get_available_templates(),
            "pipeline_components": [
                "DocumentService",
                "OpenAIClient", 
                "PromptManager"
            ]
        }
    
    def test_pipeline(self) -> Dict[str, Any]:
        """Test the complete RAG pipeline"""
        test_question = "What is the main topic of the documents?"
        
        try:
            # Test document service
            doc_stats = self.document_service.get_document_stats()
            
            # Test OpenAI connection
            openai_test = self.openai_client.test_connection()
            
            # Test RAG pipeline
            if doc_stats['total_chunks'] > 0:
                response = self.answer_question(test_question, top_k=1)
                rag_success = True
                rag_answer = response.answer[:100] + "..."
            else:
                rag_success = False
                rag_answer = "No documents available for testing"
            
            return {
                "success": True,
                "document_service": {
                    "status": "ready",
                    "total_chunks": doc_stats['total_chunks']
                },
                "openai_client": openai_test,
                "rag_pipeline": {
                    "status": "ready" if rag_success else "no_documents",
                    "test_answer": rag_answer
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "document_service": {"status": "error"},
                "openai_client": {"status": "error"},
                "rag_pipeline": {"status": "error"}
            } 