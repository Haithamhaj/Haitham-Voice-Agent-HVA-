import asyncio
import json
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from haitham_voice_agent.config import Config
from haitham_voice_agent.llm_router import get_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Verification")

async def test_backend():
    print("\n=== Verifying HVA Fine-Tuning Lab Backend ===\n")

    # 1. Test Status Endpoint Logic
    print("[1] Testing Status Logic...")
    dataset_path = project_root / Config.FINETUNE_DATASET_PATH
    model_path = project_root / Config.FINETUNE_MODEL_PATH
    
    print(f"  - Dataset Path: {dataset_path} ({'Exists' if dataset_path.exists() else 'Missing'})")
    print(f"  - Model Path: {model_path} ({'Exists' if model_path.exists() else 'Missing'})")
    
    # 2. Test Dataset Preview Logic
    print("\n[2] Testing Dataset Preview Logic...")
    if dataset_path.exists():
        with open(dataset_path, "r") as f:
            line = f.readline()
            try:
                data = json.loads(line)
                print(f"  - ✅ Successfully read first line: {json.dumps(data)[:50]}...")
            except json.JSONDecodeError:
                print("  - ❌ Failed to decode JSONL line.")
    else:
        print("  - ⚠️ Dataset not found, skipping preview test.")

    # 3. Test Tutor Chat (Mock)
    print("\n[3] Testing Tutor Chat (LLM Router)...")
    router = get_router()
    
    # Mock request
    prompt = "What is this page?"
    system_prompt = "You are a helpful tutor."
    
    try:
        # We test generation directly as convincing the router to use 'gpt' for chat
        print("  - sending request to GPT...")
        response = await router.generate_with_gpt(
            prompt=prompt,
            system_instruction=system_prompt,
            temperature=0.7,
            logical_model="logical.mini" 
        )
        print(f"  - ✅ GPT Response: {response['content'][:50]}...")
    except Exception as e:
        print(f"  - ❌ Chat Generation Failed: {e}")

    # 4. Test Comparison (Mock Local)
    print("\n[4] Testing Model Comparison (Local)...")
    try:
        # This requires Ollama running. We will try a dry run request.
        # If Ollama is not running, this will fail, which is expected in CI but here we check.
        # We'll set a short timeout or just skip if we think it's risky. 
        # But let's try calling the method if possible.
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 11434))
        if result == 0:
            print("  - Ollama is running. Sending test generation...")
            try:
                resp = await router.generate_with_local("Hello", temperature=0.1)
                print(f"  - ✅ Local Response: {resp['content'][:50]}...")
            except Exception as e:
                print(f"  - ❌ Local Generation Failed: {e}")
        else:
            print("  - ⚠️ Ollama not running (port 11434 closed). Skipping local inference test.")
        sock.close()
    except Exception as e:
        print(f"  - Error checking Ollama: {e}")

    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    asyncio.run(test_backend())
