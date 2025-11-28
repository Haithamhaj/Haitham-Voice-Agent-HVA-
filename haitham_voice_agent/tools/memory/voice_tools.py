import logging
from typing import Optional, Dict, Any

from haitham_voice_agent.tools.memory.memory_system import MemorySystem
from haitham_voice_agent.tools.memory.models.memory import MemorySource

logger = logging.getLogger(__name__)

class VoiceMemoryTools:
    """
    High-level voice tools for Memory interaction.
    """
    
    def __init__(self):
        self.memory_system = MemorySystem()
        self._initialized = False
        
    async def ensure_initialized(self):
        if not self._initialized:
            await self.memory_system.initialize()
            self._initialized = True
            
    async def process_voice_note(self, audio_text: str) -> Dict[str, Any]:
        """
        Process a raw voice note and save it as a memory.
        
        Args:
            audio_text: The transcribed text from STT
            
        Returns:
            Dict with result details
        """
        try:
            await self.ensure_initialized()
            
            logger.info(f"Processing voice note: {audio_text[:50]}...")
            
            # Save to memory
            memory = await self.memory_system.add_memory(
                content=audio_text,
                source=MemorySource.VOICE,
                context="Voice Note"
            )
            
            if memory:
                return {
                    "success": True,
                    "message": f"Saved to {memory.project}",
                    "memory_id": memory.id,
                    "summary": memory.ultra_brief
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to save memory"
                }
                
        except Exception as e:
            logger.error(f"Voice memory processing failed: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    async def search_memory_voice(self, query_text: str) -> str:
        """
        Search memories via voice and return a spoken response.
        
        Args:
            query_text: The search query
            
        Returns:
            str: The response text to be spoken
        """
        try:
            await self.ensure_initialized()
            
            results = await self.memory_system.search_memories(query_text, limit=3)
            
            if not results:
                return "I couldn't find any relevant memories."
            
            # Format response
            response = f"I found {len(results)} relevant items. "
            
            # Top result details
            top = results[0]
            response += f"The most relevant is from {top.project}: {top.ultra_brief}. "
            
            if len(results) > 1:
                response += "I also found related notes about " + \
                           ", ".join([r.topic for r in results[1:]]) + "."
                           
            return response
            
        except Exception as e:
            logger.error(f"Voice search failed: {e}")
            return "I encountered an error while searching your memories."
