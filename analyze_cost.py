import aiosqlite
import asyncio
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / '.hva/memory/hva_memory.db'

async def analyze():
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        return

    print(f"🔍 Analyzing Database: {DB_PATH}\n")
    
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # 1. Total Cost by Model (Last 24h)
        print("💰 Cost Breakdown (Last 24h):")
        async with db.execute("""
            SELECT model, count(*) as count, sum(cost) as total_cost 
            FROM token_usage 
            WHERE timestamp > datetime('now', '-1 day')
            GROUP BY model
        """) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                print(f"  - {row['model']}: {row['count']} calls, ${row['total_cost']:.4f}")
                
        # 2. Recent Token Usage (Last 10)
        print("\n📝 Recent LLM Calls:")
        async with db.execute("""
            SELECT timestamp, model, cost, context 
            FROM token_usage 
            ORDER BY id DESC LIMIT 10
        """) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                print(f"  - {row['timestamp']}: {row['model']} (${row['cost']:.4f}) - {row['context']}")

        # 3. Last Checkpoint
        print("\n🚩 Last Checkpoint:")
        async with db.execute("SELECT * FROM checkpoints ORDER BY timestamp DESC LIMIT 1") as cursor:
            row = await cursor.fetchone()
            if row:
                print(f"  - Action: {row['action_type']}")
                print(f"  - Desc: {row['description']}")
                print(f"  - Data: {row['data']}")
            else:
                print("  No checkpoints found.")

if __name__ == "__main__":
    asyncio.run(analyze())
