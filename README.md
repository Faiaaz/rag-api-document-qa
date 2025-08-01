# RAG API - Document Q&A System

A smart Retrieval-Augmented Generation (RAG) API that can answer questions based on information extracted from various document types including PDFs, Word files, images (OCR), text files, and databases.

## ⚡ Quick Start (Docker)

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd rag-api
cp env.example .env

# 2. Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your_key_here" >> .env

# 3. Run with one command
chmod +x docker-run.sh
./docker-run.sh

# 4. Access the API
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

**That's it!** Your RAG API is now running and ready to process documents and answer questions! 🚀

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
│   │   ├── embedding_manager.py
│   │   └── faiss_store.py
│   ├── llm/                 # LLM integration
│   │   ├── __init__.py
│   │   ├── openai_client.py
│   │   ├── prompt_manager.py
│   │   └── rag_pipeline.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── data/                    # Document storage
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── startup.sh              # Startup script
├── docker-run.sh           # Docker run script
└── README.md               # This file
```

## 🐳 Docker Setup (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key (optional for basic functionality)

### Quick Docker Deployment

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-api
   ```

2. **Set up environment variables**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Edit .env file and add your OpenAI API key
   nano .env  # or use your preferred editor
   ```

3. **Run with Docker (One Command)**
   ```bash
   # Make script executable and run
   chmod +x docker-run.sh
   ./docker-run.sh
   ```

   This will:
   - Build the Docker image
   - Start the service with docker-compose
   - Check the health status
   - Display access URLs

4. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Manual Docker Commands

If you prefer manual control:

```bash
# Build the image
docker build -t rag-api .

# Run with docker-compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Docker Environment Variables

The following environment variables can be configured in your `.env` file:

```bash
# Required for LLM functionality
OPENAI_API_KEY=your_openai_api_key_here

# Optional configurations
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_STORE_PATH=./data/vector_store
UPLOAD_DIR=./data/uploads
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
DEBUG=False
```

## 🚀 Local Development Setup

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
   cp env.example .env
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

### Check System Status
```bash
curl http://localhost:8000/health
```

### Get System Statistics
```bash
curl http://localhost:8000/stats
```

## 🚀 GitHub Deployment

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/rag-api-document-qa.git
cd rag-api-document-qa
```

### 2. Set Up Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env with your OpenAI API key
nano .env
```

### 3. Deploy with Docker
```bash
# Make scripts executable
chmod +x docker-run.sh startup.sh

# Run the application
./docker-run.sh
```

### 4. Push to GitHub
```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "feat: Deploy RAG API with Docker"

# Push to your repository
git push origin main
```

### 5. Set Up GitHub Actions (Optional)
The repository includes GitHub Actions for CI/CD. To enable:

1. Go to your repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add the following secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password

## 🐳 Docker Features

### ✅ Complete Containerization
- **Multi-stage builds** for optimized images
- **Non-root user** for security
- **Health checks** for monitoring
- **Volume persistence** for data storage

### ✅ Easy Deployment
- **One-command setup** with `./docker-run.sh`
- **Environment management** with `.env` files
- **Docker Compose** for service orchestration
- **Automatic health monitoring**

### ✅ Production Ready
- **Graceful error handling** for missing API keys
- **Security best practices** implemented
- **Scalable architecture** for multiple instances
- **Comprehensive logging** and monitoring

## 🔧 Development Workflow

### Local Development
```bash
# Start with Docker
docker-compose up -d

# View logs
docker-compose logs -f

# Make changes and rebuild
docker-compose down
docker-compose up --build -d
```

### Testing
```bash
# Run tests in container
docker-compose exec rag-api python -m pytest

# Or run locally
python test_llm_components.py
```

### Debugging
```bash
# Access container shell
docker-compose exec rag-api bash

# View real-time logs
docker-compose logs -f rag-api
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
- **FAISS**: Vector similarity search and storage
- **OpenAI**: LLM for question answering
- **Sentence Transformers**: Text embeddings
- **PyMuPDF**: PDF processing
- **python-docx**: Word document processing
- **pytesseract**: OCR for image processing
- **pandas**: Data processing for CSV and databases
- **Docker**: Containerization and deployment
- **Docker Compose**: Service orchestration

## 🔧 Troubleshooting

### Common Issues

#### 1. OpenAI API Key Error
```bash
# Error: OpenAI API key is required
# Solution: Set your API key in .env file
echo "OPENAI_API_KEY=your_key_here" >> .env
```

#### 2. Docker Build Fails
```bash
# Error: Build context too large
# Solution: Check .dockerignore file is present
ls -la .dockerignore
```

#### 3. Port Already in Use
```bash
# Error: Port 8000 is already in use
# Solution: Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

#### 4. Permission Denied
```bash
# Error: Permission denied for scripts
# Solution: Make scripts executable
chmod +x docker-run.sh startup.sh
```

#### 5. Memory Issues
```bash
# Error: Out of memory during build
# Solution: Increase Docker memory limit
# In Docker Desktop: Settings → Resources → Memory
```

### Getting Help

1. **Check logs**: `docker-compose logs -f`
2. **Health check**: `curl http://localhost:8000/health`
3. **Container status**: `docker-compose ps`
4. **Rebuild**: `docker-compose down && docker-compose up --build -d`

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test with Docker: `./docker-run.sh`
5. Commit: `git commit -m "feat: Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the `/docs` endpoint when running
- **Examples**: See test files for usage examples 