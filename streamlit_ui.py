#!/usr/bin/env python3
"""
Streamlit User Interface for RAG API Testing
"""

import streamlit as st
import requests
import json
import base64
import pandas as pd
from datetime import datetime
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="RAG API Testing Interface",
    page_icon="🤖",
    layout="wide"
)

def check_api_health():
    """Check API health"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def upload_file(file):
    """Upload file to API"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def ask_question(question, image_base64=None):
    """Ask question to API"""
    try:
        payload = {"question": question}
        if image_base64:
            payload["image_base64"] = image_base64
        
        response = requests.post(f"{API_BASE_URL}/query", json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_stats():
    """Get system stats"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def main():
    st.title("🤖 RAG API Testing Interface")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Dashboard", "File Upload", "Question & Answer", "System Monitoring"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "File Upload":
        show_file_upload()
    elif page == "Question & Answer":
        show_qa()
    elif page == "System Monitoring":
        show_monitoring()

def show_dashboard():
    st.header("📊 Dashboard")
    
    # Check API health
    health = check_api_health()
    
    if health:
        st.success("✅ API is running!")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Chunks", health["document_service"]["total_chunks"])
        
        with col2:
            st.metric("Index Size", health["document_service"]["index_size"])
        
        with col3:
            st.metric("Embedding Dimension", health["document_service"]["embedding_dimension"])
        
        with col4:
            llm_status = "✅ Available" if health["llm_available"] else "⚠️ Not Available"
            st.metric("LLM Service", llm_status)
        
        # Show supported file types
        st.subheader("📁 Supported File Types")
        extensions = health["document_service"]["supported_extensions"]
        st.write(", ".join(extensions))
        
    else:
        st.error("❌ API is not responding")
        st.info("Make sure the API is running on http://localhost:8000")

def show_file_upload():
    st.header("📁 File Upload")
    
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['pdf', 'docx', 'txt', 'csv', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'md', 'json', 'xml', 'html', 'htm', 'log', 'rst', 'tsv'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} file(s):")
        for file in uploaded_files:
            st.write(f"• {file.name} ({file.size} bytes)")
        
        if st.button("🚀 Upload Files"):
            progress_bar = st.progress(0)
            
            for i, file in enumerate(uploaded_files):
                result = upload_file(file)
                if result:
                    st.success(f"✅ {file.name}: Uploaded successfully")
                    st.write(f"   - Chunks: {result.get('chunks_created', 'N/A')}")
                    st.write(f"   - Processing time: {result.get('processing_time', 'N/A')}s")
                else:
                    st.error(f"❌ {file.name}: Upload failed")
                
                progress_bar.progress((i + 1) / len(uploaded_files))

def show_qa():
    st.header("❓ Question & Answer")
    
    # Check LLM availability
    health = check_api_health()
    if not health or not health["llm_available"]:
        st.warning("⚠️ LLM service is not available. Set OPENAI_API_KEY to enable Q&A.")
        return
    
    # Question input
    question = st.text_area("Enter your question:", height=100)
    
    # Image upload (optional)
    uploaded_image = st.file_uploader(
        "Upload an image (optional)",
        type=['jpg', 'jpeg', 'png', 'gif', 'bmp']
    )
    
    image_base64 = None
    if uploaded_image:
        st.image(uploaded_image, width=300)
        image_bytes = uploaded_image.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    if st.button("🔍 Ask Question") and question:
        with st.spinner("Processing..."):
            result = ask_question(question, image_base64)
        
        if result:
            st.subheader("💡 Answer")
            st.write(result.get('answer', 'No answer provided'))
            
            if 'confidence' in result:
                st.write(f"**Confidence:** {result['confidence']:.2%}")
            
            if 'sources' in result and result['sources']:
                st.subheader("📚 Sources")
                for i, source in enumerate(result['sources'], 1):
                    with st.expander(f"Source {i}: {source.get('filename', 'Unknown')}"):
                        st.write(f"**Content:** {source.get('content', 'N/A')}")
                        st.write(f"**Similarity:** {source.get('similarity_score', 'N/A')}")
        else:
            st.error("❌ Failed to get answer")

def show_monitoring():
    st.header("📊 System Monitoring")
    
    if st.button("🔄 Refresh"):
        st.rerun()
    
    stats = get_stats()
    if stats:
        # System metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documents", stats.get("total_documents", 0))
        
        with col2:
            st.metric("Total Chunks", stats.get("total_chunks", 0))
        
        with col3:
            st.metric("Index Size", stats.get("index_size", 0))
        
        with col4:
            st.metric("Storage Used", f"{stats.get('storage_used_mb', 0):.1f} MB")
        
        # Document list
        if "documents" in stats and stats["documents"]:
            st.subheader("📋 Documents")
            docs_data = []
            for doc in stats["documents"]:
                docs_data.append({
                    "Filename": doc.get("filename", "N/A"),
                    "Type": doc.get("file_type", "N/A"),
                    "Size (KB)": f"{doc.get('file_size', 0) / 1024:.1f}",
                    "Chunks": doc.get("chunks", "N/A"),
                    "Upload Time": doc.get("upload_time", "N/A")
                })
            
            df = pd.DataFrame(docs_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No documents uploaded yet.")
    else:
        st.error("❌ Failed to get system stats")

if __name__ == "__main__":
    main() 