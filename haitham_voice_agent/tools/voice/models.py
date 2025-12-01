"""
Shared Whisper Models
Holds the global model instances to avoid circular imports.
"""
import logging
from typing import Optional

try:
    from faster_whisper import WhisperModel
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False

from haitham_voice_agent.config import Config

logger = logging.getLogger(__name__)

# Global cache for Whisper model instances
WHISPER_MODELS = {
    "realtime": None,
    "session": None,
}

def init_whisper_models():
    """
    Initialize and cache Whisper models for realtime and session profiles.
    Must be called ONCE at startup.
    """
    global WHISPER_MODELS
    
    if not HAS_WHISPER:
        logger.error("faster-whisper not installed. Local STT will not work.")
        return

    try:
        for profile in ("realtime", "session"):
            model_name = Config.WHISPER_MODEL_NAMES.get(profile)
            if not model_name:
                logger.warning(f"No Whisper model configured for profile '{profile}'")
                continue

            if WHISPER_MODELS[profile] is None:
                logger.info(f"Loading Whisper model for profile '{profile}': {model_name}")
                
                try:
                    # Attempt to load the configured model
                    WHISPER_MODELS[profile] = WhisperModel(
                        model_name, 
                        device="cpu", 
                        compute_type="int8"
                    )
                    logger.info(f"Whisper model '{profile}' ({model_name}) loaded successfully")
                    
                except Exception as e:
                    # Fallback logic specifically for heavy models
                    if "large" in model_name:
                        logger.warning(f"Failed to load heavy model '{model_name}' for '{profile}'. Error: {e}")
                        logger.info("Attempting fallback to 'medium' model...")
                        try:
                            WHISPER_MODELS[profile] = WhisperModel(
                                "medium", 
                                device="cpu", 
                                compute_type="int8"
                            )
                            logger.info(f"Fallback model 'medium' loaded for '{profile}'")
                        except Exception as fallback_error:
                            logger.error(f"Fallback failed for '{profile}': {fallback_error}")
                    else:
                        logger.error(f"Failed to load model '{model_name}' for '{profile}': {e}")
                
    except Exception as e:
        logger.error(f"Failed to initialize Whisper models: {e}", exc_info=True)
