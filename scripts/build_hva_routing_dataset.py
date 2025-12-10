#!/usr/bin/env python3
"""
HVA Routing Dataset Builder
===========================

Purpose:
    Extracts (User Request -> JSON Classification) pairs from HVA logs
    to build a fine-tuning dataset for Qwen 2.5.

Usage:
    python scripts/build_hva_routing_dataset.py [--force] [--output <path>]

Note:
    This script parses two logging patterns:
    1. Legacy: "Command (Raw):" ... "DEBUG: classification =" (Requires debug/verbose logs)
    2. Standard: "ROUTING INPUT:" ... "ROUTING OUTPUT:" (Always enabled via Config.LOG_ROUTING_CLASSIFICATIONS)
"""

import re
import json
import argparse
import logging
import ast
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger("DatasetBuilder")

# Constants
DEFAULT_LOG_PATH = Path.home() / ".hva" / "logs" / "hva.log"
DEFAULT_OUTPUT_PATH = Path("data/dataset_hva_qwen_routing.jsonl")

SYSTEM_INSTRUCTION = (
    "You are the HVA Local Classifier. Given the user input, "
    "return ONLY a JSON object that matches the routing schema."
)

class DatasetBuilder:
    def __init__(self, log_path: Path, output_path: Path, force: bool):
        self.log_path = log_path
        self.output_path = output_path
        self.force = force
        self.pairs = []
        self.stats = {
            "lines_scanned": 0,
            "legacy_pairs": 0,
            "new_pairs": 0,
            "errors": 0
        }

    def parse_log_line(self, line: str) -> tuple:
        """Extract timestamp and content from log line."""
        # Log format: 2025-12-01 11:01:52,223 - logger - LEVEL - Message
        match = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - .* - (.*)$", line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    def add_pair(self, input_text: str, output_text_or_dict: str, ts_str: str, is_legacy: bool):
        """Add a valid pair/row to the dataset."""
        try:
            # Normalize output to valid JSON string
            if isinstance(output_text_or_dict, dict):
                classification_json = json.dumps(output_text_or_dict, ensure_ascii=False)
            else:
                # If it's a string, try JSON parse first
                try:
                    # Try pure JSON first
                    data = json.loads(output_text_or_dict)
                    classification_json = json.dumps(data, ensure_ascii=False)
                except json.JSONDecodeError:
                    # If failed, try ast.literal_eval (for python dict strings in logs)
                    data = ast.literal_eval(output_text_or_dict)
                    classification_json = json.dumps(data, ensure_ascii=False)
            
            # Simple deduplication check based on input+output
            # This is O(N) but fine for usually small log datasets.
            for p in self.pairs:
                if p["input"] == input_text and p["output"] == classification_json:
                    return # Duplicate

            self.pairs.append({
                "instruction": SYSTEM_INSTRUCTION,
                "input": input_text,
                "output": classification_json,
                "metadata": {
                    "timestamp": ts_str,
                    "source": self.log_path.name,
                    "format_version": "v1_legacy" if is_legacy else "v2_structured"
                }
            })
            
            if is_legacy:
                self.stats["legacy_pairs"] += 1
            else:
                self.stats["new_pairs"] += 1
                
        except Exception as e:
            logger.warning(f"Failed to parse pair at {ts_str}: {e}")
            self.stats["errors"] += 1

    def scan_logs(self):
        """Scan logs and extract pairs."""
        if not self.log_path.exists():
            logger.error(f"Log file not found: {self.log_path}")
            return

        logger.info(f"Scanning {self.log_path}...")
        
        # State tracking for multi-line extraction
        last_legacy_command = None
        
        last_routing_input = None
        
        with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                self.stats["lines_scanned"] += 1
                ts_str, content = self.parse_log_line(line.strip())
                if not content: continue

                # --- PATTERN 1: NEW STRUCTURED LOGGING ---
                # ROUTING INPUT: <text>
                # ROUTING OUTPUT: <json>
                
                # Check Input
                input_match = re.search(r"^ROUTING INPUT: (.*)", content)
                if input_match:
                    last_routing_input = input_match.group(1).strip()
                    continue
                
                # Check Output (must follow Input immediately or closely)
                output_match = re.search(r"^ROUTING OUTPUT: (.*)", content)
                if output_match and last_routing_input:
                    json_str = output_match.group(1).strip()
                    self.add_pair(last_routing_input, json_str, ts_str, is_legacy=False)
                    last_routing_input = None # Reset
                    continue

                # --- PATTERN 2: LEGACY DEBUG LOGGING ---
                # Command (Raw): <text>
                # ...
                # DEBUG: classification = <dict>
                
                cmd_match = re.search(r"Command \(Raw\): (.*)", content)
                if cmd_match:
                    last_legacy_command = cmd_match.group(1).strip()
                    last_routing_input = None # Safety reset if mixed
                    continue
                
                cls_match = re.search(r"DEBUG: classification = (\{.*\})", content)
                if cls_match and last_legacy_command:
                    dict_str = cls_match.group(1)
                    self.add_pair(last_legacy_command, dict_str, ts_str, is_legacy=True)
                    last_legacy_command = None
                    continue

    def preview_data(self):
        """Show sample data."""
        if not self.pairs:
            logger.warning("No pairs extracted.")
            return
            
        logger.info("\n--- Sample Pair ---")
        sample = self.pairs[-1] # Show latest
        logger.info(f"Input:  {sample['input']}")
        logger.info(f"Output: {sample['output']}")
        logger.info(f"Meta:   {sample['metadata']}")
        logger.info("-------------------\n")

    def save_dataset(self):
        """Write to JSONL."""
        if not self.pairs:
            return

        # Check for existing file
        if self.output_path.exists() and not self.force:
            logger.warning(f"Output file exists: {self.output_path}")
            logger.warning("Use --force to overwrite. Skipping save.")
            return

        logger.info(f"Writing {len(self.pairs)} rows to {self.output_path}...")
        
        # Create parent dir
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_path, "w", encoding="utf-8") as f:
            for pair in self.pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + "\n")
        
        logger.info("✅ Dataset saved successfully.")

    def run(self):
        self.scan_logs()
        
        logger.info("\n=== Analysis Report ===")
        logger.info(f"Lines Scanned:    {self.stats['lines_scanned']}")
        logger.info(f"Legacy Pairs:     {self.stats['legacy_pairs']}")
        logger.info(f"New Pairs:        {self.stats['new_pairs']}")
        logger.info(f"Total Valid:      {len(self.pairs)}")
        logger.info(f"Parse Errors:     {self.stats['errors']}")
        logger.info("=======================\n")
        
        self.preview_data()
        
        # Only save if we found data
        if len(self.pairs) > 0:
            if self.force:
                self.save_dataset()
            else:
                logger.info("Dry run complete. Use --force to save data.")
        else:
             logger.info("Not enough data to build dataset.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build HVA Routing Dataset")
    parser.add_argument("--force", action="store_true", help="Overwrite existing dataset")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Output JSONL path")
    parser.add_argument("--logs", type=Path, default=DEFAULT_LOG_PATH, help="Input log file path")
    
    args = parser.parse_args()
    
    if not args.logs.exists():
        print(f"Error: Log file not found at {args.logs}")
        exit(1)
        
    builder = DatasetBuilder(args.logs, args.output, args.force)
    builder.run()
