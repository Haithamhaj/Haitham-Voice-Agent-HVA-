# HVA Routing Dataset Analysis

## 1. Log Discovery & Volume
- **Log Directory**: `~/.hva/logs/`
- **Files Analyzed**: `hva.log`
- **Time Span**: 2025-11-28 18:56 to 2025-12-01 11:12

### Counts
| Metric | Count | Notes |
| :--- | :--- | :--- |
| **User Commands detected** | **31** | Lines matching `Command (Raw):` |
| **Ollama Classifications** | **3** | Lines matching `Ollama classification:` |
| **Full JSON Logs** | **2** | Lines matching `DEBUG: classification =` |
| **Potential Training Pairs**| **2** | Only high-quality pairs with full JSON |

> [!WARNING]
> **Data Scarcity Alert**: The current log volume is essentially empty for training purposes (only 2 valid JSON pairs).
> Most commands were either handled by the Regex Router (bypassing Ollama) or executed when verbose logging was disabled.
>
> **Recommendation**: To build a real dataset, we must either:
> 1.  Enable full `DEBUG` logging and run the system for a few days.
> 2.  Use the 31 raw commands to **synthesize** the JSON outputs using a script (Offline Batch Processing).

## 2. Sample Request → Classification Pairs

Here are the 2 fully captured pairs found in the logs:

**Example 1**
- **User**: "Remind me"
- **Classification**:
  ```json
  {
    "type": "needs_clarification",
    "question": "What do you want to be reminded about?",
    "missing_slots": ["content"]
  }
  ```

**Example 2**
- **User**: "Remind me" (Duplicate instance)
- **Classification**:
  ```json
  {
    "type": "needs_clarification",
    "question": "What do you want to be reminded about?",
    "missing_slots": ["content"]
  }
  ```

## 3. Dataset Design & Schema

### 3.1 Proposed JSONL Schema
We will use the **Alpaca-style** instruction format compatible with Qwen fine-tuning.

```json
{
  "instruction": "You are the HVA Local Classifier. Given the user input, return ONLY a JSON object that matches the routing schema.",
  "input": "User's raw command text",
  "output": "{\"type\": \"...\", \"intent\": \"...\", ...}"
}
```

### 3.2 Fields
- `instruction`: Static system prompt (defined in `ollama_orchestrator.py`).
- `input`: The `Command (Raw)` text.
- `output`: The JSON string found in `DEBUG: classification =`.
- `metadata` (Optional): `{"timestamp": "...", "source": "hva.log"}`

### 3.3 Quality Considerations
- **Filtering**:
    - Skip empty inputs.
    - Skip `json.JSONDecodeError` outputs.
    -Deduplicate exact matches (Input + Output).
- **Language**:
    - The dataset handles both Arabic and English naturally as provided in the logs.
    - No specific language filtering needed (the model should be multilingual).

## 4. Script Design (`scripts/build_hva_routing_dataset.py`)

Since the log data is sparse, the script will support two modes (conceptually):
1.  **Extraction Mode**: Parse existing `DEBUG: classification` lines.
2.  (Future) **Synthesis Mode**: It could take the 31 raw commands and generate the JSON using OpenAI/Ollama offline.
    *   *For this task, we implemented Extraction Mode only as requested.*

### Script Logic
1.  Read `hva.log` line by line.
2.  Maintain a buffer to associate the last seen `Command (Raw):` with the next `DEBUG: classification =`.
3.  Regex match for the JSON dict.
4.  Convert Python Dict string (`{'a': 'b'}`) to valid JSON (`{"a": "b"}`).
5.  Write to `.jsonl`.

### Dry Run Safety
- The script defaults to `dry_run=True`.
- Prints stats before writing.
- Requires `--force` or interactive confirmation to write `data/dataset_hva_qwen_routing.jsonl`.

## 5. Structured Logging Update (Implemented)

To address the data scarcity identified above, we have implemented a dedicated logging mechanism that does **not** rely on Debug mode.

### 5.1 Configuration
A new flag in `haitham_voice_agent/config.py`:
```python
LOG_ROUTING_CLASSIFICATIONS: bool = True
```
When enabled (default), every routing decision is logged at INFO level.

### 5.2 Log Format
The system now logs pairs in this easy-to-parse format:
```
2025-12-10 12:00:00,000 - ... - ROUTING INPUT: open chrome
2025-12-10 12:00:00,010 - ... - ROUTING OUTPUT: {"type": "execute_command", "intent": "open_app", ...}
```

### 5.3 Updated Builder Script
The `scripts/build_hva_routing_dataset.py` has been updated to support both:
1.  **Legacy Pattern**: The sparse `DEBUG` logs previously identified.
2.  **New Pattern**: The robust `ROUTING INPUT/OUTPUT` logs.

### 5.4 Recommended Workflow
1.  Use HVA normally for a few days/weeks to accumulate data.
2.  Run the builder periodically:
    ```bash
    python scripts/build_hva_routing_dataset.py --force
    ```
3.  Once ~100+ pairs are collected, proceed to fine-Tuning in the Lab.
