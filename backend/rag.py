import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import logging
from pathlib import Path
import json
from dotenv import load_dotenv
import openai
from huggingface_hub import InferenceClient

from document_utils import DocumentParser

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class RAGSystem:
    """
    Retrieval-Augmented Generation (RAG) system for knowledge base search.
    Uses FAISS for vector similarity search and LLM for answer synthesis.
    """
    
    def __init__(
        self,
        embedding_model: str = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        """
        Initialize RAG system.
        
        Args:
            embedding_model: Name of the sentence transformer model
            chunk_size: Size of text chunks for embedding
            chunk_overlap: Overlap between consecutive chunks
        """
        # Configuration
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model or os.getenv(
            "EMBEDDING_MODEL", 
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize components
        logger.info(f"Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # FAISS index
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Document storage
        self.documents = []  # List of dicts: {text, source, chunk_id}
        self.document_parser = DocumentParser()
        
        # LLM configuration
        self.llm_provider = os.getenv("LLM_PROVIDER", "huggingface").lower()
        self.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        
        # Initialize LLM clients
        if self.llm_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                logger.info("OpenAI API configured")
            else:
                logger.warning("OPENAI_API_KEY not set. Will use fallback method.")
        
        elif self.llm_provider == "huggingface":
            hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
            hf_model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
            
            if hf_api_key:
                self.hf_client = InferenceClient(token=hf_api_key)
                self.hf_model = hf_model
                logger.info(f"HuggingFace API configured with model: {hf_model}")
            else:
                logger.warning("HUGGINGFACE_API_KEY not set. Will use fallback method.")
                self.hf_client = None
        
        logger.info(f"RAG System initialized with LLM provider: {self.llm_provider}")
    
    def add_document(self, text: str, source: str):
        """
        Add a document to the knowledge base.
        
        Args:
            text: Document text content
            source: Source identifier (e.g., filename)
        """
        import time
        start_time = time.time()
        logger.info(f"Adding document: {source}")
        
        # Chunk the document
        chunk_start = time.time()
        chunks = self.document_parser.chunk_text(
            text, 
            chunk_size=self.chunk_size, 
            overlap=self.chunk_overlap
        )
        logger.info(f"Chunking took {time.time() - chunk_start:.2f} seconds")
        
        if not chunks:
            logger.warning(f"No chunks created from document: {source}")
            return
        
        logger.info(f"Created {len(chunks)} chunks, now generating embeddings...")
        
        # Generate embeddings
        embed_start = time.time()
        try:
            embeddings = self.embedding_model.encode(
                chunks, 
                show_progress_bar=True,  # Show progress to see if it's stuck
                convert_to_numpy=True,
                batch_size=32  # Process in batches
            )
            logger.info(f"Embedding generation took {time.time() - embed_start:.2f} seconds")
            logger.info(f"Successfully generated {len(embeddings)} embeddings with shape {embeddings.shape}")
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
        
        # Add to FAISS index
        faiss_start = time.time()
        try:
            # Ensure embeddings are 2D array
            if len(embeddings.shape) == 1:
                embeddings = embeddings.reshape(1, -1)
            
            embeddings_array = np.array(embeddings).astype('float32')
            logger.info(f"Adding {embeddings_array.shape} embeddings to FAISS index")
            self.index.add(embeddings_array)
            logger.info(f"FAISS indexing took {time.time() - faiss_start:.2f} seconds")
        except Exception as e:
            logger.error(f"Error adding to FAISS index: {str(e)}")
            raise
        
        # Store document metadata
        for i, chunk in enumerate(chunks):
            self.documents.append({
                "text": chunk,
                "source": source,
                "chunk_id": i
            })
        
        total_time = time.time() - start_time
        logger.info(f"Successfully added {len(chunks)} chunks from {source} in {total_time:.2f} seconds")
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve most relevant documents for a query.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant documents with metadata
        """
        if len(self.documents) == 0:
            logger.warning("No documents in knowledge base")
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        
        # Ensure query_embedding is 2D for FAISS search
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        elif query_embedding.shape[0] > 1:
            # If multiple embeddings returned, take the first one
            query_embedding = query_embedding[0:1]
        
        # Search in FAISS index
        distances, indices = self.index.search(
            query_embedding.astype('float32'),
            min(top_k, len(self.documents))
        )
        
        # Retrieve documents
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['score'] = float(distances[0][i])
                results.append(doc)
        
        logger.info(f"Retrieved {len(results)} documents for query: {query}")
        return results
    
    def synthesize_answer(self, query: str, context_docs: List[Dict]) -> str:
        """
        Synthesize an answer using LLM based on retrieved documents.
        
        Args:
            query: User query
            context_docs: Retrieved relevant documents
            
        Returns:
            Synthesized answer
        """
        if not context_docs:
            return "I couldn't find any relevant information in the knowledge base to answer your question."
        
        # Build context from retrieved documents
        context = "\n\n".join([
            f"[Source: {doc['source']}, Chunk {doc['chunk_id']}]\n{doc['text']}"
            for doc in context_docs
        ])
        
        # Create prompt
        prompt = f"""Using the following documents from the knowledge base, answer the user's question succinctly and accurately.

Context from documents:
{context}

User's question: {query}

Instructions:
- Provide a clear, concise answer based on the context
- If the context doesn't contain enough information, say so
- Cite sources when possible (e.g., "According to [source]...")
- Be factual and don't make up information

Answer:"""
        
        try:
            if self.llm_provider == "openai":
                response = openai.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that answers questions based on provided documents. Be concise and accurate."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                answer = response.choices[0].message.content.strip()
                logger.info("Successfully generated answer with OpenAI")
                return answer
            
            elif self.llm_provider == "huggingface":
                if not hasattr(self, 'hf_client') or self.hf_client is None:
                    logger.warning("HuggingFace client not configured. Using fallback method.")
                    return self._fallback_answer(query, context_docs)
                
                # Use HuggingFace Inference API
                response = self.hf_client.text_generation(
                    prompt,
                    model=self.hf_model,
                    max_new_tokens=500,
                    temperature=0.3,
                    return_full_text=False
                )
                
                answer = response.strip()
                logger.info("Successfully generated answer with HuggingFace")
                return answer
            
            else:
                # Fallback: simple extractive approach
                logger.warning("LLM provider not configured. Using fallback method.")
                return self._fallback_answer(query, context_docs)
        
        except Exception as e:
            logger.error(f"Error synthesizing answer: {e}")
            return self._fallback_answer(query, context_docs)
    
    def _fallback_answer(self, query: str, context_docs: List[Dict]) -> str:
        """
        Fallback answer generation without LLM (simple extraction).
        
        Args:
            query: User query
            context_docs: Retrieved documents
            
        Returns:
            Simple answer based on context
        """
        answer = "Based on the available documents:\n\n"
        
        for i, doc in enumerate(context_docs, 1):
            preview = doc['text'][:300] + "..." if len(doc['text']) > 300 else doc['text']
            answer += f"{i}. From {doc['source']}:\n{preview}\n\n"
        
        return answer
    
    def query(self, query: str, top_k: int = 3) -> Dict:
        """
        Full RAG pipeline: retrieve and synthesize answer.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            Dict with answer and sources
        """
        # Retrieve relevant documents
        relevant_docs = self.retrieve(query, top_k)
        
        # Synthesize answer
        answer = self.synthesize_answer(query, relevant_docs)
        
        # Prepare sources info
        sources = [
            {
                "source": doc['source'],
                "chunk_id": doc['chunk_id'],
                "score": doc['score'],
                "preview": doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text']
            }
            for doc in relevant_docs
        ]
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def get_document_count(self) -> int:
        """Get number of documents in knowledge base."""
        return len(self.documents)
    
    def list_documents(self) -> List[str]:
        """List all unique document sources."""
        sources = list(set(doc['source'] for doc in self.documents))
        return sources
    
    def clear(self):
        """Clear all documents from knowledge base."""
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.documents = []
        logger.info("Knowledge base cleared")
    
    def save_index(self, path: str = "faiss_index"):
        """
        Save FAISS index and metadata to disk.
        
        Args:
            path: Directory path to save index
        """
        path_obj = Path(path)
        path_obj.mkdir(exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(path_obj / "index.faiss"))
        
        # Save document metadata
        with open(path_obj / "documents.json", 'w') as f:
            json.dump(self.documents, f)
        
        logger.info(f"Index saved to {path}")
    
    def load_index(self, path: str = "faiss_index"):
        """
        Load FAISS index and metadata from disk.
        
        Args:
            path: Directory path to load index from
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            logger.warning(f"Index path does not exist: {path}")
            return
        
        # Load FAISS index
        self.index = faiss.read_index(str(path_obj / "index.faiss"))
        
        # Load document metadata
        with open(path_obj / "documents.json", 'r') as f:
            self.documents = json.load(f)
        
        logger.info(f"Index loaded from {path}")
