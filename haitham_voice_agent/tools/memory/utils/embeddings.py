import logging
from typing import List
import os
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Generate embeddings for text
    """
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-3-small"  # 1536 dimensions
        
    async def generate(self, text: str) -> List[float]:
        """
        Generate embedding for text
        """
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            # Return zero vector or raise? 
            # Raising is better so we don't store bad data
            raise
