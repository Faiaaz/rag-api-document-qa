"""
FAISS vector store for efficient similarity search
"""
import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json

from app.models import DocumentChunk
from .embedding_manager import EmbeddingManager


class FAISSVectorStore:
    """FAISS-based vector store for document embeddings"""
    
    def __init__(self, 
                 embedding_manager: EmbeddingManager,
                 index_path: str = "./data/vector_store",
                 index_name: str = "document_index"):
        """
        Initialize the FAISS vector store
        
        Args:
            embedding_manager: EmbeddingManager instance
            index_path: Path to store the FAISS index
            index_name: Name of the index file
        """
        self.embedding_manager = embedding_manager
        self.index_path = Path(index_path)
        self.index_name = index_name
        
        # Create directory if it doesn't exist
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize FAISS index
        self.index = None
        self.metadata_store = []
        self.chunk_store = []
        self.is_initialized = False
        
        # Load existing index if available
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing index or create a new one"""
        index_file = self.index_path / f"{self.index_name}.faiss"
        metadata_file = self.index_path / f"{self.index_name}_metadata.pkl"
        chunks_file = self.index_path / f"{self.index_name}_chunks.pkl"
        
        if index_file.exists() and metadata_file.exists() and chunks_file.exists():
            print(f"Loading existing FAISS index from {index_file}")
            try:
                # Load FAISS index
                self.index = faiss.read_index(str(index_file))
                
                # Load metadata
                with open(metadata_file, 'rb') as f:
                    self.metadata_store = pickle.load(f)
                
                # Load chunks
                with open(chunks_file, 'rb') as f:
                    self.chunk_store = pickle.load(f)
                
                self.is_initialized = True
                print(f"Successfully loaded index with {len(self.metadata_store)} vectors")
                
            except Exception as e:
                print(f"Failed to load existing index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create a new FAISS index"""
        print("Creating new FAISS index")
        dimension = self.embedding_manager.get_embedding_dimension()
        
        # Create a flat index for cosine similarity
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        self.metadata_store = []
        self.chunk_store = []
        self.is_initialized = True
        
        print(f"Created new FAISS index with dimension {dimension}")
    
    def add_documents(self, chunks: List[DocumentChunk]) -> List[int]:
        """
        Add document chunks to the vector store
        
        Args:
            chunks: List of DocumentChunk objects
            
        Returns:
            List of chunk IDs
        """
        if not chunks:
            return []
        
        # Generate embeddings for chunks
        embeddings = self.embedding_manager.generate_embeddings_for_chunks(chunks)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to FAISS index
        start_id = len(self.metadata_store)
        self.index.add(embeddings)
        
        # Store metadata and chunks
        chunk_ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = start_id + i
            
            # Add embedding to chunk
            chunk.embedding = embeddings[i].tolist()
            
            # Store metadata
            metadata = {
                "chunk_id": chunk_id,
                "filename": chunk.metadata.get("filename", ""),
                "chunk_index": chunk.metadata.get("chunk_index", 0),
                "total_chunks": chunk.metadata.get("total_chunks", 1),
                "processor": chunk.metadata.get("processor", ""),
                "file_size": chunk.metadata.get("size", 0),
                "chunk_length": chunk.metadata.get("chunk_length", 0)
            }
            
            self.metadata_store.append(metadata)
            self.chunk_store.append(chunk)
            chunk_ids.append(chunk_id)
        
        print(f"Added {len(chunks)} chunks to vector store")
        return chunk_ids
    
    def search(self, 
               query: str, 
               top_k: int = 5, 
               threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            top_k: Number of top results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of search results with chunks and scores
        """
        if not self.is_initialized or len(self.metadata_store) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_manager.generate_embeddings(query)
        
        # Normalize query embedding
        faiss.normalize_L2(query_embedding.reshape(1, -1))
        
        # Search in FAISS index
        scores, indices = self.index.search(query_embedding, min(top_k, len(self.metadata_store)))
        
        # Format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or score < threshold:  # FAISS returns -1 for invalid indices
                continue
            
            if idx < len(self.chunk_store):
                chunk = self.chunk_store[idx]
                metadata = self.metadata_store[idx]
                
                result = {
                    "chunk_id": idx,
                    "score": float(score),
                    "content": chunk.content,
                    "metadata": metadata,
                    "chunk_metadata": chunk.metadata
                }
                results.append(result)
        
        return results
    
    def search_by_embedding(self, 
                           query_embedding: np.ndarray, 
                           top_k: int = 5, 
                           threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Search using a pre-computed embedding
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of search results
        """
        if not self.is_initialized or len(self.metadata_store) == 0:
            return []
        
        # Normalize query embedding
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search in FAISS index
        scores, indices = self.index.search(query_embedding, min(top_k, len(self.metadata_store)))
        
        # Format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or score < threshold:
                continue
            
            if idx < len(self.chunk_store):
                chunk = self.chunk_store[idx]
                metadata = self.metadata_store[idx]
                
                result = {
                    "chunk_id": idx,
                    "score": float(score),
                    "content": chunk.content,
                    "metadata": metadata,
                    "chunk_metadata": chunk.metadata
                }
                results.append(result)
        
        return results
    
    def get_chunk_by_id(self, chunk_id: int) -> Optional[DocumentChunk]:
        """Get a specific chunk by ID"""
        if 0 <= chunk_id < len(self.chunk_store):
            return self.chunk_store[chunk_id]
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            "total_chunks": len(self.chunk_store),
            "index_size": self.index.ntotal if self.index else 0,
            "embedding_dimension": self.embedding_manager.get_embedding_dimension(),
            "is_initialized": self.is_initialized,
            "index_path": str(self.index_path),
            "index_name": self.index_name
        }
    
    def save(self):
        """Save the vector store to disk"""
        if not self.is_initialized:
            return
        
        index_file = self.index_path / f"{self.index_name}.faiss"
        metadata_file = self.index_path / f"{self.index_name}_metadata.pkl"
        chunks_file = self.index_path / f"{self.index_name}_chunks.pkl"
        
        try:
            # Save FAISS index
            faiss.write_index(self.index, str(index_file))
            
            # Save metadata
            with open(metadata_file, 'wb') as f:
                pickle.dump(self.metadata_store, f)
            
            # Save chunks
            with open(chunks_file, 'wb') as f:
                pickle.dump(self.chunk_store, f)
            
            print(f"Vector store saved to {self.index_path}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to save vector store: {str(e)}")
    
    def clear(self):
        """Clear all data from the vector store"""
        self._create_new_index()
        print("Vector store cleared")
    
    def delete_by_filename(self, filename: str) -> int:
        """
        Delete all chunks from a specific file
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            Number of chunks deleted
        """
        if not self.is_initialized:
            return 0
        
        # Find chunks to delete
        indices_to_delete = []
        for i, metadata in enumerate(self.metadata_store):
            if metadata.get("filename") == filename:
                indices_to_delete.append(i)
        
        if not indices_to_delete:
            return 0
        
        # Remove from FAISS index (this is complex, so we'll rebuild)
        self._rebuild_index_excluding(indices_to_delete)
        
        print(f"Deleted {len(indices_to_delete)} chunks for file: {filename}")
        return len(indices_to_delete)
    
    def _rebuild_index_excluding(self, indices_to_exclude: List[int]):
        """Rebuild index excluding specific indices"""
        # Keep only the chunks we want
        new_chunks = []
        new_metadata = []
        
        for i in range(len(self.chunk_store)):
            if i not in indices_to_exclude:
                new_chunks.append(self.chunk_store[i])
                new_metadata.append(self.metadata_store[i])
        
        # Rebuild index
        self.chunk_store = new_chunks
        self.metadata_store = new_metadata
        
        if new_chunks:
            # Generate embeddings for remaining chunks
            embeddings = self.embedding_manager.generate_embeddings_for_chunks(new_chunks)
            faiss.normalize_L2(embeddings)
            
            # Create new index
            dimension = self.embedding_manager.get_embedding_dimension()
            self.index = faiss.IndexFlatIP(dimension)
            self.index.add(embeddings)
        else:
            # Create empty index
            dimension = self.embedding_manager.get_embedding_dimension()
            self.index = faiss.IndexFlatIP(dimension) 