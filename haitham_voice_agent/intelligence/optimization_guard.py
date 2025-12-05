import hashlib
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from haitham_voice_agent.tools.memory.storage.sqlite_store import SQLiteStore

logger = logging.getLogger(__name__)

class OptimizationGuard:
    """
    Safety Layer to prevent unnecessary LLM costs.
    Acts as a gatekeeper by checking content fingerprints against a cache.
    """
    
    def __init__(self):
        self.sqlite_store = SQLiteStore()
        # Ensure we don't re-init the store if it's already running, 
        # but here we just need access to it.
        
    async def check_file(self, file_path: str, context: str) -> Dict[str, Any]:
        """
        Check if a file has already been processed in this context.
        
        Args:
            file_path: Absolute path to the file
            context: Operation context (e.g., "deep_organize")
            
        Returns:
            Dict with:
            - should_process: bool
            - cached_result: Optional[Dict]
            - reason: str
        """
        try:
            path_obj = Path(file_path)
            if not path_obj.exists():
                return {"should_process": False, "reason": "File not found"}
                
            # 1. Calculate Fingerprint (Hash)
            file_hash = self._calculate_file_hash(path_obj)
            
            # 2. Check Cache
            cached = await self.sqlite_store.get_optimization_cache(file_hash, context)
            
            if cached:
                logger.info(f"🛡️ OptimizationGuard: Blocked redundant processing for {path_obj.name} (Saved cost)")
                return {
                    "should_process": False,
                    "cached_result": cached.get("result"),
                    "reason": "Content unchanged (Cache Hit)",
                    "savings": cached.get("cost_saved", 0.0)
                }
                
            return {
                "should_process": True, 
                "file_hash": file_hash,
                "reason": "New content"
            }
            
        except Exception as e:
            logger.error(f"OptimizationGuard check failed: {e}")
            # Fail safe: Allow processing if guard fails, but log error
            return {"should_process": True, "reason": f"Guard Error: {e}"}

    async def save_result(self, file_hash: str, context: str, result: Dict[str, Any], cost_saved: float = 0.0):
        """Save a successful result to the cache"""
        try:
            await self.sqlite_store.save_optimization_cache(
                file_hash=file_hash,
                context=context,
                result=result,
                cost_saved=cost_saved
            )
        except Exception as e:
            logger.error(f"Failed to save optimization cache: {e}")

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()

# Singleton
_guard = None

def get_optimization_guard():
    global _guard
    if _guard is None:
        _guard = OptimizationGuard()
    return _guard
