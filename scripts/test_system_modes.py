import asyncio
from haitham_voice_agent.tools.system_tools import SystemTools

async def test_modes():
    tools = SystemTools()
    
    print("--- Testing Meeting Mode ---")
    res = await tools.meeting_mode()
    print(res)
    
    await asyncio.sleep(2)
    
    print("--- Testing Work Mode ---")
    res = await tools.work_mode()
    print(res)
    
    await asyncio.sleep(2)
    
    print("--- Testing Chill Mode ---")
    res = await tools.chill_mode()
    print(res)

if __name__ == "__main__":
    asyncio.run(test_modes())
