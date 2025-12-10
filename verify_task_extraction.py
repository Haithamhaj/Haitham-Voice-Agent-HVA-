
import asyncio
from haitham_voice_agent.ollama_orchestrator import get_orchestrator
from haitham_voice_agent.tools.tasks.task_manager import task_manager

async def test_extraction():
    print("----------------------------------------------------------------")
    print("              VERIFYING SMART TASK EXTRACTION                   ")
    print("----------------------------------------------------------------")
    
    ollama = get_orchestrator()
    
    # Test Case 1: English
    text_en = "Add task call mom tomorrow at 5 PM"
    print(f"\n[1] Testing: '{text_en}'")
    res_en = await ollama.extract_task_details(text_en)
    print(f" -> Extracted: {res_en}")
    
    # Test Case 2: Arabic
    text_ar = "ذكرني باجتماع الفريق يوم الاثنين الساعة 10 صباحا"
    print(f"\n[2] Testing: '{text_ar}'")
    res_ar = await ollama.extract_task_details(text_ar)
    print(f" -> Extracted: {res_ar}")
    
    # Test Case 3: Task Manager Creation (Dry Run)
    if res_en.get("due_date"):
        print(f"\n[3] Creating Task in Manager (Dry Run)...")
        try:
            # We won't actually save it to pollute, just check if method accepts it
            # But wait, create_task saves. Let's create and delete.
            task = task_manager.create_task(
                title=res_en.get("title"),
                due_date=res_en.get("due_date")
            )
            print(f" -> Task Created: ID={task.id}, Due={task.due_date}")
            
            # Cleanup
            task_manager.delete_task(task.id, "inbox")
            print(" -> Task Deleted (Cleanup OK)")
        except Exception as e:
            print(f" -> FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_extraction())
