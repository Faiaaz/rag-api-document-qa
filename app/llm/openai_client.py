"""
OpenAI client for LLM integration
"""
import os
import time
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI

from app.models import QueryResponse


class OpenAIClient:
    """OpenAI client for LLM communication"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key (if None, will use environment variable)
            model: Model to use for generation
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        print(f"OpenAI client initialized with model: {self.model}")
    
    def generate_response(self, 
                         messages: List[Dict[str, str]], 
                         max_tokens: int = 1000,
                         temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate response using OpenAI API
        
        Args:
            messages: List of message dictionaries
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-2)
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            start_time = time.time()
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract response
            content = response.choices[0].message.content
            usage = response.usage
            
            processing_time = time.time() - start_time
            
            return {
                "content": content,
                "model": self.model,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                },
                "processing_time": processing_time,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def generate_answer_with_context(self, 
                                   question: str, 
                                   context: str,
                                   max_tokens: int = 1000,
                                   temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate answer based on question and context
        
        Args:
            question: User's question
            context: Retrieved context from documents
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Dictionary with answer and metadata
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context. Only use information from the context to answer the question. If the context doesn't contain enough information to answer the question, say so clearly."
            },
            {
                "role": "user", 
                "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
            }
        ]
        
        return self.generate_response(messages, max_tokens, temperature)
    
    def generate_answer_with_sources(self, 
                                   question: str, 
                                   search_results: List[Dict[str, Any]],
                                   max_tokens: int = 1000,
                                   temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate answer with source information
        
        Args:
            question: User's question
            search_results: List of search results with content and metadata
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Dictionary with answer and metadata
        """
        # Format context with source information
        context_parts = []
        for i, result in enumerate(search_results, 1):
            content = result.get('content', '')
            metadata = result.get('metadata', {})
            filename = metadata.get('filename', 'Unknown')
            score = result.get('score', 0)
            
            context_parts.append(f"Source {i} (from {filename}, relevance: {score:.3f}):\n{content}\n")
        
        context = "\n".join(context_parts)
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided sources. Use information from the sources to answer the question. Cite the sources when providing information. If the sources don't contain enough information to answer the question, say so clearly."
            },
            {
                "role": "user",
                "content": f"Sources:\n{context}\n\nQuestion: {question}\n\nAnswer:"
            }
        ]
        
        return self.generate_response(messages, max_tokens, temperature)
    
    def test_connection(self) -> Dict[str, Any]:
        """Test OpenAI API connection"""
        try:
            messages = [{"role": "user", "content": "Hello, this is a test message."}]
            response = self.generate_response(messages, max_tokens=10)
            
            return {
                "success": True,
                "message": "OpenAI API connection successful",
                "model": self.model,
                "test_response": response["content"]
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"OpenAI API connection failed: {str(e)}",
                "model": self.model
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model": self.model,
            "api_key_configured": bool(self.api_key),
            "client_initialized": hasattr(self, 'client')
        } 