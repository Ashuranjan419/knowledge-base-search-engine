#!/bin/bash

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/Scripts/activate

# Navigate to backend
cd backend

# Start the server
echo "🚀 Starting Knowledge Base Search Engine..."
echo "📊 Server will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "⏳ Server starting (model will download on first document upload)..."
echo ""

python main.py
