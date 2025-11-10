import requests
from icalendar import Calendar
from datetime import datetime, timedelta
import pytz
import json
import csv

ICS_URL = "https://www.truman.edu/?rhc_action=get_icalendar_events&post_type[]=events"  # Truman ICS feed
LOCAL_TZ = pytz.timezone("US/Central")           # Truman timezone (CST/CDT)
DAYS_AHEAD = 30                                  # Filter for next 30 days
JSON_FILE = "truman_events.json"
CSV_FILE = "truman_events.csv"

def get_all_events_in_30_Days():
    resp = requests.get(ICS_URL, timeout=10)
    resp.raise_for_status()
    cal = Calendar.from_ical(resp.content)

    now = datetime.now(LOCAL_TZ)
    one_month_later = now + timedelta(days=DAYS_AHEAD)

    upcoming_events = []

    for component in cal.walk():
        if component.name == "VEVENT":
            start = component.get("dtstart").dt
            end = component.get("dtend").dt if component.get("dtend") else None

            # Ensure datetime objects have timezone info
            if isinstance(start, datetime) and start.tzinfo is None:
                start = LOCAL_TZ.localize(start)
            if isinstance(end, datetime) and end.tzinfo is None:
                end = LOCAL_TZ.localize(end)

            # Filter by date window
            if isinstance(start, datetime) and now <= start <= one_month_later:
                upcoming_events.append({
                    "id": str(component.get("uid")),
                    "title": str(component.get("summary")),
                    "start": start.isoformat(),
                    "end": end.isoformat() if end else None,
                    "description": str(component.get("description") or ""),
                    "location": str(component.get("location") or "")
                })

    upcoming_events.sort(key=lambda x: x["start"])

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(upcoming_events, f, indent=2, ensure_ascii=False)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "start", "end", "description", "location"])
        writer.writeheader()
        writer.writerows(upcoming_events)

    print(f"Total upcoming events (next {DAYS_AHEAD} days): {len(upcoming_events)}")
    for e in upcoming_events[:5]:
        print(e["start"], "-", e["title"])

def get_event_details(event_id):
    url = f"https://www.truman.edu/?rhc_action=get_icalendar_events&ID={event_id}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    cal = Calendar.from_ical(resp.content)

    for component in cal.walk():
        if component.name == "VEVENT":
            event = {
                "id": str(component.get("uid")),
                "title": str(component.get("summary")),
                "start": component.get("dtstart").dt.isoformat() if component.get("dtstart") else None,
                "end": component.get("dtend").dt.isoformat() if component.get("dtend") else None,
                "description": str(component.get("description") or ""),
                "location": str(component.get("location") or ""),
                "url": str(component.get("url") or "")
            }
            return event
    return None

if __name__ == "__main__":
    get_all_events_in_30_Days()
    event = get_event_details("186443")
    print(event)

