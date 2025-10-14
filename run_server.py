#!/usr/bin/env python3
"""
Simple server starter for Knowledge Base Search Engine
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 50)
print(" 🚀 Knowledge Base Search Engine")
print("=" * 50)
print()
print("📊 Server: http://localhost:8000")
print("📚 API Docs: http://localhost:8000/docs")
print("🌐 Frontend: Open frontend/index.html")
print()
print("⏳ Starting server...")
print("💡 Tip: Model downloads on first document upload")
print()
print("Press CTRL+C to stop")
print("-" * 50)
print()

# Import and run
from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
