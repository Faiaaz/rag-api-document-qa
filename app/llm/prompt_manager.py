"""
Prompt manager for LLM interactions
"""
from typing import List, Dict, Any, Optional


class PromptManager:
    """Manages prompt templates for different use cases"""
    
    def __init__(self):
        """Initialize prompt manager with default templates"""
        self.templates = {
            "qa_with_context": self._get_qa_with_context_template(),
            "qa_with_sources": self._get_qa_with_sources_template(),
            "summarize": self._get_summarize_template(),
            "extract_keywords": self._get_extract_keywords_template(),
            "compare_documents": self._get_compare_documents_template()
        }
    
    def _get_qa_with_context_template(self) -> str:
        """Get template for Q&A with context"""
        return """You are a helpful assistant that answers questions based on the provided context. 

Instructions:
- Only use information from the provided context to answer the question
- If the context doesn't contain enough information to answer the question, say so clearly
- Be concise but comprehensive in your response
- If you're unsure about something, acknowledge the uncertainty

Context:
{context}

Question: {question}

Answer:"""
    
    def _get_qa_with_sources_template(self) -> str:
        """Get template for Q&A with multiple sources"""
        return """You are a helpful assistant that answers questions based on the provided sources.

Instructions:
- Use information from the provided sources to answer the question
- Cite the sources when providing information (e.g., "According to Source 1...")
- If the sources don't contain enough information, say so clearly
- Be accurate and cite specific sources for claims
- If sources contradict each other, acknowledge this

Sources:
{sources}

Question: {question}

Answer:"""
    
    def _get_summarize_template(self) -> str:
        """Get template for document summarization"""
        return """You are a helpful assistant that creates concise summaries of documents.

Instructions:
- Create a clear, concise summary of the provided content
- Focus on the main points and key information
- Maintain the original meaning and tone
- Keep the summary under 200 words unless specified otherwise

Content to summarize:
{content}

Summary:"""
    
    def _get_extract_keywords_template(self) -> str:
        """Get template for keyword extraction"""
        return """You are a helpful assistant that extracts key terms and concepts from text.

Instructions:
- Identify the most important keywords, concepts, and terms
- Focus on technical terms, proper nouns, and key concepts
- Return a list of relevant terms separated by commas
- Avoid common words unless they are contextually important

Content:
{content}

Key terms and concepts:"""
    
    def _get_compare_documents_template(self) -> str:
        """Get template for document comparison"""
        return """You are a helpful assistant that compares multiple documents.

Instructions:
- Compare the provided documents for similarities and differences
- Focus on key themes, topics, and information
- Identify any contradictions or complementary information
- Provide a structured comparison

Document 1:
{doc1}

Document 2:
{doc2}

Comparison:"""
    
    def format_prompt(self, 
                     template_name: str, 
                     **kwargs) -> str:
        """
        Format a prompt template with provided variables
        
        Args:
            template_name: Name of the template to use
            **kwargs: Variables to substitute in the template
            
        Returns:
            Formatted prompt string
        """
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name]
        return template.format(**kwargs)
    
    def format_qa_prompt(self, 
                        question: str, 
                        context: str,
                        include_sources: bool = False) -> str:
        """
        Format a Q&A prompt
        
        Args:
            question: User's question
            context: Retrieved context
            include_sources: Whether to include source information
            
        Returns:
            Formatted prompt
        """
        if include_sources:
            return self.format_prompt("qa_with_sources", sources=context, question=question)
        else:
            return self.format_prompt("qa_with_context", context=context, question=question)
    
    def format_search_results_for_prompt(self, 
                                       search_results: List[Dict[str, Any]]) -> str:
        """
        Format search results for use in prompts
        
        Args:
            search_results: List of search results
            
        Returns:
            Formatted context string
        """
        if not search_results:
            return "No relevant documents found."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            content = result.get('content', '')
            metadata = result.get('metadata', {})
            filename = metadata.get('filename', 'Unknown')
            score = result.get('score', 0)
            
            context_parts.append(f"Source {i} (from {filename}, relevance: {score:.3f}):\n{content}\n")
        
        return "\n".join(context_parts)
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template names"""
        return list(self.templates.keys())
    
    def add_custom_template(self, name: str, template: str):
        """
        Add a custom template
        
        Args:
            name: Template name
            template: Template string with placeholders
        """
        self.templates[name] = template
    
    def get_template(self, name: str) -> str:
        """Get a specific template"""
        if name not in self.templates:
            raise ValueError(f"Template '{name}' not found")
        return self.templates[name] 