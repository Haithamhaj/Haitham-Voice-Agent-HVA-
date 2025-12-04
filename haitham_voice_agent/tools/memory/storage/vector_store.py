import logging
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Any, Optional

from haitham_voice_agent.config import Config

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Vector storage using ChromaDB
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (Config.MEMORY_DB_PATH.parent / "vector_db")
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        try:
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )
            
            self.collection = self.client.get_or_create_collection(
                name="memories",
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"VectorStore initialized at {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def add_embedding(self, memory_id: str, embedding: List[float], metadata: Dict[str, Any]):
        """
        Add or update embedding
        """
        try:
            # Ensure metadata values are strings, ints, floats, or bools (Chroma restriction)
            clean_metadata = {}
            for k, v in metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    clean_metadata[k] = v
                elif v is None:
                    continue
                else:
                    clean_metadata[k] = str(v)
            
            self.collection.upsert(
                ids=[memory_id],
                embeddings=[embedding],
                metadatas=[clean_metadata]
            )
            logger.debug(f"Added embedding for {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add embedding: {e}")
            return False

    def search(
        self, 
        query_embedding: List[float], 
        limit: int = 10, 
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search
        """
        try:
            # Handle multiple filter criteria (ChromaDB requires $and)
            final_filter = filter_criteria
            if filter_criteria and len(filter_criteria) > 1:
                final_filter = {"$and": [{k: v} for k, v in filter_criteria.items()]}

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=final_filter
            )
            
            # Format results
            formatted_results = []
            if results["ids"]:
                ids = results["ids"][0]
                metadatas = results["metadatas"][0]
                distances = results["distances"][0]
                
                for i, memory_id in enumerate(ids):
                    formatted_results.append({
                        "id": memory_id,
                        "metadata": metadatas[i],
                        "score": 1.0 - distances[i]  # Convert distance to similarity score
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    def delete_embedding(self, memory_id: str):
        """Delete embedding"""
        try:
            self.collection.delete(ids=[memory_id])
            return True
        except Exception as e:
            logger.error(f"Failed to delete embedding: {e}")
            return False
