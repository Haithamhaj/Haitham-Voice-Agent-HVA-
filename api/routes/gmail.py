from fastapi import APIRouter, HTTPException
from haitham_voice_agent.dispatcher import get_dispatcher

router = APIRouter(prefix="/gmail", tags=["gmail"])

@router.get("/unread")
async def get_unread_emails():
    """Get unread emails count and preview"""
    dispatcher = get_dispatcher()
    gmail_tool = dispatcher.tools.get("gmail")
    
    if not gmail_tool:
        raise HTTPException(status_code=503, detail="Gmail tool not available")
        
    try:

        # Use ConnectionManager's search_emails method
        # Filter for Primary category only to avoid spam/promotions
        result = await gmail_tool.search_emails(query="is:unread category:primary", limit=20)
        
        if result.get("error"):
            return result
            
        return {
            "count": result.get("count", 0),
            "messages": result.get("emails", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize/{message_id}")
async def summarize_email(message_id: str):
    """Summarize an email using LLM"""
    dispatcher = get_dispatcher()
    gmail_tool = dispatcher.tools.get("gmail")
    
    if not gmail_tool:
        raise HTTPException(status_code=503, detail="Gmail tool not available")
        
    try:
        # 1. Get email content
        email = await gmail_tool.get_email_by_id(message_id)
        if email.get("error"):
            raise HTTPException(status_code=404, detail="Email not found")
            
        # 2. Prepare content for LLM
        subject = email.get("subject", "")
        body = email.get("body_text", "") or email.get("snippet", "")
        
        # 3. Call LLM (using Gemini for summarization)
        from haitham_voice_agent.llm_router import get_router
        
        router = get_router()
        
        # summary_result is {"content": "...", "model": "..."}
        summary_result = await router.summarize_with_gemini(
            text=f"Subject: {subject}\n\nBody: {body}",
            summary_type="brief"
        )
        
        # Translate to Arabic if needed (or ensure prompt asks for Arabic)
        # Actually summarize_with_gemini prompt is English by default.
        # Let's use generate_with_gemini directly for Arabic control.
        
        prompt = f"""
        قم بتحليل هذه الرسالة وتلخيصها بشكل احترافي باللغة العربية.
        الموضوع: {subject}
        المحتوى: {body[:2000]}
        
        الصيغة المطلوبة:
        - **الفكرة الرئيسية**: سطر واحد.
        - **النقاط الهامة**: قائمة نقطية (تواريخ، أرقام، أسماء).
        - **الإجراء المطلوب**: إذا وجد.
        """
        
        result = await router.generate_with_gemini(prompt, temperature=0.3)
        summary = result.get("content", "تعذر التلخيص")
        
        return {"id": message_id, "summary": summary}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/task/{message_id}")
async def convert_email_to_task(message_id: str):
    """Convert email to task using LLM"""
    dispatcher = get_dispatcher()
    gmail_tool = dispatcher.tools.get("gmail")
    tasks_tool = dispatcher.tools.get("tasks")
    
    if not gmail_tool or not tasks_tool:
        raise HTTPException(status_code=503, detail="Required tools not available")
        
    try:
        # 1. Get email
        email = await gmail_tool.get_email_by_id(message_id)
        if email.get("error"):
            raise HTTPException(status_code=404, detail="Email not found")
            
        subject = email.get("subject", "")
        body = email.get("body_text", "") or email.get("snippet", "")
        
        # 2. Extract task details using GPT (Action-oriented)
        from haitham_voice_agent.llm_router import get_router
        import json
        
        router = get_router()
        
        import re
        prompt = f"""
        [INST] You are a task extractor. Extract the actionable task from this email into JSON.
        Subject: {subject}
        Body: {body[:1000]}
        
        Return JSON object with keys: "title" (Arabic actionable title) and "priority" (high/medium).
        JSON ONLY. NO EXPLANATION.
        [/INST]
        """
        
        # Using Local Qwen via Ollama
        llm_result = await router.generate_with_local(
            prompt, 
            temperature=0.1
        )
        
        # Robust JSON parsing for local models
        content = llm_result["content"]
        try:
            # Find JSON block
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                content = match.group(0)
            task_data = json.loads(content)
        except Exception:
            # Fallback if parsing fails
            task_data = {"title": subject or "مراجعة إيميل", "priority": "medium"}
        
        # 3. Create Task
        # Note: add_task is synchronous, do not await it
        result = tasks_tool.add_task(
            title=task_data.get("title", subject),
            project_id="inbox",
            description=f"Generated from email: {subject}",
            due_date=task_data.get("due_date"),
            priority=task_data.get("priority", "medium")
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
