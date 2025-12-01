import sys
sys.path.append("/Users/haitham/development/Haitham Voice Agent (HVA)")
from haitham_voice_agent.config import Config

def verify_models():
    print("Verifying Model Configuration...")
    
    # Check GPT_MODEL
    print(f"GPT_MODEL: {Config.GPT_MODEL}")
    assert Config.GPT_MODEL == "gpt-5", f"Expected gpt-5, got {Config.GPT_MODEL}"
    
    # Check Mappings
    nano = Config.resolve_model("logical.nano")
    print(f"logical.nano -> {nano}")
    assert nano == "gpt-5-mini", f"Expected gpt-5-mini, got {nano}"
    
    mini = Config.resolve_model("logical.mini")
    print(f"logical.mini -> {mini}")
    assert mini == "gpt-5-mini", f"Expected gpt-5-mini, got {mini}"
    
    premium = Config.resolve_model("logical.premium")
    print(f"logical.premium -> {premium}")
    assert premium == "gpt-5", f"Expected gpt-5, got {premium}"
    
    print("✅ All model verifications passed!")

if __name__ == "__main__":
    verify_models()
