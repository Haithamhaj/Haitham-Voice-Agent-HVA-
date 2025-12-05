import os
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class SimpleOrganizer:
    """
    Simple, rule-based file organizer.
    Organizes files by extension into predefined categories.
    Zero cost, no LLM usage.
    """
    
    CATEGORIES = {
        "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".heic"},
        "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages", ".md"},
        "Spreadsheets": {".xls", ".xlsx", ".csv", ".numbers", ".ods"},
        "Presentations": {".ppt", ".pptx", ".key", ".odp"},
        "Audio": {".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg"},
        "Video": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"},
        "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
        "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml", ".yaml", ".sql"},
        "Executables": {".exe", ".msi", ".dmg", ".pkg", ".app"}
    }
    
    def __init__(self):
        pass
        
    async def scan_and_plan(self, directory: str, instruction: str = None) -> Dict[str, Any]:
        """
        Scan directory and generate a simple reorganization plan.
        """
        root_path = Path(directory)
        if not root_path.exists():
            return {"error": f"Directory not found: {directory}"}
            
        logger.info(f"Starting Simple Scan of {directory}...")
        
        plan = {
            "root": str(root_path),
            "timestamp": datetime.now().isoformat(),
            "changes": [],
            "ignored": 0,
            "scanned": 0,
            "mode": "simple"
        }
        
        # Determine Recursion
        is_recursive = False
        if instruction:
             # Flattening implies recursion (to find files in subfolders)
             # Also check for explicit "recursive" keywords
             keywords = ["recursive", "subfolders", "deep", "all", "فرعي", "الكل", "عميق", "flatten", "direct", "مباشر", "بدون مجلدات", "الغي المجلدات", "إلغاء المجلدات"]
             if any(k in instruction.lower() for k in keywords):
                 is_recursive = True
        
        # DEBUG LOGGING
        try:
            with open("/tmp/hva_recursion_debug.log", "w") as f:
                f.write(f"Instruction: {instruction}\n")
                f.write(f"Is Recursive: {is_recursive}\n")
                f.write(f"Root Path: {root_path}\n")
        except:
            pass

        if is_recursive:
            walker = os.walk(root_path)
        else:
            # Non-recursive: Only scan the root directory
            try:
                # Get all files in root_path (filtering hidden ones)
                files = [f.name for f in root_path.iterdir() if f.is_file() and not f.name.startswith(".")]
                walker = [(str(root_path), [], files)]
            except Exception as e:
                logger.error(f"Error scanning root path: {e}")
                walker = []

        for root, dirs, files in walker:
            # Skip hidden dirs (only relevant for recursive)
            if is_recursive and Path(root).name.startswith("."):
                continue
                
            for file in files:
                if file.startswith("."):
                    continue
                    
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                
                # Check for "Flatten" / "Direct" Instruction
                if instruction and ("direct" in instruction.lower() or "flatten" in instruction.lower() or "مباشر" in instruction or "بدون مجلدات" in instruction or "الغي المجلدات" in instruction or "إلغاء المجلدات" in instruction):
                    # Flatten: Move to root
                    category = ""
                    reason = "Flattened to root directory"
                # Check for Date Sorting Instruction
                elif instruction and ("date" in instruction.lower() or "تاريخ" in instruction):
                    # Sort by Date: Year/Month
                    mtime = file_path.stat().st_mtime
                    dt = datetime.fromtimestamp(mtime)
                    category = f"{dt.year}/{dt.strftime('%m-%B')}"
                    reason = f"Sorted by Date: {dt.strftime('%Y-%m-%d')}"
                else:
                    # Default: Sort by Extension
                    # Find category
                    category = "Others"
                    for cat, extensions in self.CATEGORIES.items():
                        if ext in extensions:
                            category = cat
                            break
                    reason = f"File extension {ext} maps to {category}"
                
                # Proposed path
                if category:
                    proposed_path = root_path / category / file
                else:
                    proposed_path = root_path / file
                
                plan["scanned"] += 1
                
                # Skip if already in correct place
                if proposed_path.resolve() == file_path.resolve():
                    continue
                plan["changes"].append({
                    "original_path": str(file_path),
                    "proposed_path": str(proposed_path),
                    "new_filename": file, # No renaming in simple mode
                    "category": category,
                    "reason": reason,
                    "usage": {"cost": 0.0, "tokens": 0} # Explicit zero cost
                })
                
        return plan

    async def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the simple plan"""
        # Reuse DeepOrganizer's execution logic or implement simple move
        # For simplicity and consistency, we can reuse the same structure
        # But since DeepOrganizer has complex indexing, let's keep it simple here or import it?
        # Better to have a shared executor or just implement move here.
        
        report = {
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        changes = plan.get("changes", [])
        operations_log = []
        
        for change in changes:
            try:
                src = Path(change["original_path"])
                dst = Path(change["proposed_path"])
                
                if not src.exists():
                    report["failed"] += 1
                    continue
                    
                dst.parent.mkdir(parents=True, exist_ok=True)
                
                if dst.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dst = dst.parent / f"{dst.stem}_{timestamp}{dst.suffix}"
                    
                shutil.move(str(src), str(dst))
                report["success"] += 1
                
                operations_log.append({
                    "src": str(src),
                    "dst": str(dst),
                    "reason": change.get("reason"),
                    "category": change.get("category")
                })
                
            except Exception as e:
                report["failed"] += 1
                report["errors"].append(str(e))
                
        # Create Checkpoint (Zero Cost)
        if operations_log:
            try:
                from haitham_voice_agent.tools.checkpoint_manager import get_checkpoint_manager
                cm = get_checkpoint_manager()
                await cm.create_checkpoint(
                    action_type="simple_organize",
                    description=f"Simple Organization of {len(operations_log)} files",
                    operations=operations_log,
                    meta={
                        "model": "Rule-Based (Free)",
                        "cost": 0.0,
                        "tokens": 0
                    }
                )
            except Exception:
                pass
                
        return report

# Singleton
_simple_organizer = None

def get_simple_organizer():
    global _simple_organizer
    if _simple_organizer is None:
        _simple_organizer = SimpleOrganizer()
    return _simple_organizer
