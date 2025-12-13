#!/usr/bin/env python3
"""
JSON Stress Test (Executive Directive)
======================================
Purpose: 
    Stress-test the V2 Fine-Tuned Model to ensure 'Alignment Tax' hasn't broken 
    the system's ability to output valid JSON.

Success Criteria:
    - Failure Rate <= 5% (Acceptable for V2).
    - If > 5%, TRIGGER SYNTHETIC DATA PLAN (V2.1).

Usage:
    python scripts/verify_json_integrity.py
"""

import json
import logging
from typing import List, Dict, Any
from haitham_voice_agent.intelligence.ollama_orchestrator import OllamaOrchestrator, Config

# Mock Config to ensure we use the right model (can be overridden)
# Config.OLLAMA_MODEL = "hva-haithm-v2"  # User must ensure this is set in environment or config
Config.LOG_ROUTING_CLASSIFICATIONS = False # Disable logging during test

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("JSON_STRESS_TEST")

# --- 1. THE DATASET (50 Examples) ---
TECHNICAL_TESTS = [
    "open_folder", "open window", "open app safari", "show files in Downloads", "list documents by date",
    "organize downloads folder", "sort files by size", "system status", "check cpu usage", "check ram",
    "search for invoice.pdf", "find file annual report", "where is the contract", "run diagnostics",
    "work mode", "activate work mode", "meeting mode", "chill mode", "good morning", "morning briefing",
    "create task call client", "add task buy milk", "remind me to sleep", "what is 5+5", "define AI"
]

NATURAL_TESTS = [
    "يا هيثم افتح لي مجلد التنزيلات بالله",
    "دبر لي ملف العقد ضروري",
    "شوف لي الجهاز ليش بطيء",
    "ياخي الجهاز يعلق، شيك عليه",
    "رتب لي هالمجلد المحيوس",
    "نظم المستندات بس لا تحوس الدنيا",
    "وين حطيت ملفات المشروع؟",
    "طلع لي ملف الفواتير من شهر 5",
    "صباح الخير يا باشا",
    "شغل لي وضع الشغل خلنا نركز",
    "يا رجل طفش، تفعيل وضع الاستكنان",
    "عندي اجتماع بعد شوي، جهز الوضع",
    "ذكرني اكلم المدير بكرة الصبح",
    "سجل عندك مهمة جديدة: مراجعة العقود",
    "كم تاريخ اليوم يا وحش؟",
    "وش رأيك في الذكاء الاصطناعي؟",
    "من جدك؟ افتح سفاري",
    "ياخي الايميلات كثرت، لخص لي المهم",
    "ترجم لي هالملف بسرعة",
    "عندي فكرة مشروع مجنونة",
    "اسمع، خطط لي لرحلة دبي",
    "بدي ملف عن التسويق",
    "وين ملفات البوربوينت؟",
    "الجهاز حامي، شيك الحرارة",
    "خلصنا شغل، فكنا"
]

ALL_TESTS = TECHNICAL_TESTS + NATURAL_TESTS

async def run_stress_test():
    print("\n" + "="*50)
    print("🚦 STARTING JSON STRESS TEST (EXECUTIVE DIRECTIVE)")
    print("="*50)
    print(f"Total Tests: {len(ALL_TESTS)}")
    print(f"Model Target: {Config.OLLAMA_MODEL}")
    print("-" * 50)

    orchestrator = OllamaOrchestrator()
    
    passed = 0
    failed = 0
    failures = []

    for i, user_input in enumerate(ALL_TESTS):
        print(f"[{i+1}/{len(ALL_TESTS)}] Input: '{user_input}' ... ", end="", flush=True)
        
        try:
            # We bypass the full orchestrator flow and hit the model directly via the same method
            # but we act as if it's the classification step.
            result = await orchestrator.classify_request(user_input)
            
            # Validation Logic
            if isinstance(result, dict) and "type" in result:
                # Extra Check: Does it have 'intent' if execute_command?
                if result.get("type") == "execute_command" and "intent" not in result:
                     print("❌ FAIL (Missing intent)")
                     failed += 1
                     failures.append({"input": user_input, "error": "Missing 'intent' field", "raw": result})
                else:
                    print("✅ PASS")
                    passed += 1
            else:
                # Should not happen because classify_request returns dict,
                # but if the internal json.loads failed inside orchestrator, it returns a delegate/error dict.
                # If reason is 'json_parse_error', it's a FAIL for this test.
                if result.get("reason") == "json_parse_error":
                     print("❌ FAIL (JSON Parse Error)")
                     failed += 1
                     failures.append({"input": user_input, "error": "Invalid JSON Output", "raw": result})
                else:
                     # It returned a valid fallback dict (e.g. delegate), which is technically valid JSON behavior
                     print("✅ PASS (Fallback/Delegate)")
                     passed += 1

        except Exception as e:
            print(f"❌ FAIL (Exception: {e})")
            failed += 1
            failures.append({"input": user_input, "error": str(e), "raw": "CRASH"})

    # --- REPORTING ---
    failure_rate = (failed / len(ALL_TESTS)) * 100
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS")
    print("="*50)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Failure Rate: {failure_rate:.1f}%")
    
    print("-" * 50)
    if failure_rate <= 5.0:
        print("✅ RESULT: PASSED (Under 5% Threshold)")
        print("🚀 ACTION: PROCEED TO DEPLOYMENT")
    else:
        print("❌ RESULT: FAILED (Over 5% Threshold)")
        print("⚠️ ACTION: STOP DEPLOYMENT. TRIGGER PLAN 'V2.1' (Synthetic Data).")
        print("\n📝 Failure Log:")
        for fail in failures:
            print(f" - Input: {fail['input']}")
            print(f"   Error: {fail['error']}")

    print("="*50)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_stress_test())
