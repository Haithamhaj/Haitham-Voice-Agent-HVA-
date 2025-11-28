import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

from .models.memory import Memory, MemoryType, MemorySource, SensitivityLevel
from .storage.sqlite_store import SQLiteStore
from .storage.vector_store import VectorStore
from .intelligence.classifier import SmartClassifier
from .intelligence.summarizer import Summarizer
from .utils.embeddings import EmbeddingGenerator

logger = logging.getLogger(__name__)

class MemorySystem:
    """
    Main entry point for the Advanced Memory System.
    Coordinates input processing, intelligence, storage, and retrieval.
    """
    
    def __init__(self):
        self.sqlite_store = SQLiteStore()
        self.vector_store = VectorStore()
        self.classifier = SmartClassifier()
        self.summarizer = Summarizer()
        self.embedding_generator = EmbeddingGenerator()
        
    async def initialize(self):
        """Initialize storage systems"""
        await self.sqlite_store.initialize()
        
    async def add_memory(
        self, 
        content: str, 
        source: Union[MemorySource, str] = MemorySource.MANUAL,
        context: Optional[str] = None
    ) -> Optional[Memory]:
        """
        Process and store a new memory
        """
        try:
            # 1. Generate Embedding
            embedding = await self.embedding_generator.generate(content)
            
            # 2. Classify
            classification = await self.classifier.classify(content, context)
            
            # 3. Summarize
            summary = await self.summarizer.summarize(content)
            
            # 4. Create Memory Object
            memory_id = str(uuid.uuid4())
            timestamp = datetime.now()
            
            # Handle source enum
            if isinstance(source, str):
                try:
                    source_enum = MemorySource(source.lower())
                except ValueError:
                    source_enum = MemorySource.MANUAL
            else:
                source_enum = source
            
            # Handle type enum
            try:
                type_enum = MemoryType(classification.get("type", "note").lower())
            except ValueError:
                type_enum = MemoryType.NOTE
                
            memory = Memory(
                id=memory_id,
                timestamp=timestamp,
                source=source_enum,
                project=classification.get("project", "General"),
                topic=classification.get("topic", "Unclassified"),
                type=type_enum,
                tags=classification.get("tags", []),
                ultra_brief=summary.get("ultra_brief", ""),
                executive_summary=summary.get("executive_summary", []),
                detailed_summary=summary.get("detailed_summary", ""),
                raw_content=content,
                decisions=summary.get("decisions", []),
                action_items=summary.get("action_items", []),
                open_questions=summary.get("open_questions", []),
                key_insights=summary.get("key_insights", []),
                people_mentioned=summary.get("people_mentioned", []),
                projects_mentioned=summary.get("projects_mentioned", []),
                language="en", # TODO: Detect language
                sentiment=classification.get("sentiment", "neutral"),
                importance=classification.get("importance", 3),
                confidence=classification.get("confidence", 1.0),
                sensitivity=SensitivityLevel.PRIVATE,
                embedding=embedding
            )
            
            # 5. Save to SQLite
            await self.sqlite_store.save_memory(memory)
            
            # 6. Save to Vector Store
            metadata = {
                "project": memory.project,
                "topic": memory.topic,
                "type": memory.type.value,
                "timestamp": memory.timestamp.isoformat()
            }
            self.vector_store.add_embedding(memory_id, embedding, metadata)
            
            logger.info(f"Memory stored: {memory_id} ({memory.project} - {memory.topic})")
            return memory
            
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")
            return None

    async def search_memories(
        self, 
        query: str, 
        limit: int = 5,
        project: Optional[str] = None
    ) -> List[Memory]:
        """
        Semantic search for memories
        """
        try:
            # 1. Generate query embedding
            query_embedding = await self.embedding_generator.generate(query)
            
            # 2. Search Vector Store
            filter_criteria = {}
            if project:
                filter_criteria["project"] = project
                
            vector_results = self.vector_store.search(
                query_embedding, 
                limit=limit,
                filter_criteria=filter_criteria if filter_criteria else None
            )
            
            # 3. Retrieve full objects from SQLite
            memories = []
            for result in vector_results:
                memory_id = result["id"]
                memory = await self.sqlite_store.get_memory(memory_id)
                if memory:
                    memories.append(memory)
            
            return memories
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete memory from all stores"""
        try:
            sqlite_success = await self.sqlite_store.delete_memory(memory_id)
            vector_success = self.vector_store.delete_embedding(memory_id)
            return sqlite_success and vector_success
        except Exception as e:
            logger.error(f"Failed to delete memory {memory_id}: {e}")
            return False
