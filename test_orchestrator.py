import asyncio
from haitham_voice_agent.ollama_orchestrator import get_orchestrator

async def test():
    orchestrator = get_orchestrator()
    
    test_cases = [
        "Hello, how are you?",
        "Open the downloads folder",
        "Plan a trip to Paris",
        "Summarize this PDF file",
        "What is 5 + 3?"
    ]
    
    print("Testing Ollama Orchestrator...")
    for text in test_cases:
        print(f"\nInput: {text}")
        result = await orchestrator.classify_request(text)
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test())
