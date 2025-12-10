
import asyncio
from haitham_voice_agent.ollama_orchestrator import get_orchestrator
from haitham_voice_agent.dispatcher import get_dispatcher
from haitham_voice_agent.tools.calendar import CalendarTools

async def verify_sync():
    print("----------------------------------------------------------------")
    print("              VERIFYING TASK -> CALENDAR SYNC                   ")
    print("----------------------------------------------------------------")
    
    # 1. Simulate Chat Request Logic (since we can't easily call the API route directly from script without running server)
    # We will manually run the logic snippet
    
    text = "Add task finalize report tomorrow at 9 AM"
    print(f"Request: '{text}'")
    
    ollama = get_orchestrator()
    res = await ollama.extract_task_details(text)
    print(f"Extracted: {res}")
    
    if res.get("due_date"):
        title = res.get("title")
        due_date = res.get("due_date")
        
        print("\n[Sync Check] Dispatching Calendar Event...")
        cal = CalendarTools()
        event_res = await cal.create_event(title, due_date)
        print(f"Calendar Result: {event_res}")
        
        if event_res.get("success"):
            print("✅ Calendar Event Created Successfully")
            # Cleanup
            # event_id = event_res.get("event_id")
            # await cal.delete_event(event_id) 
        else:
            print("❌ Calendar Creation Failed")

if __name__ == "__main__":
    asyncio.run(verify_sync())
