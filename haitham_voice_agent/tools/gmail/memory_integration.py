import logging
from typing import Optional, Dict, Any

from haitham_voice_agent.tools.gmail.gmail_api_handler import GmailAPIHandler
from haitham_voice_agent.tools.memory.memory_system import MemorySystem
from haitham_voice_agent.tools.memory.models.memory import MemorySource

logger = logging.getLogger(__name__)

class GmailMemoryBridge:
    """
    Bridge between Gmail Module and Memory Module.
    Allows saving emails as structured memories.
    """
    
    def __init__(self):
        self.gmail_handler = GmailAPIHandler()
        self.memory_system = MemorySystem()
        
    async def initialize(self):
        """Initialize both systems"""
        # Gmail handler doesn't need explicit async init, but Memory does
        await self.memory_system.initialize()
        
    async def save_email_to_memory(self, email_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch an email and save it to the Memory System.
        
        Args:
            email_id: The Gmail message ID
            
        Returns:
            Dict with memory details if successful, None otherwise
        """
        try:
            # 1. Fetch Email
            logger.info(f"Fetching email {email_id}...")
            email = self.gmail_handler.get_email_by_id(email_id)
            if not email:
                logger.error(f"Email {email_id} not found")
                return None
                
            # 2. Prepare Content
            # Combine subject and body for context
            content = f"Subject: {email['subject']}\n\n{email['body_text']}"
            
            # Context includes sender and date
            context = f"Email from {email['from']} received on {email['date']}"
            
            # 3. Save to Memory
            logger.info("Processing and saving to memory...")
            memory = await self.memory_system.add_memory(
                content=content,
                source=MemorySource.EMAIL,
                context=context
            )
            
            if memory:
                logger.info(f"Email saved as memory {memory.id}")
                return {
                    "success": True,
                    "memory_id": memory.id,
                    "project": memory.project,
                    "summary": memory.ultra_brief
                }
            else:
                logger.error("Failed to save memory")
                return None
                
        except Exception as e:
            logger.error(f"Failed to bridge email to memory: {e}")
            return None
