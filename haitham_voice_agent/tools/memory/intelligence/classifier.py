import json
import logging
from typing import Dict, Any, Optional

from haitham_voice_agent.llm_router import LLMRouter
from . import prompts

logger = logging.getLogger(__name__)

class SmartClassifier:
    """
    ML/LLM-powered classifier for memory entries
    """
    
    def __init__(self):
        self.router = LLMRouter()
        
    async def classify(self, content: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Classify content using LLM
        """
        try:
            prompt = prompts.CLASSIFY_MEMORY_PROMPT.format(
                content=content[:4000],  # Truncate if too long
                context=context or "None"
            )
            
            # Use GPT for structured JSON output
            response = await self.router.generate_with_gpt(
                prompt=prompt,
                temperature=0.3
            )
            
            # Parse JSON
            if isinstance(response, str):
                # Clean up markdown code blocks if present
                clean_response = response.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_response)
            elif isinstance(response, dict):
                return response
            else:
                raise ValueError(f"Unexpected response type: {type(response)}")
                
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            # Return default fallback
            return {
                "project": "General",
                "topic": "Unclassified",
                "type": "note",
                "tags": [],
                "sentiment": "neutral",
                "importance": 3,
                "confidence": 0.0
            }
