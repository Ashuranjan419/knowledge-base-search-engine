import PyPDF2
import pdfplumber
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class DocumentParser:
    """
    Parser for text and PDF documents.
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt']
    
    def parse_document(self, file_path: str) -> str:
        """
        Parse a document and extract text content.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = path.suffix.lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        if file_extension == '.pdf':
            return self._parse_pdf(file_path)
        elif file_extension == '.txt':
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _parse_pdf(self, file_path: str) -> str:
        """
        Parse PDF file and extract text.
        Uses pdfplumber as primary method, falls back to PyPDF2 if needed.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        text_content = ""
        
        try:
            # Try pdfplumber first (better for complex PDFs)
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num} ---\n"
                        text_content += page_text + "\n"
            
            if text_content.strip():
                logger.info(f"Successfully parsed PDF with pdfplumber: {file_path}")
                return text_content.strip()
            
            # Fallback to PyPDF2
            logger.info(f"pdfplumber returned empty, trying PyPDF2: {file_path}")
            text_content = self._parse_pdf_pypdf2(file_path)
            
        except Exception as e:
            logger.warning(f"pdfplumber failed: {e}. Trying PyPDF2...")
            text_content = self._parse_pdf_pypdf2(file_path)
        
        if not text_content.strip():
            raise ValueError(f"Could not extract text from PDF: {file_path}")
        
        return text_content.strip()
    
    def _parse_pdf_pypdf2(self, file_path: str) -> str:
        """
        Parse PDF using PyPDF2 (fallback method).
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        text_content = ""
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num} ---\n"
                        text_content += page_text + "\n"
            
            logger.info(f"Successfully parsed PDF with PyPDF2: {file_path}")
            
        except Exception as e:
            logger.error(f"PyPDF2 parsing failed: {e}")
            raise ValueError(f"Failed to parse PDF with PyPDF2: {e}")
        
        return text_content.strip()
    
    def _parse_txt(self, file_path: str) -> str:
        """
        Parse text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Text content
        """
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            logger.info(f"Successfully parsed TXT file: {file_path}")
            return content.strip()
            
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding
            logger.warning(f"UTF-8 failed, trying latin-1 for: {file_path}")
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
            
            logger.info(f"Successfully parsed TXT file with latin-1: {file_path}")
            return content.strip()
        
        except Exception as e:
            logger.error(f"Failed to parse TXT file: {e}")
            raise ValueError(f"Failed to parse text file: {e}")
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text content to chunk
            chunk_size: Target size of each chunk (in characters)
            overlap: Number of overlapping characters between chunks
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        max_iterations = 10000  # Safety limit to prevent infinite loops
        iteration_count = 0
        
        while start < text_length and iteration_count < max_iterations:
            iteration_count += 1
            end = start + chunk_size
            
            # Try to break at sentence or word boundary
            if end < text_length:
                # Look for sentence end
                for delimiter in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
                    boundary = text.rfind(delimiter, start, end)
                    if boundary != -1:
                        end = boundary + len(delimiter)
                        break
                else:
                    # Look for word boundary
                    boundary = text.rfind(' ', start, end)
                    if boundary != -1:
                        end = boundary + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            # Ensure we always make progress
            if end <= start:
                # Prevent infinite loop if we're not moving forward
                start += max(1, chunk_size)
            else:
                start = end - overlap if end < text_length else text_length
        
        if iteration_count >= max_iterations:
            logger.warning(f"Chunking hit iteration limit. Processed {len(chunks)} chunks.")
        
        logger.info(f"Text chunked into {len(chunks)} chunks")
        return chunks
