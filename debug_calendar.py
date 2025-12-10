
import asyncio
import datetime
from haitham_voice_agent.tools.calendar import CalendarTools

async def debug_calendar():
    print("----------------------------------------------------------------")
    print("              DEBUGGING CALENDAR API RESPONSE                   ")
    print("----------------------------------------------------------------")
    
    cal = CalendarTools()
    
    # 1. Check Timezone
    now_local = datetime.datetime.now().astimezone()
    print(f"System Time (Local): {now_local}")
    print(f"System Time (UTC):   {datetime.datetime.utcnow()}")
    
    # 2. Fetch 'Today'
    print("\n[1/2] Fetching 'today' events...")
    res = await cal.list_events("today")
    print(res)
    
    if res.get("success") and res.get("count") == 0:
        print(" -> Count is 0. Trying 'tomorrow' just in case of timezone shift...")
        res_tomorrow = await cal.list_events("tomorrow")
        print(f" -> Tomorrow: {res_tomorrow}")

    # 3. List next 10 events regardless of time
    print("\n[2/2] Fetching next 10 events (raw list)...")
    try:
        service = cal.service or (cal._ensure_service() and cal.service)
        if service:
            events_result = service.events().list(
                calendarId='primary',
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            items = events_result.get('items', [])
            print(f"Found {len(items)} raw events:")
            for event in items:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f" - {start}: {event.get('summary')}")
        else:
            print("Service not available.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_calendar())
