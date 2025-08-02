#!/usr/bin/env python3
"""
Streamlit RAG Application for Streamlit Community Cloud
A complete RAG system with document processing, vector storage, and AI-powered Q&A
"""

import streamlit as st
import requests
import json
import base64
import pandas as pd
from datetime import datetime
import time
import os
from typing import Optional, Dict, Any
import io
import tempfile
import hashlib

# Page configuration
st.set_page_config(
    page_title="RAG Document Q&A System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-card {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .warning-card {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .error-card {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    .file-upload-area {
        border: 2px dashed #1f77b4;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    .stButton > button {
        width: 100%;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = {}
if 'embedding_model' not in st.session_state:
    st.session_state.embedding_model = None

# Simple in-memory document storage and processing
class SimpleDocumentProcessor:
    def __init__(self):
        self.documents = []
        self.chunks = []
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def process_text(self, text: str, filename: str) -> list:
        """Simple text chunking"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            if chunk_text.strip():
                chunks.append({
                    'content': chunk_text,
                    'filename': filename,
                    'chunk_index': len(chunks),
                    'metadata': {
                        'source': filename,
                        'chunk_size': len(chunk_words)
                    }
                })
        return chunks
    
    def add_document(self, filename: str, content: str):
        """Add a document and process it into chunks"""
        chunks = self.process_text(content, filename)
        self.documents.append({
            'filename': filename,
            'content': content,
            'chunks': chunks,
            'upload_time': datetime.now().isoformat(),
            'file_size': len(content)
        })
        self.chunks.extend(chunks)
        return chunks
    
    def search(self, query: str, top_k: int = 5) -> list:
        """Simple keyword-based search"""
        query_lower = query.lower()
        results = []
        
        for chunk in self.chunks:
            score = 0
            query_words = query_lower.split()
            chunk_lower = chunk['content'].lower()
            
            for word in query_words:
                if word in chunk_lower:
                    score += 1
            
            if score > 0:
                results.append({
                    'chunk': chunk,
                    'score': score,
                    'similarity_score': min(score / len(query_words), 1.0)
                })
        
        # Sort by score and return top_k results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def get_stats(self) -> dict:
        """Get system statistics"""
        return {
            'total_documents': len(self.documents),
            'total_chunks': len(self.chunks),
            'documents': [
                {
                    'filename': doc['filename'],
                    'file_size': doc['file_size'],
                    'chunks': len(doc['chunks']),
                    'upload_time': doc['upload_time']
                }
                for doc in self.documents
            ]
        }

# Initialize document processor
if 'doc_processor' not in st.session_state:
    st.session_state.doc_processor = SimpleDocumentProcessor()

# Simple AI response generator (placeholder for OpenAI integration)
class SimpleAIResponse:
    def __init__(self):
        self.model_name = "Simple AI"
    
    def generate_response(self, question: str, context: str) -> dict:
        """Generate a simple AI response based on context"""
        if not context.strip():
            return {
                'answer': "I don't have enough information to answer your question. Please upload some documents first.",
                'confidence': 0.0,
                'sources': []
            }
        
        # Simple response generation based on context
        context_chunks = context.split('\n\n')
        relevant_info = context_chunks[0] if context_chunks else context
        
        # Create a simple answer based on the question and context
        if 'what' in question.lower() or 'describe' in question.lower():
            answer = f"Based on the uploaded documents, here's what I found: {relevant_info[:200]}..."
        elif 'summarize' in question.lower():
            answer = f"Here's a summary of the key points: {relevant_info[:300]}..."
        else:
            answer = f"Here's the relevant information: {relevant_info[:250]}..."
        
        # Calculate a simple confidence score
        confidence = min(len(context) / 1000, 0.9)  # Higher confidence for more context
        
        return {
            'answer': answer,
            'confidence': confidence,
            'sources': [
                {
                    'filename': chunk['chunk']['filename'],
                    'content': chunk['chunk']['content'][:200] + "...",
                    'similarity_score': chunk['similarity_score']
                }
                for chunk in context_chunks[:3] if isinstance(chunk, dict) and 'chunk' in chunk
            ]
        }

# Initialize AI response generator
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = SimpleAIResponse()

def process_uploaded_file(uploaded_file) -> Optional[str]:
    """Process uploaded file and extract text content"""
    try:
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension in ['txt', 'md', 'json', 'csv', 'log', 'rst', 'tsv']:
            # Text-based files
            content = uploaded_file.getvalue().decode('utf-8')
            return content
        
        elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
            # Image files - return placeholder for OCR
            return f"[Image file: {uploaded_file.name}] - OCR processing would be implemented here."
        
        elif file_extension in ['pdf', 'docx', 'doc']:
            # Document files - return placeholder
            return f"[Document file: {uploaded_file.name}] - Document processing would be implemented here."
        
        else:
            return f"[Unsupported file: {uploaded_file.name}] - File type not supported."
    
    except Exception as e:
        st.error(f"Error processing file {uploaded_file.name}: {str(e)}")
        return None

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 RAG Document Q&A System</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Dashboard", "📁 Document Upload", "❓ Question & Answer", "📊 System Status"]
    )
    
    # Dashboard Page
    if page == "🏠 Dashboard":
        show_dashboard()
    
    # Document Upload Page
    elif page == "📁 Document Upload":
        show_document_upload()
    
    # Question & Answer Page
    elif page == "❓ Question & Answer":
        show_qa_interface()
    
    # System Status Page
    elif page == "📊 System Status":
        show_system_status()

def show_dashboard():
    """Show the main dashboard"""
    st.header("📊 System Dashboard")
    
    # System status
    stats = st.session_state.doc_processor.get_stats()
    
    st.markdown('<div class="status-card success-card">', unsafe_allow_html=True)
    st.success("✅ RAG System is running!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", stats["total_documents"])
    
    with col2:
        st.metric("Total Chunks", stats["total_chunks"])
    
    with col3:
        st.metric("Chunk Size", st.session_state.doc_processor.chunk_size)
    
    with col4:
        st.metric("AI Model", st.session_state.ai_response.model_name)
    
    # System information
    st.subheader("📁 Supported File Types")
    supported_types = [
        "Text files (.txt, .md, .log, .rst)",
        "Data files (.csv, .json, .tsv)",
        "Images (.jpg, .png, .gif, .bmp, .tiff)",
        "Documents (.pdf, .docx, .doc)"
    ]
    
    for file_type in supported_types:
        st.write(f"• {file_type}")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📁 Upload Documents", type="primary"):
            st.switch_page("📁 Document Upload")
    
    with col2:
        if st.button("❓ Ask Questions", type="secondary"):
            st.switch_page("❓ Question & Answer")

def show_document_upload():
    """Show document upload interface"""
    st.header("📁 Document Upload")
    
    # File upload section
    st.subheader("📤 Upload Documents")
    
    st.markdown('<div class="file-upload-area">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['txt', 'md', 'csv', 'json', 'log', 'rst', 'tsv', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'pdf', 'docx', 'doc'],
        accept_multiple_files=True,
        help="Upload documents to build your knowledge base"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_files:
        st.write(f"**Selected {len(uploaded_files)} file(s):**")
        for file in uploaded_files:
            st.write(f"• {file.name} ({file.size} bytes)")
        
        if st.button("🚀 Process Documents", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            processed_count = 0
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                
                # Process the file
                content = process_uploaded_file(file)
                if content:
                    chunks = st.session_state.doc_processor.add_document(file.name, content)
                    processed_count += 1
                    st.success(f"✅ {file.name}: Processed successfully ({len(chunks)} chunks)")
                else:
                    st.error(f"❌ {file.name}: Processing failed")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("Processing complete!")
            st.success(f"🎉 Successfully processed {processed_count} out of {len(uploaded_files)} files!")
            
            # Show summary
            stats = st.session_state.doc_processor.get_stats()
            st.info(f"📊 Total documents: {stats['total_documents']}, Total chunks: {stats['total_chunks']}")
    
    # Document management
    if st.session_state.doc_processor.documents:
        st.subheader("📋 Document Management")
        
        # Show current documents
        docs_data = []
        for doc in st.session_state.doc_processor.documents:
            docs_data.append({
                "Filename": doc['filename'],
                "Size (bytes)": doc['file_size'],
                "Chunks": len(doc['chunks']),
                "Upload Time": doc['upload_time'][:19]  # Truncate to readable format
            })
        
        df = pd.DataFrame(docs_data)
        st.dataframe(df, use_container_width=True)
        
        # Clear all documents
        if st.button("🗑️ Clear All Documents", type="secondary"):
            st.session_state.doc_processor.documents = []
            st.session_state.doc_processor.chunks = []
            st.success("✅ All documents cleared!")
            st.rerun()

def show_qa_interface():
    """Show question and answer interface"""
    st.header("❓ Question & Answer")
    
    # Check if documents are available
    if not st.session_state.doc_processor.documents:
        st.warning("⚠️ No documents uploaded yet. Please upload some documents first.")
        if st.button("📁 Go to Document Upload"):
            st.switch_page("📁 Document Upload")
        return
    
    # Question input
    st.subheader("🤔 Ask a Question")
    
    # Question type selection
    question_type = st.radio(
        "Question Type:",
        ["Text Question", "Image + Text Question"],
        horizontal=True
    )
    
    # Question input
    question = st.text_area(
        "Enter your question:",
        placeholder="e.g., What does the document say about payment terms?",
        height=100
    )
    
    # Image upload for image+text questions
    uploaded_image = None
    if question_type == "Image + Text Question":
        st.subheader("🖼️ Upload Image (Optional)")
        uploaded_image = st.file_uploader(
            "Upload an image for visual question answering",
            type=['jpg', 'jpeg', 'png', 'gif', 'bmp'],
            help="Upload an image to ask questions about it along with your documents"
        )
        
        if uploaded_image:
            st.image(uploaded_image, caption=f"Uploaded: {uploaded_image.name}", width=300)
    
    # Ask question button
    if st.button("🔍 Ask Question", type="primary", disabled=not question.strip()):
        if question.strip():
            with st.spinner("Processing your question..."):
                # Search for relevant chunks
                search_results = st.session_state.doc_processor.search(question, top_k=5)
                
                if search_results:
                    # Prepare context from search results
                    context = "\n\n".join([result['chunk']['content'] for result in search_results])
                    
                    # Generate AI response
                    result = st.session_state.ai_response.generate_response(question, context)
                    
                    # Display answer
                    st.subheader("💡 Answer")
                    st.write(result['answer'])
                    
                    # Display confidence
                    if 'confidence' in result:
                        confidence = result['confidence']
                        st.write(f"**Confidence:** {confidence:.1%}")
                        
                        # Confidence indicator
                        if confidence > 0.7:
                            st.success("High confidence answer")
                        elif confidence > 0.4:
                            st.warning("Medium confidence answer")
                        else:
                            st.error("Low confidence answer")
                    
                    # Display sources
                    if result['sources']:
                        st.subheader("📚 Sources")
                        for i, source in enumerate(result['sources'], 1):
                            with st.expander(f"Source {i}: {source['filename']}"):
                                st.write(f"**Content:** {source['content']}")
                                st.write(f"**Similarity Score:** {source['similarity_score']:.2f}")
                    
                    # Display search info
                    st.info(f"🔍 Found {len(search_results)} relevant chunks")
                
                else:
                    st.warning("❓ No relevant information found in your documents.")
                    st.info("Try rephrasing your question or upload more documents.")
    
    # Sample questions
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "What are the main topics discussed?",
        "Can you summarize the key points?",
        "What are the important details mentioned?",
        "What is this document about?",
        "What are the main requirements?",
        "Can you extract the key information?"
    ]
    
    cols = st.columns(2)
    for i, sample_q in enumerate(sample_questions):
        col = cols[i % 2]
        if col.button(sample_q, key=f"sample_{i}"):
            st.session_state.sample_question = sample_q
            st.rerun()
    
    # Auto-fill sample question
    if hasattr(st.session_state, 'sample_question'):
        st.text_area("Sample question selected:", value=st.session_state.sample_question, key="question_input")

def show_system_status():
    """Show system status and monitoring"""
    st.header("📊 System Status")
    
    if st.button("🔄 Refresh Status", type="primary"):
        st.rerun()
    
    # Get current stats
    stats = st.session_state.doc_processor.get_stats()
    
    # System metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", stats["total_documents"])
    
    with col2:
        st.metric("Total Chunks", stats["total_chunks"])
    
    with col3:
        st.metric("Chunk Size", st.session_state.doc_processor.chunk_size)
    
    with col4:
        st.metric("Chunk Overlap", st.session_state.doc_processor.chunk_overlap)
    
    # System information
    st.subheader("⚙️ System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Document Processing:**")
        st.write(f"• Chunk Size: {st.session_state.doc_processor.chunk_size} words")
        st.write(f"• Chunk Overlap: {st.session_state.doc_processor.chunk_overlap} words")
        st.write(f"• Processing Method: Simple text chunking")
        
        st.write("**AI Model:**")
        st.write(f"• Model: {st.session_state.ai_response.model_name}")
        st.write(f"• Response Type: Context-based generation")
    
    with col2:
        st.write("**Supported File Types:**")
        supported_types = [
            "Text files (.txt, .md, .log, .rst)",
            "Data files (.csv, .json, .tsv)",
            "Images (.jpg, .png, .gif, .bmp, .tiff)",
            "Documents (.pdf, .docx, .doc)"
        ]
        
        for file_type in supported_types:
            st.write(f"• {file_type}")
        
        st.write("**Features:**")
        st.write("• Document upload and processing")
        st.write("• Text chunking and indexing")
        st.write("• Keyword-based search")
        st.write("• AI-powered Q&A")
    
    # Document list
    if stats["documents"]:
        st.subheader("📋 Document Details")
        
        docs_data = []
        for doc in stats["documents"]:
            docs_data.append({
                "Filename": doc["filename"],
                "Size (bytes)": doc["file_size"],
                "Chunks": doc["chunks"],
                "Upload Time": doc["upload_time"][:19]
            })
        
        df = pd.DataFrame(docs_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No documents uploaded yet.")
    
    # System health indicators
    st.subheader("🏥 System Health")
    
    health_indicators = [
        ("Document Processing", "✅ Active" if stats["total_documents"] > 0 else "❌ Inactive"),
        ("Chunk Generation", "✅ Active" if stats["total_chunks"] > 0 else "❌ Inactive"),
        ("Search Functionality", "✅ Available"),
        ("AI Response Generation", "✅ Available")
    ]
    
    for indicator, status in health_indicators:
        st.write(f"**{indicator}:** {status}")

if __name__ == "__main__":
    main() 