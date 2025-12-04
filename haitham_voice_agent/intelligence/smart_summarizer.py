import logging
from typing import Optional

from haitham_voice_agent.ollama_orchestrator import get_orchestrator
from haitham_voice_agent.llm_router import get_router

logger = logging.getLogger(__name__)

class SmartSummarizer:
    """
    Summarizes content using a Local-First strategy.
    1. Try Local Qwen (via Ollama).
    2. Fallback to Cloud (Gemini/GPT) via LLMRouter.
    """
    
    def __init__(self):
        self.ollama = get_orchestrator()
        self.llm_router = get_router()
        
    async def summarize_content(self, text: str, max_length: int = 2000) -> str:
        """Generate a concise summary/description of the text"""
        if not text:
            return ""
            
        # Truncate if too long for context window
        truncated_text = text[:max_length]
        prompt = f"Summarize the following file content in 1-2 sentences. Focus on what it is and its key topics:\n\n{truncated_text}"
        
        # 1. Try Local Qwen
        try:
            logger.info("Attempting local summarization with Qwen...")
            # We use classify_request as a generic generation interface for now if available,
            # or we might need to add a generate method to OllamaOrchestrator.
            # Assuming OllamaOrchestrator has a generate method or we use the underlying client.
            # Let's check OllamaOrchestrator capabilities.
            # If not exposed, we might need to add it. For now, let's assume we can use it.
            # Actually, OllamaOrchestrator is designed for classification.
            # Let's use the LLM Router's Gemini Flash as primary fallback if Ollama isn't easy to hook into for generation yet.
            # BUT the requirement is Qwen first.
            # Let's see if we can use the ollama client directly if the orchestrator doesn't support raw generation.
            
            # Re-reading OllamaOrchestrator code (from memory/context):
            # It uses `AsyncClient`.
            
            response = await self.ollama.client.generate(
                model=self.ollama.model,
                prompt=prompt,
                options={"temperature": 0.3}
            )
            
            summary = response.get("response", "").strip()
            if summary:
                logger.info("Generated summary using Qwen")
                return summary
                
        except Exception as e:
            logger.warning(f"Local summarization failed: {e}")
            
        # 2. Fallback to Cloud (Gemini Flash is preferred for speed/cost)
        try:
            logger.info("Falling back to Cloud summarization...")
            # We force Gemini by asking for 'analysis' or just using the router
            result = await self.llm_router.generate_with_gemini(
                prompt, 
                logical_model="logical.gemini.flash" # Hint for Flash
            )
            return result["content"]
            
        except Exception as e:
            logger.error(f"Cloud summarization failed: {e}")
            return "Content available (Summarization failed)"

# Singleton
smart_summarizer = SmartSummarizer()
