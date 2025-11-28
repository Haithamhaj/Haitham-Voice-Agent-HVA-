import pytest
import asyncio
import os
import logging
from haitham_voice_agent.tools.memory.memory_system import MemorySystem
from haitham_voice_agent.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_memory_live_smoke():
    """
    Live smoke test for Memory System.
    Requires OPENAI_API_KEY and GEMINI_API_KEY to be set.
    """
    # 1. Check for API keys
    if not Config.OPENAI_API_KEY or not Config.GEMINI_API_KEY:
        pytest.skip("Skipping live test: API keys not found in environment")
        return

    print("\n\n========== STARTING LIVE MEMORY SMOKE TEST ==========")
    
    # 2. Initialize System
    system = MemorySystem()
    await system.initialize()
    print("✓ Memory System Initialized")
    
    # 3. Add a complex memory
    # Using a unique timestamp/ID in content to ensure we find THIS specific memory
    import time
    unique_id = int(time.time())
    content = f"Meeting notes regarding the Mind-Q database migration project (ID: {unique_id}). We decided to switch from MongoDB to PostgreSQL because of better time-series support with TimescaleDB. The migration is scheduled for Q2 2025. Sarah will lead the data modeling team."
    
    print(f"\nAdding memory: {content[:50]}...")
    memory = await system.add_memory(content, source="manual", context="Weekly Engineering Sync")
    
    assert memory is not None
    assert memory.id is not None
    print(f"✓ Memory Saved! ID: {memory.id}")
    print(f"  - Project: {memory.project}")
    print(f"  - Topic: {memory.topic}")
    print(f"  - Type: {memory.type.value}")
    print(f"  - Summary: {memory.ultra_brief}")
    
    # 4. Verify Vector Search (Semantic)
    # Search with a different phrasing
    query = "Why did we choose Postgres for Mind-Q?"
    print(f"\nSearching for: '{query}'")
    
    results = await system.search_memories(query, limit=3)
    
    found = False
    for res in results:
        if str(unique_id) in res.raw_content:
            found = True
            print(f"✓ Found target memory via semantic search!")
            print(f"  - Match: {res.ultra_brief}")
            break
            
    if not found:
        print("✗ Failed to find memory via semantic search")
        # Print what was found
        for res in results:
            print(f"  - Found: {res.ultra_brief} (ID: {res.id})")
            
    assert found, "Semantic search failed to retrieve the saved memory"
    
    # 5. Cleanup (Optional - maybe we want to keep it to prove persistence?)
    # await system.delete_memory(memory.id)
    # print("\n✓ Cleanup complete")
    
    print("\n========== LIVE TEST PASSED ==========\n")

if __name__ == "__main__":
    # Allow running directly
    asyncio.run(test_memory_live_smoke())
