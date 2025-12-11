# Haithm Corpus Ingestion Pipeline

## Purpose
The goal of this pipeline is to ingest various documents and chat logs authored by or relevant to "Haithm" (the user/persona) into a single, normalized machine-learning-ready corpus (`jsonl`). This raw text corpus will serve as the foundation for building a "Style" fine-tuning dataset for the Qwen model.


## Supported Formats

### Documents
- **PDF** (`.pdf`): Extracts text from pages.
- **Word** (`.docx`): Extracts text from paragraphs.
- **Text** (`.txt`, `.md`): Raw text ingestion.

### Chats (GPT Exports)
- **JSON** (`.json`): Supports standard "OpenAI Data Export" format (`conversations.json`), recursively parsing the conversation tree.
- **HTML** (`chat.html`): Heuristic parsing of message containers.

**Example: Ingesting a GPT Data Export**
You can ingest directly from your extracted export folder:
```bash
python scripts/ingest_haithm_corpus.py \
  --root "/Users/haitham/development/Haitham Voice Agent (HVA)/Haitham Data/GPT -Haitham 11-12-2025" \
  --force
```

### Audio (Speech-to-Text)
- **Extensions**: `.m4a`, `.mp3`, `.wav`
- **Engine**: Uses `openai-whisper` (local model, typically `base` size).
- **Requirement**: `ffmpeg` must be installed on the system.
- **Process**: Transcribes audio -> Chunks text -> Assigns role="user".

### Images (OCR)
- **Extensions**: `.png`, `.jpg`, `.jpeg`, `.webp`
- **Engine**: Uses `Tesseract OCR` via `pytesseract`.
- **Requirement**: `tesseract` binary must be installed (e.g., `brew install tesseract`).
- **Process**: OCR -> Chunks text -> Assigns role="user".

## Output Format

The script generates `data/haithm_corpus_raw.jsonl`. Each line is a JSON object corresponding to a chunk of text.

### Schema
```json
{
  "id": "7f8a9d..._0",              // Unique ID (Hash of path + chunk index)
  "source_path": "haithm_corpus/docs/my_cv.pdf",
  "source_type": "pdf",             // txt, md, pdf, docx, chat_json, chat_html
  "role": "user",                   // user (Haithm), assistant, or system
  "chunk_index": 0,                 // integer index
  "text": "Extracted text content..."
}
```

### Roles
- **user**: Represents Haithm's voice (human input in chats, or the author of static docs).
- **assistant**: Represents AI model outputs (in chat logs).
- **system**: System prompts (if found in chat logs).

## Next Steps
After populating this raw corpus, a separate process (Dataset Builder) will filter and format these records into `(Instruction, Input, Output)` pairs for fine-tuning.
