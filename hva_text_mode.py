#!/usr/bin/env python3
"""
HVA Text-Only Mode
No terminal output, no voice - just clean text file
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, "/Users/haitham/development/Haitham Voice Agent (HVA)")

# Suppress logging
os.environ['HVA_QUIET_MODE'] = '1'
import logging
logging.basicConfig(level=logging.CRITICAL)

# Import HVA components
from haitham_voice_agent.tools.voice.stt import LocalSTT
from haitham_voice_agent.wake_word import get_detector
from haitham_voice_agent.llm_router import LLMRouter

# Output file
OUTPUT_FILE = Path.home() / "Desktop" / "HVA_Conversation.txt"

def write_to_file(text):
    """Append text to output file"""
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(text + "\n")

def main():
    try:
        # Initialize
        write_to_file("Initializing...")
        
        stt = LocalSTT()
        detector = get_detector()
        router = LLMRouter()
        
        # Clear previous conversation
        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()
        
        # Welcome message
        write_to_file("=" * 60)
        write_to_file("🎤 Haitham Voice Agent - Text Mode")
        write_to_file("=" * 60)
        write_to_file(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        write_to_file("")
        write_to_file("💡 Speak your command now...")
        write_to_file("")
        
        # Open file for user to see
        os.system(f'open "{OUTPUT_FILE}"')
        
        # Listen
        write_to_file("🎤 Listening...")
        result = stt.listen_realtime()
        
        if not result or not result.get('text'):
            write_to_file("❌ No speech detected")
            write_to_file("")
            write_to_file("Please try again with clearer speech.")
            return
        
        text = result['text']
        confidence = result.get('confidence', 0)
        
        # Show what was heard
        write_to_file(f"📝 You said: {text}")
        write_to_file(f"   Confidence: {confidence:.2%}")
        write_to_file("")
        
        # Extract command
        has_wake_word, command = detector.detect(text)
        if has_wake_word:
            write_to_file(f"✅ Wake word detected!")
            write_to_file(f"   Command: {command}")
        else:
            command = text
            write_to_file(f"ℹ️  Processing: {command}")
        
        write_to_file("")
        write_to_file("⚙️  Analyzing command...")
        write_to_file("")
        
        # Get plan
        import asyncio
        plan = asyncio.run(router.route(command))
        
        if not plan or plan.get('intent') == 'Unknown':
            write_to_file("❌ Could not understand command")
            write_to_file("")
            write_to_file("Please try rephrasing or being more specific.")
            return
        
        # Show plan
        intent = plan.get('intent', 'Unknown')
        tool = plan.get('tool', 'unknown')
        action = plan.get('action', 'unknown')
        params = plan.get('parameters', {})
        
        write_to_file(f"📋 Intent: {intent}")
        write_to_file(f"🔧 Tool: {tool}")
        write_to_file(f"⚡ Action: {action}")
        write_to_file("")
        
        if params:
            write_to_file("📦 Parameters:")
            for key, value in params.items():
                write_to_file(f"   • {key}: {value}")
            write_to_file("")
        
        write_to_file("✅ Command understood successfully!")
        write_to_file("")
        write_to_file("💡 To execute this command, use the full HVA interface.")
        write_to_file("")
        
        write_to_file("=" * 60)
        write_to_file("Session completed")
        write_to_file(f"Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        write_to_file("=" * 60)
        
    except KeyboardInterrupt:
        write_to_file("")
        write_to_file("⚠️  Session cancelled by user")
    except Exception as e:
        write_to_file("")
        write_to_file(f"❌ Error: {str(e)}")
        write_to_file("")
        write_to_file("Please check the system or try again.")
        import traceback
        write_to_file("")
        write_to_file("Technical details:")
        write_to_file(traceback.format_exc())

if __name__ == "__main__":
    main()
