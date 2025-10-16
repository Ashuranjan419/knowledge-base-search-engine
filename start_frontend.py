"""
Simple HTTP server to serve the frontend.
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Change to frontend directory
frontend_dir = Path(__file__).parent / "frontend"
os.chdir(frontend_dir)

PORT = 3000

Handler = http.server.SimpleHTTPRequestHandler

print("=" * 60)
print("Knowledge Base Search Engine - Frontend Server")
print("=" * 60)
print(f"Frontend URL: http://localhost:{PORT}")
print(f"Backend API: http://localhost:8000")
print(f"API Docs: http://localhost:8000/docs")
print("=" * 60)
print()
print("Opening browser...")
print("Press CTRL+C to stop")
print()

# Open browser
webbrowser.open(f"http://localhost:{PORT}")

# Start server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[OK] Frontend server running on port {PORT}")
    httpd.serve_forever()
