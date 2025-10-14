#!/bin/bash

# Knowledge Base Search Engine - Startup Script

echo "🚀 Starting Knowledge Base Search Engine..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
cd backend
pip install -r requirements.txt

# Check if .env exists
if [ ! -f "../.env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp ../.env.example ../.env
    echo "Please edit .env file with your API keys before running."
    exit 1
fi

# Start the server
echo "Starting FastAPI server..."
python main.py
