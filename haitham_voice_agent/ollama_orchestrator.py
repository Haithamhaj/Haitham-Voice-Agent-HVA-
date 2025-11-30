"""
Ollama Orchestrator Module
Acts as a middleware layer to route requests between local Ollama and cloud LLMs.
"""

import json
import logging
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List

from .config import Config

logger = logging.getLogger(__name__)

class OllamaOrchestrator:
    """
    Orchestrates requests using a local Ollama model for initial understanding
    and simple tasks, routing complex ones to GPT/Gemini.
    """
    
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.OLLAMA_MODEL
        self.system_prompt = """
You are a smart assistant named "Haitham". Your job is to understand user requests and route them correctly.

Classification rules:

1. Answer directly (yourself) if the request is:
- Normal conversation (greeting, thanks, goodbye)
- General question needing explanation or information
- Simple direct command (open folder, show files)
- Simple calculation
- Does NOT contain the keywords below

2. Route to GPT if the request contains:
- "plan" or Arabic equivalents
- "execute" or Arabic equivalents
- "email" or Arabic equivalents
- "memory" or "save" or "remember" or Arabic equivalents
- "json"
- Multi-step tasks needing planning

3. Route to Gemini if the request contains:
- "pdf" or attached file
- "translate" or Arabic equivalents
- "summarize" or Arabic equivalents
- "analyze" or Arabic equivalents
- "image" or Arabic equivalents

Response format (JSON ONLY):

If you will answer directly:
{"type": "direct_response", "response": "your answer here"}

If simple command to execute:
{"type": "execute_command", "intent": "intent_name", "parameters": {...}}

If routing to GPT:
{"type": "delegate", "delegate_to": "gpt", "reason": "reason", "keywords": ["keywords"]}

If routing to Gemini:
{"type": "delegate", "delegate_to": "gemini", "reason": "reason", "keywords": ["keywords"]}

Notes:
- Answer in Arabic for Arabic questions
- Answer in English for English questions
- Be concise and helpful
"""

    async def classify_request(self, user_input: str) -> Dict[str, Any]:
        """
        Classify the user request using local Ollama model.
        """
        logger.info(f"Orchestrating request: {user_input}")
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.1  # Low temp for classification
                    }
                }
                
                async with session.post(f"{self.base_url}/api/chat", json=payload) as response:
                    if response.status != 200:
                        logger.error(f"Ollama API error: {response.status}")
                        return {"type": "delegate", "delegate_to": "gpt", "reason": "ollama_error"}
                        
                    result = await response.json()
                    content = result.get("message", {}).get("content", "")
                    
                    try:
                        classification = json.loads(content)
                        logger.info(f"Ollama classification: {classification['type']}")
                        return classification
                    except json.JSONDecodeError:
                        logger.error("Failed to parse Ollama JSON response")
                        return {"type": "delegate", "delegate_to": "gpt", "reason": "json_parse_error"}
                        
        except Exception as e:
            logger.error(f"Ollama connection failed: {e}")
            # Fallback to GPT if Ollama is down
            return {"type": "delegate", "delegate_to": "gpt", "reason": "connection_failed"}

# Singleton instance
_orchestrator_instance: Optional[OllamaOrchestrator] = None

def get_orchestrator() -> OllamaOrchestrator:
    """Get singleton orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = OllamaOrchestrator()
    return _orchestrator_instance
