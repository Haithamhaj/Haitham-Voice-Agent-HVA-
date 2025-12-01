import asyncio
import logging
import sys
from unittest.mock import MagicMock, AsyncMock

# Add project root to path
sys.path.append("/Users/haitham/development/Haitham Voice Agent (HVA)")

from haitham_voice_agent.main import HVA
from haitham_voice_agent.ollama_orchestrator import OllamaOrchestrator
from haitham_voice_agent.memory.manager import MemoryManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_idea_agent():
    # 1. Mock HVA components
    hva = HVA()
    hva.stt = MagicMock()
    hva.tts = MagicMock()
    hva.llm_router = AsyncMock()
    
    # Mock STT input
    hva.stt.capture_audio.return_value = (b"audio", 1.0)
    hva.stt.transcribe_command.return_value = "I have an idea for a smart gardening app"
    
    # Mock Orchestrator
    orchestrator = OllamaOrchestrator()
    orchestrator.classify_request = AsyncMock(return_value={
        "type": "new_idea",
        "content": "I have an idea for a smart gardening app"
    })
    
    # Inject mocked orchestrator
    import haitham_voice_agent.main
    haitham_voice_agent.main.get_orchestrator = lambda: orchestrator
    
    # Mock Memory Manager
    # We want to test the REAL MemoryManager logic calling the Mocked LLMRouter
    # So we shouldn't mock MemoryManager entirely.
    # But in the previous test we mocked MemoryManager.crystallize_idea directly.
    # To verify the model switch, we need to mock LLMRouter inside MemoryManager.
    
    real_memory_manager = MemoryManager()
    real_memory_manager.llm_router = AsyncMock()
    real_memory_manager.llm_router.generate_with_gpt.return_value = """
    {
        "title": "Smart Garden AI",
        "executive_summary": "AI-powered gardening assistant",
        "objectives": ["Monitor soil", "Automate watering", "Identify plants"],
        "key_features": ["Sensors", "App", "AI"],
        "first_steps": ["Buy sensors", "Code app"],
        "tags": ["iot", "ai", "gardening"]
    }
    """
    # Mock SQLiteStore to avoid DB operations
    real_memory_manager.sqlite_store = AsyncMock()
    real_memory_manager.vector_store = MagicMock()
    
    # Inject real memory manager with mocked dependencies
    haitham_voice_agent.main.get_memory_manager = lambda: real_memory_manager
    
    # Patch route_command to avoid interception
    mock_intent = {"action": "unknown", "confidence": 0.0}
    hva.route_command = MagicMock(return_value=mock_intent)
    haitham_voice_agent.main.route_command = MagicMock(return_value=mock_intent)
    
    # 2. Run process_command_mode
    print("Starting Idea Agent Test...")
    await hva.process_command_mode()
    
    # 3. Verify Interactions
    
    # Check if generate_with_gpt was called with logical_model="logical.nano"
    real_memory_manager.llm_router.generate_with_gpt.assert_called_once()
    call_kwargs = real_memory_manager.llm_router.generate_with_gpt.call_args.kwargs
    assert call_kwargs.get("logical_model") == "logical.nano", f"Expected logical.nano, got {call_kwargs.get('logical_model')}"
    logger.info("✅ Verification 1 SUCCESS: generate_with_gpt called with logical.nano (gpt-4o-mini).")
    
    # Check if confirmation was spoken
    # We expect "Created new project: Smart Garden AI. Defined 3 objectives." (since language defaults to 'ar' but message logic handles it)
    # Wait, HVA defaults to 'ar'.
    # msg_ar = f"تم إنشاء مشروع جديد باسم {title}. حددت له {objectives_count} أهداف."
    expected_msg_part = "تم إنشاء مشروع جديد باسم Smart Garden AI"
    
    found = False
    for call in hva.tts.speak.call_args_list:
        if expected_msg_part in str(call):
            found = True
            break
    
    if found:
        logger.info("✅ Verification 2 SUCCESS: Confirmation spoken.")
    else:
        logger.error(f"❌ Verification 2 FAILED: Confirmation not found in {hva.tts.speak.call_args_list}")

if __name__ == "__main__":
    asyncio.run(test_idea_agent())
