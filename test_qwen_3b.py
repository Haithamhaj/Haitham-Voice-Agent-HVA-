import asyncio
import aiohttp
import json
import time

MODEL = "qwen2.5:3b"
BASE_URL = "http://localhost:11434"

SYSTEM_PROMPT = """
You are Haitham, a smart Arabic/English voice assistant orchestrator.

YOUR JOB: Classify user requests and respond with JSON ONLY.

═══════════════════════════════════════════════════════════
RULE 1: ANSWER DIRECTLY (type: direct_response)
═══════════════════════════════════════════════════════════
When request is:
- Greetings: مرحبا، صباح الخير، كيف حالك، hello، hi، شكراً، مع السلامة
- Simple questions: ما هو X؟، اشرح لي Y، what is Z?
- Calculations: كم 5+3؟، what is 20% of 100?
- General knowledge: questions you can answer from your knowledge

Response:
{"type": "direct_response", "response": "إجابتك هنا"}

═══════════════════════════════════════════════════════════
RULE 2: EXECUTE COMMAND (type: execute_command)
═══════════════════════════════════════════════════════════
When request is a simple system command:

VALID INTENTS:
- open_folder: افتح مجلد، open folder
- open_app: افتح برنامج، شغل تطبيق، open app، launch
- show_files: اعرض الملفات، list files (params: path, sort_by [date, size, name])
- morning_briefing: صباح الخير، good morning (triggers daily briefing)
- work_mode: وضع العمل، work mode
- meeting_mode: وضع الاجتماع، meeting mode
- chill_mode: وضع الراحة، chill mode
- system_status: حالة النظام، كم البطارية، system status

Response:
{"type": "execute_command", "intent": "open_folder", "parameters": {"path": "Downloads"}}

═══════════════════════════════════════════════════════════
RULE 3: DELEGATE TO GPT (type: delegate, delegate_to: gpt)
═══════════════════════════════════════════════════════════
When request contains these keywords:
- plan، خطط، خطة، planning
- execute، نفذ، تنفيذ
- email، إيميل، بريد، رسالة
- memory، ذاكرة، احفظ، تذكر، save، remember
- json
- Multi-step complex tasks

Response:
{"type": "delegate", "delegate_to": "gpt", "reason": "needs planning", "keywords": ["plan"]}

═══════════════════════════════════════════════════════════
RULE 4: DELEGATE TO GEMINI (type: delegate, delegate_to: gemini)
═══════════════════════════════════════════════════════════
When request contains these keywords:
- pdf، ملف PDF
- translate، ترجم، ترجمة
- summarize، لخص، ملخص، تلخيص
- analyze، حلل، تحليل
- image، صورة، صور

Response:
{"type": "delegate", "delegate_to": "gemini", "reason": "document analysis", "keywords": ["pdf"]}

═══════════════════════════════════════════════════════════
RULE 5: NEEDS CLARIFICATION (type: needs_clarification)
═══════════════════════════════════════════════════════════
When request is ambiguous or missing critical details:
- "Remind me" (Missing: what, when)
- "Add task" (Missing: title)

Response:
{"type": "needs_clarification", "question": "بماذا تريد أن أذكرك؟", "missing_slots": ["content"]}

CRITICAL RULES:
1. RESPOND WITH JSON ONLY - no extra text
2. Use Arabic response for Arabic input
"""

TEST_CASES = [
    {"input": "افتح مجلد التنزيلات", "expected_type": "execute_command", "desc": "Simple Command (Arabic)"},
    {"input": "Open Safari app", "expected_type": "execute_command", "desc": "Simple Command (English)"},
    {"input": "خطط لمشروع جديد لتعلم بايثون", "expected_type": "delegate", "expected_delegate": "gpt", "desc": "Complex Planning"},
    {"input": "لخص هذا الملف PDF", "expected_type": "delegate", "expected_delegate": "gemini", "desc": "Document Analysis"},
    {"input": "ذكرني", "expected_type": "needs_clarification", "desc": "Ambiguous Request"},
    {"input": "صباح الخير", "expected_type": "execute_command", "expected_intent": "morning_briefing", "desc": "Morning Briefing"},
]

SUMMARIZATION_TEXT = """
Artificial Intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term "artificial intelligence" to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving", however, this definition is rejected by major AI researchers.

AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Tesla), automated decision-making and competing at the highest level in strategic game systems (such as chess and Go).
"""

async def test_routing():
    print(f"\n🚀 Testing Routing with {MODEL}...\n")
    print(f"{'TEST CASE':<40} | {'STATUS':<10} | {'TIME':<10} | {'RESULT'}")
    print("-" * 100)
    
    async with aiohttp.ClientSession() as session:
        for case in TEST_CASES:
            start_time = time.time()
            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": case["input"]}
                ],
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.1}
            }
            
            try:
                async with session.post(f"{BASE_URL}/api/chat", json=payload) as response:
                    result = await response.json()
                    duration = time.time() - start_time
                    content = result.get("message", {}).get("content", "")
                    
                    try:
                        data = json.loads(content)
                        actual_type = data.get("type")
                        
                        success = actual_type == case["expected_type"]
                        if success and "expected_delegate" in case:
                            success = data.get("delegate_to") == case["expected_delegate"]
                        if success and "expected_intent" in case:
                            success = data.get("intent") == case["expected_intent"]
                            
                        status = "✅ PASS" if success else "❌ FAIL"
                        print(f"{case['desc']:<40} | {status:<10} | {duration:.2f}s    | {actual_type}")
                        if not success:
                            print(f"   Expected: {case['expected_type']} -> Got: {data}")
                            
                    except json.JSONDecodeError:
                        print(f"{case['desc']:<40} | ❌ JSON  | {duration:.2f}s    | Invalid JSON")
                        
            except Exception as e:
                print(f"{case['desc']:<40} | ❌ ERR   | 0.00s    | {e}")

async def test_summarization():
    print(f"\n📚 Testing Summarization with {MODEL}...\n")
    
    prompt = f"Summarize the following text in 1 sentence and provide a title:\n\n{SUMMARIZATION_TEXT}"
    
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3}
        }
        
        async with session.post(f"{BASE_URL}/api/generate", json=payload) as response:
            result = await response.json()
            duration = time.time() - start_time
            content = result.get("response", "").strip()
            
            print(f"⏱️ Time taken: {duration:.2f}s")
            print("-" * 50)
            print(content)
            print("-" * 50)

async def main():
    await test_routing()
    await test_summarization()

if __name__ == "__main__":
    asyncio.run(main())
