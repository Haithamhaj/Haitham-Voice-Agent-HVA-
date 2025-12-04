import requests
import json
import time

BASE_URL = "http://localhost:8765"

def test_chat(message):
    print(f"\nTesting message: '{message}'")
    try:
        response = requests.post(
            f"{BASE_URL}/chat/",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server...")
    time.sleep(5)
    
    # Test 1: Greeting (Should be Ollama)
    print("--- Test 1: Greeting (Ollama) ---")
    test_chat("مرحباً")
    
    # Test 2: Complex Task (Should be GPT)
    print("--- Test 2: Complex Task (GPT) ---")
    test_chat("Plan a marketing campaign for a new coffee brand")
