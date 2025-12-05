import asyncio
import logging
from haitham_voice_agent.tools.files import FileTools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CleanupTrigger")

async def main():
    logger.info("🚀 Triggering Downloads Cleanup...")
    ft = FileTools()
    # Using 0 hours to force cleanup of ALL files as requested ("empty")
    # But let's stick to 72h first to be safe, unless user insists on "empty".
    # User said "tafreegh" (empty), so I will use a very low threshold (e.g. 0 or 1 hour)
    # to move almost everything, but keep very recent downloads (last hour).
    # Actually, let's use 0 to be true to "empty".
    report = await ft.cleanup_downloads(hours=0)
    logger.info(f"✅ Cleanup Complete! Report: {report}")

if __name__ == "__main__":
    asyncio.run(main())
