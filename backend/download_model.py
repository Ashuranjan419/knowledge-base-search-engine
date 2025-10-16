"""
Quick test to download and verify the embedding model.
Run this ONCE before starting the server to cache the model.
"""
import sys
import logging
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_model():
    """Download and test the embedding model."""
    logger.info("=" * 50)
    logger.info("Downloading Embedding Model")
    logger.info("=" * 50)
    logger.info("Model: sentence-transformers/all-MiniLM-L6-v2")
    logger.info("Size: ~90MB")
    logger.info("This is a ONE-TIME download. Please wait...")
    logger.info("")
    
    try:
        # Download model with progress
        logger.info("Starting download...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        logger.info("✓ Model downloaded successfully!")
        logger.info("")
        
        # Test the model
        logger.info("Testing model...")
        test_text = ["This is a test sentence."]
        embeddings = model.encode(test_text, convert_to_numpy=True)
        
        logger.info(f"✓ Model test successful!")
        # Handle both 1D and 2D arrays
        if len(embeddings.shape) == 1:
            embedding_dim = embeddings.shape[0]
        else:
            embedding_dim = embeddings.shape[1]
        logger.info(f"  Embedding dimension: {embedding_dim}")
        logger.info("")
        logger.info("=" * 50)
        logger.info("SUCCESS! Model is ready to use.")
        logger.info("You can now start the server without delays.")
        logger.info("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
        logger.error("")
        logger.error("Troubleshooting:")
        logger.error("1. Check your internet connection")
        logger.error("2. Try running again")
        logger.error("3. If it still fails, the model may be downloading in background")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
