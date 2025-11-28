import pytest
import asyncio
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from haitham_voice_agent.tools.memory.memory_system import MemorySystem
from haitham_voice_agent.tools.memory.models.memory import MemoryType, MemorySource

# Test Data
TEST_CONTENT = "We decided to use PostgreSQL for the Mind-Q database project because it handles time-series data well."
TEST_EMBEDDING = [0.1] * 1536  # Mock embedding

import pytest_asyncio

@pytest_asyncio.fixture
async def memory_system(tmp_path):
    """Setup MemorySystem with temporary DB paths"""
    # Override config paths for testing
    with patch("haitham_voice_agent.config.Config.MEMORY_DB_PATH", tmp_path / "memory.db"), \
         patch("haitham_voice_agent.tools.memory.utils.embeddings.AsyncOpenAI"):
        
        system = MemorySystem()
        
        # Mock Embedding Generator generate method
        system.embedding_generator.generate = AsyncMock(return_value=TEST_EMBEDDING)
        
        # Mock Classifier
        system.classifier.classify = AsyncMock(return_value={
            "project": "Mind-Q",
            "topic": "Database Selection",
            "type": "decision",
            "tags": ["database", "postgresql", "architecture"],
            "sentiment": "positive",
            "importance": 5,
            "confidence": 0.95
        })
        
        # Mock Summarizer
        system.summarizer.summarize = AsyncMock(return_value={
            "ultra_brief": "Selected PostgreSQL for Mind-Q.",
            "executive_summary": ["Chose PostgreSQL", "Good for time-series"],
            "detailed_summary": "We selected PostgreSQL...",
            "decisions": ["Use PostgreSQL"],
            "action_items": ["Install Postgres"],
            "open_questions": [],
            "key_insights": [],
            "people_mentioned": [],
            "projects_mentioned": ["Mind-Q"]
        })
        
        await system.initialize()
        yield system
        
        # Cleanup (handled by tmp_path, but good to be explicit if needed)

@pytest.mark.asyncio
async def test_add_memory(memory_system):
    """Test adding a memory"""
    memory = await memory_system.add_memory(TEST_CONTENT, source="voice")
    
    assert memory is not None
    assert memory.project == "Mind-Q"
    assert memory.type == MemoryType.DECISION
    assert memory.source == MemorySource.VOICE
    assert memory.embedding == TEST_EMBEDDING
    
    # Verify SQLite storage
    stored_memory = await memory_system.sqlite_store.get_memory(memory.id)
    assert stored_memory is not None
    assert stored_memory.id == memory.id
    assert stored_memory.project == "Mind-Q"
    
    print(f"\n✓ Memory added: {memory.id}")

@pytest.mark.asyncio
async def test_search_memory(memory_system):
    """Test searching memories"""
    # Add a memory first
    await memory_system.add_memory(TEST_CONTENT)
    
    # Search
    results = await memory_system.search_memories("PostgreSQL", limit=1)
    
    assert len(results) == 1
    assert results[0].project == "Mind-Q"
    assert "PostgreSQL" in results[0].detailed_summary
    
    print(f"\n✓ Search returned {len(results)} result(s)")

@pytest.mark.asyncio
async def test_delete_memory(memory_system):
    """Test deleting a memory"""
    memory = await memory_system.add_memory(TEST_CONTENT)
    
    # Delete
    success = await memory_system.delete_memory(memory.id)
    assert success is True
    
    # Verify deletion
    stored = await memory_system.sqlite_store.get_memory(memory.id)
    assert stored is None
    
    # Verify vector deletion (mocked check or real if using real chroma)
    # Since we use real Chroma in the class (but with tmp path), we can check
    # But VectorStore.search might return empty if deleted
    results = await memory_system.search_memories("PostgreSQL")
    assert len(results) == 0
    
    print(f"\n✓ Memory deleted")
