
import logging
import sys
from haitham_voice_agent.tools.gmail.auth.credentials_store import get_credential_store
from haitham_voice_agent.tools.gmail.auth.oauth_flow import get_oauth_flow
from haitham_voice_agent.tools.calendar import CalendarTools

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("reauth")

def reauth():
    print("----------------------------------------------------------------")
    print("              HVA GOOGLE SERVICES RE-AUTHENTICATION             ")
    print("----------------------------------------------------------------")
    
    store = get_credential_store()
    
    # 1. Clear existing credentials
    print("\n[1/3] Clearing old credentials...")
    services = ["gmail_oauth", "calendar_oauth"]
    for service in services:
        if store.has_credential(service):
            store.delete_credential(service)
            print(f"  - Deleted {service}")
        else:
            print(f"  - No existing credential for {service}")
            
    # 2. Authenticate Gmail
    print("\n[2/3] Authenticating Gmail...")
    print("  > A browser window should open. Please sign in with your Google account.")
    print("  > If it does not open, check the console for a URL.")
    
    gmail_flow = get_oauth_flow()
    creds = gmail_flow.authorize()
    
    if creds:
        print("  ✓ Gmail Authentication Successful!")
    else:
        print("  ✗ Gmail Authentication Failed.")
        
    # 3. Authenticate Calendar
    print("\n[3/3] Authenticating Calendar...")
    print("  > A browser window should open. Please sign in again (for Calendar permissions).")
    
    cal_tool = CalendarTools()
    result = cal_tool.authorize()
    
    if result.get("success"):
        print("  ✓ Calendar Authentication Successful!")
    else:
        print(f"  ✗ Calendar Authentication Failed: {result.get('message')}")
        
    print("\n----------------------------------------------------------------")
    print("                        PROCESS COMPLETE                        ")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    reauth()
