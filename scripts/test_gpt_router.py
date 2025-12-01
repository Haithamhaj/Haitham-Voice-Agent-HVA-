import asyncio
from haitham_voice_agent.llm_router import get_router
from haitham_voice_agent.config import Config

async def test_gpt_router():
    router = get_router()
    
    print(f"Testing Router with GPT Model: {router.gpt_model}")
    
    # Test generate_execution_plan (which uses temperature=0.3 and json_object)
    try:
        plan = await router.generate_execution_plan("Schedule a meeting tomorrow at 5pm")
        print("Successfully generated plan:")
        print(plan)
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_gpt_router())
