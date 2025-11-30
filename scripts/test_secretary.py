import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from haitham_voice_agent.tools.secretary import get_secretary

async def test_secretary():
    print("🧪 Testing Secretary Module...")
    
    secretary = get_secretary()
    
    # 1. Test Morning Briefing
    print("\n🌅 Testing Morning Briefing...")
    briefing = await secretary.get_morning_briefing()
    print("--- Briefing Output ---")
    print(briefing["text"])
    print("-----------------------")
    
    if "Morning Briefing" in briefing["text"] and "Weather" in briefing["text"]:
        print("✅ Briefing generated successfully")
    else:
        print("❌ Briefing generation failed")
        
    # 2. Test Work Mode (Simulation)
    # We won't actually open apps to avoid disturbing user, but we check the return string
    print("\n💼 Testing Work Mode...")
    # Mocking system tools to avoid opening real apps during test
    secretary.system_tools.open_app = lambda x: asyncio.sleep(0.1)
    secretary.system_tools.set_volume = lambda x: asyncio.sleep(0.1)
    
    res = await secretary.set_work_mode("work")
    print(f"Result: {res}")
    
    if "Work Mode Activated" in res:
        print("✅ Work Mode logic correct")
    else:
        print("❌ Work Mode logic failed")

if __name__ == "__main__":
    asyncio.run(test_secretary())
