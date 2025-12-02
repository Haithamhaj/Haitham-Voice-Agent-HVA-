from fastapi import APIRouter, HTTPException
from haitham_voice_agent.dispatcher import get_dispatcher

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/status")
async def get_system_status():
    """Get system status"""
    dispatcher = get_dispatcher()
    system_tool = dispatcher.tools.get("system")
    
    if not system_tool:
        raise HTTPException(status_code=503, detail="System tool not available")
        
    try:
        if hasattr(system_tool, "get_status"):
            status = await system_tool.get_status()
            return status
        else:
            return {"status": "online", "message": "System tool active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_system_logs(lines: int = 100):
    """Get backend logs"""
    try:
        log_file = "/tmp/hva_backend.log"
        with open(log_file, "r") as f:
            # Read all lines and return last N
            all_lines = f.readlines()
            return all_lines[-lines:]
    except FileNotFoundError:
        return ["Log file not found."]
    except Exception as e:
        return [f"Error reading logs: {str(e)}"]
