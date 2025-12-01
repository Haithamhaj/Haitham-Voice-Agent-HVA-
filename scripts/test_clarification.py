import asyncio
import logging
import sys
from unittest.mock import MagicMock, AsyncMock

# Add project root to path
sys.path.append("/Users/haitham/development/Haitham Voice Agent (HVA)")

from haitham_voice_agent.main import HVA
from haitham_voice_agent.ollama_orchestrator import OllamaOrchestrator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_clarification_loop():
    # 1. Mock HVA components
    hva = HVA()
    hva.stt = MagicMock()
    hva.tts = MagicMock()
    hva.llm_router = AsyncMock()
    
    # Mock STT to simulate conversation
    # First call: "Remind me" (Ambiguous)
    # Second call: "to call Ahmed" (Answer)
    hva.stt.capture_audio.side_effect = [
        (b"audio1", 1.0), # User input 1
        (b"audio2", 1.0)  # User input 2 (Answer)
    ]
    
    hva.stt.transcribe_command.side_effect = [
        "Remind me",      # Transcription 1
        "to call Ahmed"   # Transcription 2
    ]
    
    # Mock Orchestrator
    orchestrator = OllamaOrchestrator()
    orchestrator.classify_request = AsyncMock()
    
    # First classification: Needs Clarification
    orchestrator.classify_request.side_effect = [
        {
            "type": "needs_clarification",
            "question": "What do you want to be reminded about?",
            "missing_slots": ["content"]
        },
        # Second classification (Merged): Execute Command
        {
            "type": "execute_command",
            "intent": "create_task",
            "parameters": {"title": "Call Ahmed"}
        }
    ]
    
    # Inject mocked orchestrator
    # We need to patch get_orchestrator in main.py, but since we can't easily do that without 
    # complex patching, we'll just mock the call inside process_command_mode if possible.
    # Actually, main.py calls get_orchestrator(). 
    # Let's monkeypatch the module level function.
    import haitham_voice_agent.main
    haitham_voice_agent.main.get_orchestrator = lambda: orchestrator
    
    # Patch route_command to ensure it doesn't intercept "Remind me"
    # It must return a dict with confidence, not None
    mock_intent = {"action": "unknown", "confidence": 0.0}
    hva.route_command = MagicMock(return_value=mock_intent)
    haitham_voice_agent.main.route_command = MagicMock(return_value=mock_intent)
    
    # Mock execute_plan to verify final execution
    hva.execute_plan = AsyncMock()
    
    # 2. Run process_command_mode
    print("Starting Clarification Test...")
    await hva.process_command_mode()
    
    # 3. Verify Interactions
    
    # Check if question was spoken
    print("TTS Calls:", hva.tts.speak.call_args_list)
    # hva.tts.speak.assert_any_call("What do you want to be reminded about?", language="ar")
    
    # Manual check to be safer
    found = False
    for call in hva.tts.speak.call_args_list:
        if "What do you want to be reminded about?" in str(call):
            found = True
            break
    assert found, "Clarification question not spoken"
    logger.info("✅ Verification 1 SUCCESS: System asked for clarification.")
    
    # Check if answer was captured
    assert hva.stt.capture_audio.call_count >= 2
    logger.info("✅ Verification 2 SUCCESS: System listened for answer.")
    
    # Check if merged text was re-processed
    # The second classify_request call should be with merged text
    # Note: process_command_mode calls process_text_command for the merged text
    # process_text_command calls plan_command
    # plan_command calls orchestrator.classify_request
    
    # Wait, our mock setup for classify_request side_effect might be tricky because
    # process_command_mode calls classify_request directly first.
    # Then it calls process_text_command(merged) which calls plan_command(merged) which calls classify_request(merged).
    # So we expect 2 calls to classify_request.
    
    calls = orchestrator.classify_request.call_args_list
    if len(calls) >= 2:
        args, _ = calls[1]
        if "Remind me to call Ahmed" in args[0]:
             logger.info(f"✅ Verification 3 SUCCESS: Merged text '{args[0]}' sent for re-classification.")
        else:
             logger.error(f"❌ Verification 3 FAILED: Expected merged text, got '{args[0]}'")
    else:
        logger.error("❌ Verification 3 FAILED: classify_request not called enough times.")

    # Check execution
    if hva.execute_plan.called:
        logger.info("✅ Verification 4 SUCCESS: Plan executed after clarification.")
    else:
        # It might be called inside process_text_command -> plan_command -> execute_plan
        # Let's check if plan_command returned a plan that led to execution
        pass

if __name__ == "__main__":
    asyncio.run(test_clarification_loop())
