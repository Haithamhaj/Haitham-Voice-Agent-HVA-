import asyncio
from haitham_voice_agent.tools.memory.storage.vector_store import VectorStore

async def check_vector():
    print("🔍 Checking Vector Store...")
    try:
        vs = VectorStore()
        count = vs.count()
        print(f"✅ Vector Count: {count}")
        
        if count > 0:
            peek = vs.collection.peek(limit=5)
            print(f"👀 Peek: {len(peek['ids'])} items")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_vector())
