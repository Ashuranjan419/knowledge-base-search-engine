from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import shutil
from pathlib import Path
import logging

from rag import RAGSystem
from document_utils import DocumentParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Knowledge Base Search Engine", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system (lazy loading)
rag_system = None
document_parser = DocumentParser()

def get_rag_system():
    """Lazy initialize RAG system."""
    global rag_system
    if rag_system is None:
        rag_system = RAGSystem()
    return rag_system

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    query: str

@app.get("/")
async def root():
    return {
        "message": "Knowledge Base Search Engine API",
        "version": "1.0.0",
        "endpoints": {
            "/upload": "POST - Upload documents (PDF/TXT)",
            "/query": "POST - Query the knowledge base",
            "/documents": "GET - List indexed documents",
            "/clear": "DELETE - Clear all documents"
        }
    }

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload one or more documents (PDF or TXT) to the knowledge base.
    """
    uploaded_files = []
    
    try:
        for file in files:
            # Validate file type
            if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file.filename}. Only PDF and TXT files are allowed."
                )
            
            # Save file
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"Saved file: {file_path}")
            
            # Parse document
            try:
                text_content = document_parser.parse_document(str(file_path))
                
                # Add to RAG system (lazy init)
                rag = get_rag_system()
                rag.add_document(text_content, file.filename)
                
                uploaded_files.append({
                    "filename": file.filename,
                    "status": "success",
                    "chunks": len(text_content.split('\n\n'))
                })
                
                logger.info(f"Successfully processed: {file.filename}")
                
            except Exception as e:
                import traceback
                error_msg = str(e) if str(e) else "Unknown error"
                logger.error(f"Error processing {file.filename}: {error_msg}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                uploaded_files.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": error_msg
                })
        
        return {
            "message": f"Processed {len(files)} file(s)",
            "files": uploaded_files,
            "total_documents": get_rag_system().get_document_count()
        }
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """
    Query the knowledge base and get a synthesized answer.
    """
    try:
        rag = get_rag_system()
        if rag.get_document_count() == 0:
            raise HTTPException(
                status_code=400,
                detail="No documents in knowledge base. Please upload documents first."
            )
        
        logger.info(f"Processing query: {request.query}")
        
        # Get answer from RAG system
        result = rag.query(request.query, top_k=request.top_k)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            query=request.query
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """
    List all documents in the knowledge base.
    """
    try:
        rag = get_rag_system()
        documents = rag.list_documents()
        return {
            "total_documents": len(documents),
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
async def clear_knowledge_base():
    """
    Clear all documents from the knowledge base.
    """
    try:
        # Clear RAG system
        rag = get_rag_system()
        rag.clear()
        
        # Remove uploaded files
        for file in UPLOAD_DIR.iterdir():
            if file.is_file():
                file.unlink()
        
        return {
            "message": "Knowledge base cleared successfully",
            "documents_remaining": 0
        }
    except Exception as e:
        logger.error(f"Error clearing knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    # Don't initialize RAG for health check - just check if it exists
    doc_count = rag_system.get_document_count() if rag_system else 0
    return {
        "status": "healthy",
        "documents_indexed": doc_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
