"""
Vector store package for RAG API
Handles embeddings and similarity search
"""

from .faiss_store import FAISSVectorStore
from .embedding_manager import EmbeddingManager

__all__ = [
    'FAISSVectorStore',
    'EmbeddingManager'
] 