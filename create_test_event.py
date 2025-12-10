
import asyncio
import datetime
from haitham_voice_agent.tools.calendar import CalendarTools

async def create_test_event():
    print("----------------------------------------------------------------")
    print("              CREATING TEST CALENDAR EVENT                      ")
    print("----------------------------------------------------------------")
    
    cal = CalendarTools()
    
    # Create event at 8:00 PM today (safe buffer)
    # Using simple "today 8pm" parsing rely on the tool's smart parsing
    # Or explicitly:
    now = datetime.datetime.now()
    target = now.replace(hour=20, minute=0, second=0)
    
    summary = "HVA Connection Test 🟢"
    start_time = target.strftime("%Y-%m-%d %H:%M")
    
    print(f"Creating event '{summary}' at {start_time}...")
    
    res = await cal.create_event(summary, start_time, duration_minutes=30)
    print(res)

if __name__ == "__main__":
    asyncio.run(create_test_event())
