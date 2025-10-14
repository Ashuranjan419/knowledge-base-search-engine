"""
Test script for the Knowledge Base Search Engine API.
This script tests all major endpoints of the API.
"""

import requests
import json
import time
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
SAMPLE_DOCS_DIR = Path("../sample_documents")

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health_check():
    """Test the health check endpoint."""
    print_section("Testing Health Check")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print_section("Testing Root Endpoint")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_upload_documents():
    """Test document upload."""
    print_section("Testing Document Upload")
    
    # Check if sample documents exist
    if not SAMPLE_DOCS_DIR.exists():
        print(f"Sample documents directory not found: {SAMPLE_DOCS_DIR}")
        print("Please create sample documents first.")
        return False
    
    # Find all txt files
    txt_files = list(SAMPLE_DOCS_DIR.glob("*.txt"))
    
    if not txt_files:
        print("No .txt files found in sample_documents directory")
        return False
    
    try:
        files = []
        for file_path in txt_files:
            files.append(('files', (file_path.name, open(file_path, 'rb'), 'text/plain')))
        
        print(f"Uploading {len(files)} file(s)...")
        response = requests.post(f"{API_URL}/upload", files=files)
        
        # Close file handles
        for _, (_, file_obj, _) in files:
            file_obj.close()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_list_documents():
    """Test listing documents."""
    print_section("Testing List Documents")
    try:
        response = requests.get(f"{API_URL}/documents")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_query(query_text):
    """Test querying the knowledge base."""
    print_section(f"Testing Query: '{query_text}'")
    try:
        payload = {
            "query": query_text,
            "top_k": 3
        }
        response = requests.post(
            f"{API_URL}/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print(f"\nAnswer:\n{result['answer']}\n")
            print(f"Sources ({len(result['sources'])}):")
            for i, source in enumerate(result['sources'], 1):
                print(f"\n  {i}. {source['source']} (Chunk {source['chunk_id']})")
                print(f"     Score: {source['score']:.4f}")
                print(f"     Preview: {source['preview'][:100]}...")
        else:
            print(f"Error: {json.dumps(result, indent=2)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_multiple_queries():
    """Test multiple queries."""
    queries = [
        "What is machine learning?",
        "Explain supervised learning",
        "What are the types of machine learning?",
        "What is data science?",
        "What tools do data scientists use?",
        "Explain the data science process"
    ]
    
    results = []
    for query in queries:
        success = test_query(query)
        results.append((query, success))
        time.sleep(1)  # Small delay between queries
    
    # Summary
    print_section("Query Test Summary")
    for query, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {query}")
    
    return all(success for _, success in results)

def test_clear_knowledge_base():
    """Test clearing the knowledge base."""
    print_section("Testing Clear Knowledge Base")
    try:
        response = requests.delete(f"{API_URL}/clear")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("  KNOWLEDGE BASE SEARCH ENGINE - API TEST SUITE")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Upload Documents", test_upload_documents),
        ("List Documents", test_list_documents),
        ("Multiple Queries", test_multiple_queries),
        # ("Clear Knowledge Base", test_clear_knowledge_base),  # Uncomment to test clearing
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
        time.sleep(1)
    
    # Final Summary
    print("\n" + "="*60)
    print("  FINAL TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    print("\nMake sure the backend server is running on http://localhost:8000")
    input("Press Enter to start tests...")
    
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)
