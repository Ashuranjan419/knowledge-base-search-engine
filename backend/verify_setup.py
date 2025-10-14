#!/usr/bin/env python3
"""
Setup Verification Script for Knowledge Base Search Engine
This script checks if all components are properly installed and configured.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check Python version."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print(" Python version is compatible (3.8+)")
        return True
    else:
        print(" Python version too old. Requires 3.8 or higher")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print_header("Checking Dependencies")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'sentence_transformers',
        'faiss',
        'openai',
        'PyPDF2',
        'pdfplumber',
        'python_multipart',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'faiss':
                __import__('faiss')
            elif package == 'python_multipart':
                __import__('multipart')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT FOUND")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n All dependencies are installed")
        return True

def check_project_structure():
    """Check if project structure is correct."""
    print_header("Checking Project Structure")
    
    project_root = Path(__file__).parent.parent
    
    required_files = [
        'backend/main.py',
        'backend/rag.py',
        'backend/document_utils.py',
        'backend/config.py',
        'backend/requirements.txt',
        'frontend/index.html',
        '.env.example',
        'README.md'
    ]
    
    required_dirs = [
        'backend',
        'frontend',
        'sample_documents'
    ]
    
    all_good = True
    
    # Check directories
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f" {dir_name}/")
        else:
            print(f" {dir_name}/ - NOT FOUND")
            all_good = False
    
    # Check files
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"{file_name}")
        else:
            print(f"{file_name} - NOT FOUND")
            all_good = False
    
    if all_good:
        print("\n Project structure is correct")
    else:
        print("\n  Some files or directories are missing")
    
    return all_good

def check_env_file():
    """Check if .env file exists and has required variables."""
    print_header("Checking Environment Configuration")
    
    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env'
    env_example = project_root / '.env.example'
    
    if not env_example.exists():
        print(" .env.example not found")
        return False
    
    print(" .env.example exists")
    
    if not env_file.exists():
        print("  .env file not found")
        print("   Create it by copying .env.example and adding your API key")
        print(f"   Run: cp {env_example} {env_file}")
        return False
    
    print(" .env file exists")
    
    # Check for OpenAI API key
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content:
                if 'your_openai_api_key_here' in content or 'sk-' not in content:
                    print("  OPENAI_API_KEY not configured (still has placeholder)")
                    print("   Edit .env and add your actual OpenAI API key")
                    return False
                else:
                    print(" OPENAI_API_KEY is configured")
                    return True
            else:
                print("  OPENAI_API_KEY not found in .env")
                return False
    except Exception as e:
        print(f" Error reading .env file: {e}")
        return False

def check_sample_documents():
    """Check if sample documents exist."""
    print_header("Checking Sample Documents")
    
    project_root = Path(__file__).parent.parent
    sample_dir = project_root / 'sample_documents'
    
    if not sample_dir.exists():
        print("  sample_documents directory not found")
        return False
    
    files = list(sample_dir.glob('*.*'))
    
    if not files:
        print("  No sample documents found")
        print("   Sample documents help with testing")
        return False
    
    print(f" Found {len(files)} sample document(s):")
    for f in files:
        print(f"   - {f.name}")
    
    return True

def check_ports():
    """Check if required ports are available."""
    print_header("Checking Port Availability")
    
    import socket
    
    ports_to_check = [
        (8000, "Backend API"),
        (8080, "Frontend server (optional)")
    ]
    
    all_available = True
    
    for port, description in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"  Port {port} ({description}) is in use")
            all_available = False
        else:
            print(f" Port {port} ({description}) is available")
    
    return all_available

def run_import_test():
    """Test if key imports work."""
    print_header("Testing Key Imports")
    
    try:
        print("Testing FastAPI import...")
        from fastapi import FastAPI
        print("FastAPI")
        
        print("Testing Sentence Transformers...")
        from sentence_transformers import SentenceTransformer
        print(" Sentence Transformers")
        
        print("Testing FAISS...")
        import faiss
        print(" FAISS")
        
        print("Testing OpenAI...")
        import openai
        print(" OpenAI")
        
        print("Testing PDF libraries...")
        import PyPDF2
        import pdfplumber
        print(" PDF libraries")
        
        print("\n All imports successful")
        return True
        
    except Exception as e:
        print(f"\n Import failed: {e}")
        return False

def main():
    """Run all checks."""
    print("\n" + "="*60)
    print("  KNOWLEDGE BASE SEARCH ENGINE - SETUP VERIFICATION")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Environment Configuration", check_env_file),
        ("Sample Documents", check_sample_documents),
        ("Port Availability", check_ports),
        ("Import Test", run_import_test),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n Error during {check_name}: {e}")
            results.append((check_name, False))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = " PASS" if result else "  FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n All checks passed! You're ready to start the server.")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && python main.py")
        print("2. Open frontend: Open frontend/index.html in browser")
        print("3. Upload sample documents and test queries")
    else:
        print("\n Some checks failed. Please review the issues above.")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r backend/requirements.txt")
        print("- Create .env file: cp .env.example .env")
        print("- Add your OpenAI API key to .env")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nVerification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
