#!/bin/bash

# Docker build and run script for RAG API

set -e

echo "🐳 Building and running RAG API with Docker..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from env.example..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Created .env from env.example"
        echo "📝 Please edit .env file and add your OPENAI_API_KEY"
    else
        echo "❌ No env.example file found. Please create a .env file manually."
        exit 1
    fi
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t rag-api .

# Run with docker-compose
echo "🚀 Starting RAG API with docker-compose..."
docker-compose up -d

echo "✅ RAG API is starting up!"
echo "📊 Check status with: docker-compose ps"
echo "📝 View logs with: docker-compose logs -f"
echo "🌐 API will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"

# Wait a moment and check health
echo "⏳ Waiting for service to start..."
sleep 10

# Check health
echo "🏥 Checking service health..."
curl -f http://localhost:8000/health || echo "⚠️  Service not ready yet. Check logs with: docker-compose logs -f" 