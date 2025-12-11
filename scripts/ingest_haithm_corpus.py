#!/usr/bin/env python3
"""
Haithm Corpus Ingestion Script
==============================

Purpose:
    Walks through `haithm_corpus/` (or specified root) and ingests supported files into 
    a normalized JSONL dataset (`data/haithm_corpus_raw.jsonl`).

Supported Formats:
    - Text: .txt, .md
    - Documents: .pdf, .docx
    - Chats: .json (OpenAI export), .html (heuristic)
    - Audio: .m4a, .mp3, .wav (via OpenAI Whisper)
    - Images: .png, .jpg, .jpeg, .webp (via Tesseract OCR)

Usage:
    python scripts/ingest_haithm_corpus.py [--force] [--root <path>]
"""

import os
import json
import argparse
import hashlib
import logging
import uuid
import warnings
from pathlib import Path
from typing import List, Dict, Any, Optional

# --- Library Imports & Graceful Fallbacks ---

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Audio (Whisper)
try:
    import whisper
except ImportError:
    whisper = None

# OCR (Tesseract)
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Ingestor")

# Suppress some noisy warnings from libs
warnings.filterwarnings("ignore", category=UserWarning) 

class CorpusIngestor:
    def __init__(self, root_dir: str, output_file: str, max_chars: int, force: bool):
        self.root_dir = Path(root_dir)
        self.output_file = Path(output_file)
        self.max_chars = max_chars
        self.force = force
        self.stats = {
            "scanned": 0,
            "ingested": 0,
            "skipped": 0,
            "records": 0,
            "by_type": {},
            "by_role": {}
        }
        self.whisper_model = None  # Lazy load

    def run(self):
        # Checks
        if not self.root_dir.exists():
            logger.error(f"Root directory not found: {self.root_dir}")
            return

        if self.output_file.exists() and not self.force:
            logger.error(f"Output file exists: {self.output_file}")
            logger.info("Use --force to overwrite. Exiting.")
            return

        logger.info(f"Starting ingestion from: {self.root_dir}")
        all_records = []

        # Walk directory
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                file_path = Path(root) / file
                # Skip hidden files
                if file.startswith("."): 
                    continue
                
                self.stats["scanned"] += 1
                try:
                    records = self.process_file(file_path)
                    if records:
                        all_records.extend(records)
                        self.stats["ingested"] += 1
                    else:
                        self.stats["skipped"] += 1
                except Exception as e:
                    logger.error(f"CRITICAL ERROR processing {file}: {e}")
                    self.stats["skipped"] += 1

        # Write output
        if all_records:
            self._write_jsonl(all_records)
            self._print_summary()
        else:
            logger.warning("No records were generated. Is the directory empty?")

    def process_file(self, path: Path) -> List[Dict]:
        """Dispatch to appropriate handler based on extension."""
        ext = path.suffix.lower()
        
        try:
            if ext in [".txt", ".md"]:
                return self._handle_text(path)
            elif ext == ".pdf":
                if not PyPDF2:
                    logger.warning_once(f"Skipping PDF: PyPDF2 not installed")
                    return []
                return self._handle_pdf(path)
            elif ext == ".docx":
                if not docx:
                    logger.warning_once(f"Skipping DOCX: python-docx not installed")
                    return []
                return self._handle_docx(path)
            elif ext == ".json":
                return self._handle_json_chat(path)
            elif ext in [".html", ".htm"]:
                if not BeautifulSoup:
                    logger.warning_once(f"Skipping HTML: beautifulsoup4 not installed")
                    return []
                return self._handle_html_chat(path)
            elif ext in [".m4a", ".mp3", ".wav"]:
                if not whisper:
                    logger.warning_once(f"Skipping Audio: openai-whisper not installed")
                    return []
                return self._handle_audio(path)
            elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
                if not pytesseract or not Image:
                    logger.warning_once(f"Skipping Image: pytesseract/Pillow not installed")
                    return []
                return self._handle_image(path)
            else:
                # logger.debug(f"Skipping unsupported type: {path.name}")
                return []
        except Exception as e:
            logger.error(f"Error processing {path.name}: {e}")
            return []

    # --- Handlers ---

    def _handle_text(self, path: Path) -> List[Dict]:
        """Simple text ingestion."""
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        return self._create_chunks(text, path, source_type=path.suffix[1:], role="user")

    def _handle_pdf(self, path: Path) -> List[Dict]:
        """PDF ingestion."""
        text = ""
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n\n"
        except Exception as e:
            logger.warning(f"PDF read error {path.name}: {e}")
            return []
        
        return self._create_chunks(text, path, source_type="pdf", role="user")

    def _handle_docx(self, path: Path) -> List[Dict]:
        """DOCX ingestion."""
        try:
            doc = docx.Document(path)
            text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            return self._create_chunks(text, path, source_type="docx", role="user")
        except Exception as e:
            logger.warning(f"DOCX read error {path.name}: {e}")
            return []

    def _handle_json_chat(self, path: Path) -> List[Dict]:
        """
        Handle JSON chats using heuristic auto-detection.
        Support:
        1. List of messages: [{"role": "user", "content": "..."}]
        2. OpenAI Export (conversations.json): List of conversation objects with "mapping".
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in {path.name}")
            return []

        messages = []
        
        # Heuristic 1: List of conversations (OpenAI Export)
        if isinstance(data, list):
            # Check for OpenAI Export format: List of dicts, each has 'mapping' or 'title'
            if len(data) > 0 and isinstance(data[0], dict) and ("mapping" in data[0] or "current_node" in data[0]):
                # logger.info(f"Detected OpenAI Export format in {path.name}")
                for convo in data:
                    messages.extend(self._extract_openai_messages_from_convo(convo))
            else:
                # Assume simple list of messages
                messages = data
        
        # Heuristic 2: Single dict with 'messages' key
        elif isinstance(data, dict) and "messages" in data:
            messages = data["messages"]
        else:
            return []

        records = []
        for msg in messages:
            # Normalize fields
            # OpenAI exports use 'author' dict inside message, but helper below already flattened it to 'role'
            role = msg.get("role") or msg.get("author") or msg.get("author_role")
            content = msg.get("content") or msg.get("text") or msg.get("parts")
            
            # OpenAI specific: content might be list of strings
            if isinstance(content, list): 
                try:
                    content = "\n".join([str(c) for c in content if c])
                except:
                    content = ""
            
            if not isinstance(content, str) or not content.strip():
                continue
            
            # Map roles
            normalized_role = "user" # Default for analysis
            if role in ["assistant", "model", "bot", "gpt-4", "gpt-3.5-turbo"]:
                normalized_role = "assistant"
            elif role == "system":
                normalized_role = "system"
            elif role == "user":
                normalized_role = "user"
            else:
                normalized_role = "user" # Fallback
            
            # Create chunks
            chunks = self._create_chunks(content, path, source_type="chat_json", role=normalized_role)
            records.extend(chunks)

        return records

    def _extract_openai_messages_from_convo(self, conversation: Dict) -> List[Dict]:
        """Helper to extract messages from a single OpenAI conversation object."""
        msgs = []
        mapping = conversation.get("mapping", {})
        
        # The mapping is a dict of UUID -> Node. To get order, we should theoretically traverse links.
        # But commonly, sorting by create_time (if present) works sufficiently for ingestion purposes.
        # Or just dumping them is fine since we treat chunks often independently for style.
        # Let's try to sort by create_time.
        
        nodes = []
        for key, val in mapping.items():
            if not val or not isinstance(val, dict): continue
            message = val.get("message")
            if not message or not isinstance(message, dict): continue
            
            # Ignore hidden/empty messages
            if message.get("status") != "finished_successfully": continue
            
            create_time = message.get("create_time") or 0
            nodes.append((create_time, message))
            
        # Sort by time
        nodes.sort(key=lambda x: x[0])
        
        for _, message in nodes:
            author = message.get("author", {})
            role = author.get("role")
            content_dict = message.get("content", {})
            parts = content_dict.get("parts", [])
            
            # Extract text parts
            text_content = ""
            if parts:
                text_parts = [str(p) for p in parts if isinstance(p, str) and p]
                text_content = "\n".join(text_parts)
            
            if text_content.strip():
                msgs.append({
                    "role": role,
                    "content": text_content,
                    "timestamp": message.get("create_time")
                })
        
        return msgs

    def _handle_html_chat(self, path: Path) -> List[Dict]:
        """HTML chat extraction."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
        except Exception as e:
            logger.warning(f"HTML read error {path.name}: {e}")
            return []
        
        records = []
        
        # Heuristic 1: Look for common chat container logic
        # ChatGPT Export usually has specific structure
        # Often: <div class="conversation"> ... </div>
        # Message: <div data-message-author-role="user">...</div>
        
        # Try finding elements with 'data-message-author-role' (common in exports)
        messages_with_role = soup.find_all(attrs={"data-message-author-role": True})
        
        if messages_with_role:
            for el in messages_with_role:
                role = el["data-message-author-role"]
                text = el.get_text(separator="\n", strip=True)
                if not text: continue
                
                normalized_role = "user"
                if role in ["assistant", "model"]: normalized_role = "assistant"
                if role == "system": normalized_role = "system"
                
                records.extend(self._create_chunks(text, path, source_type="chat_html", role=normalized_role))
            return records

        # Fallback: Just text (treat as user doc)
        text = soup.get_text(separator="\n", strip=True)
        return self._create_chunks(text, path, source_type="chat_html", role="user")

    def _handle_audio(self, path: Path) -> List[Dict]:
        """Audio transcription using Whisper."""
        try:
            # Lazy load whisper model
            if self.whisper_model is None:
                logger.info("Loading Whisper model (base)...")
                self.whisper_model = whisper.load_model("base") # Use 'base' for speed/balance
            
            logger.info(f"Transcribing audio: {path.name}")
            result = self.whisper_model.transcribe(str(path))
            text = result.get("text", "")
            
            if not text.strip():
                return []
                
            return self._create_chunks(text, path, source_type="audio", role="user")
            
        except Exception as e:
            logger.warning(f"Audio transcription failed for {path.name}: {e}")
            return []

    def _handle_image(self, path: Path) -> List[Dict]:
        """OCR using Tesseract."""
        try:
            image = Image.open(path)
            text = pytesseract.image_to_string(image)
            
            if not text.strip():
                return []
                
            return self._create_chunks(text, path, source_type="image", role="user")
        except ImportError:
            logger.warning("OCR skipped. pytesseract or PIL not installed.")
            return []
        except Exception as e:
            # e.g. Tesseract binary not found
            logger.warning(f"OCR failed for {path.name}: {e}")
            return []

    # --- Core Logic ---

    def _create_chunks(self, text: str, path: Path, source_type: str, role: str) -> List[Dict]:
        """Split text into chunks and wrap in JSON objects."""
        if not text: return []
        
        chunks = []
        lines = text.split('\n')
        current_chunk = []
        current_length = 0
        chunk_segments = []
        
        for line in lines:
            line_len = len(line)
            if current_length + line_len > self.max_chars and current_chunk:
                chunk_segments.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(line)
            current_length += line_len
            
        if current_chunk:
            chunk_segments.append("\n".join(current_chunk))
        
        relative_path_str = str(path)
        # Try to make path relative to root if possible for cleaner IDs, else use full name
        try:
            relative_path_str = str(path.relative_to(self.root_dir))
        except ValueError:
            relative_path_str = path.name

        path_hash = hashlib.md5(relative_path_str.encode()).hexdigest()[:8]
        
        for i, segment in enumerate(chunk_segments):
            if not segment.strip(): continue
            
            record = {
                "id": f"{path_hash}_{i}",
                "source_path": str(path),
                "source_type": source_type,
                "role": role,
                "chunk_index": i,
                "text": segment
            }
            chunks.append(record)
            
            self.stats["records"] += 1
            self.stats["by_type"][source_type] = self.stats["by_type"].get(source_type, 0) + 1
            self.stats["by_role"][str(role)] = self.stats["by_role"].get(str(role), 0) + 1
            
        return chunks

    def _write_jsonl(self, records: List[Dict]):
        """Write records to output file."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        logger.info(f"Successfully wrote {len(records)} records to {self.output_file}")

    def _print_summary(self):
        print("\n--- Ingestion Summary ---")
        print(f"Files Scanned:    {self.stats['scanned']}")
        print(f"Files Ingested:   {self.stats['ingested']}")
        print(f"Files Skipped:    {self.stats['skipped']}")
        print(f"Total Chunks:     {self.stats['records']}")
        print("\nBreakdown by Type:")
        for k, v in self.stats['by_type'].items():
            print(f"  {k}: {v}")
        print("\nBreakdown by Role:")
        for k, v in self.stats['by_role'].items():
            print(f"  {k}: {v}")
        print("-------------------------\n")


# Monkey patch warning_once to avoid log spam if missing libs
def warning_once(self, msg, *args, **kwargs):
    if not hasattr(self, 'seen_warnings'): self.seen_warnings = set()
    if msg not in self.seen_warnings:
        self.warning(msg, *args, **kwargs)
        self.seen_warnings.add(msg)
logging.Logger.warning_once = warning_once


def main():
    parser = argparse.ArgumentParser(description="Ingest Haithm Corpus Files")
    parser.add_argument("--root", default="haithm_corpus", help="Root directory for input files")
    parser.add_argument("--output", default="data/haithm_corpus_raw.jsonl", help="Output JSONL file")
    parser.add_argument("--max-chars", type=int, default=2000, help="Max characters per text chunk")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output file")
    
    args = parser.parse_args()
    
    ingestor = CorpusIngestor(
        root_dir=args.root,
        output_file=args.output,
        max_chars=args.max_chars,
        force=args.force
    )
    ingestor.run()

if __name__ == "__main__":
    main()
