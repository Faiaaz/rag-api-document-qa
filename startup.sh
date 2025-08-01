#!/bin/bash

# Startup script for RAG API

echo "🚀 Starting RAG API..."

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY is not set!"
    echo "   The API will start but LLM functionality will be limited."
    echo "   Set OPENAI_API_KEY environment variable for full functionality."
fi

# Create necessary directories
mkdir -p data/uploads data/vector_store

# Set default values for environment variables
export OPENAI_MODEL=${OPENAI_MODEL:-gpt-3.5-turbo}
export EMBEDDING_MODEL=${EMBEDDING_MODEL:-all-MiniLM-L6-v2}
export VECTOR_STORE_PATH=${VECTOR_STORE_PATH:-./data/vector_store}
export UPLOAD_DIR=${UPLOAD_DIR:-./data/uploads}
export CHUNK_SIZE=${CHUNK_SIZE:-1000}
export CHUNK_OVERLAP=${CHUNK_OVERLAP:-200}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}
export DEBUG=${DEBUG:-False}

echo "📋 Configuration:"
echo "   OpenAI Model: $OPENAI_MODEL"
echo "   Embedding Model: $EMBEDDING_MODEL"
echo "   Vector Store: $VECTOR_STORE_PATH"
echo "   Upload Dir: $UPLOAD_DIR"
echo "   Chunk Size: $CHUNK_SIZE"
echo "   Chunk Overlap: $CHUNK_OVERLAP"
echo "   Host: $HOST"
echo "   Port: $PORT"
echo "   Debug: $DEBUG"

# Start the application
echo "🎯 Starting FastAPI application..."
exec uvicorn app.main:app --host $HOST --port $PORT --reload $([ "$DEBUG" = "True" ] && echo "--reload" || echo "") 