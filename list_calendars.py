
import asyncio
from haitham_voice_agent.tools.calendar import CalendarTools

async def list_calendars():
    print("----------------------------------------------------------------")
    print("              LISTING ALL GOOGLE CALENDARS                      ")
    print("----------------------------------------------------------------")
    
    cal = CalendarTools()
    service = cal.service or (cal._ensure_service() and cal.service)
    
    if not service:
        print("Error: Could not authorize service.")
        return

    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(f"ID: {calendar_list_entry['id']}")
                print(f"Summary: {calendar_list_entry['summary']}")
                print(f"Primary: {calendar_list_entry.get('primary', False)}")
                print("-" * 30)
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
    except Exception as e:
        print(f"Error listing calendars: {e}")

if __name__ == "__main__":
    asyncio.run(list_calendars())
