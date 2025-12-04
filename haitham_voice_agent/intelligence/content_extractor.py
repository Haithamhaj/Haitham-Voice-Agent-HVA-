import logging
from pathlib import Path
import PyPDF2
from typing import Optional

logger = logging.getLogger(__name__)

class ContentExtractor:
    """
    Extracts raw text from various file formats.
    Supported: .txt, .md, .py, .js, .json, .html, .css, .pdf
    """
    
    def __init__(self):
        pass
        
    def extract_text(self, path: str) -> Optional[str]:
        """Extract text content from file"""
        file_path = Path(path)
        if not file_path.exists():
            logger.warning(f"File not found: {path}")
            return None
            
        ext = file_path.suffix.lower()
        
        try:
            if ext == '.pdf':
                return self._extract_pdf(file_path)
            elif ext in ['.txt', '.md', '.py', '.js', '.json', '.html', '.css', '.csv', '.log']:
                return self._extract_text(file_path)
            else:
                logger.info(f"Unsupported file type for extraction: {ext}")
                return None
        except Exception as e:
            logger.error(f"Failed to extract content from {path}: {e}")
            return None
            
    def _extract_text(self, path: Path) -> str:
        """Read plain text files"""
        return path.read_text(encoding='utf-8', errors='ignore')
        
    def _extract_pdf(self, path: Path) -> str:
        """Extract text from PDF"""
        text = []
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)

# Singleton
content_extractor = ContentExtractor()
