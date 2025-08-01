# RAG API - Document Q&A System

A smart Retrieval-Augmented Generation (RAG) API that can answer questions based on information extracted from various document types including PDFs, Word files, images (OCR), text files, and databases.

## 🎯 What This System Does

1. **Document Ingestion**: Accepts various file types (.pdf, .docx, .txt, .jpg, .png, .csv, .db)
2. **Content Extraction**: Extracts text and processes images using OCR
3. **Vector Storage**: Stores document embeddings in FAISS for fast similarity search
4. **Question Answering**: Answers questions based on stored document content
5. **Multimodal Support**: Handles both text and image-based questions

## 🏗️ Project Structure

```
rag-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── document_processor/  # Document processing modules
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   ├── docx_processor.py
│   │   ├── image_processor.py
│   │   └── text_processor.py
│   ├── vector_store/        # Vector database operations
│   │   ├── __init__.py
│   │   └── faiss_store.py
│   ├── llm/                 # LLM integration
│   │   ├── __init__.py
│   │   └── openai_client.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── data/                    # Document storage
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Tesseract OCR (for image processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📚 API Usage

### Upload Documents
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"
```

### Ask Questions
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the payment terms mentioned?",
    "image_base64": null
  }'
```

## 🔧 Development Steps

We'll build this system in small, manageable steps:

1. **Step 1**: Basic FastAPI setup and project structure
2. **Step 2**: Document processing for different file types
3. **Step 3**: Vector storage with FAISS
4. **Step 4**: LLM integration for question answering
5. **Step 5**: API endpoints for upload and query
6. **Step 6**: OCR and image processing
7. **Step 7**: Advanced features and optimization

## 🛠️ Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **FAISS**: Vector similarity search
- **OpenAI**: LLM for question answering
- **PyMuPDF**: PDF processing
- **python-docx**: Word document processing
- **pytesseract**: OCR for image processing
- **pandas**: Data processing for CSV and databases

## 📝 License

MIT License 