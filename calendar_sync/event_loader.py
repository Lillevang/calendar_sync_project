from icalendar import Calendar
from datetime import datetime, timedelta, timezone


def load_events(ics_file, days):
    """
    Load events from the ICS file from today + days ahead.
    """
    with open(ics_file, "rb") as f:
        gcal = Calendar.from_ical(f.read())

    # Make 'now' timezone-aware using UTC
    now = datetime.now(timezone.utc)
    future_limit = now + timedelta(days=days)
    events = []

    for component in gcal.walk():
        if component.name == "VEVENT":
            start_time = component.get("DTSTART").dt
            end_time = component.get("DTEND").dt

            # Convert naive datetimes to UTC if necessary
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)

            # Now compare both timezone-aware datetimes
            if now <= start_time <= future_limit:
                events.append(
                    {
                        "uid": str(component.get("UID")),
                        "summary": str(component.get("SUMMARY")),
                        "start": start_time,
                        "end": end_time,
                    }
                )

    return events
