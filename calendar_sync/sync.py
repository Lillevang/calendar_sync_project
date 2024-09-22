from icalendar import Calendar
from icalendar.prop import vText
import click
from termcolor import colored


def read_calendar(file_path: str) -> Calendar:
    """Reads the ICS file and returns a Calendar object."""
    with open(file_path, "rb") as f:
        return Calendar.from_ical(f.read())


def get_events_from_calendar(calendar: Calendar) -> dict:
    """Extracts events from the calendar and returns a dictionary of events by UID."""
    events = {}
    for event in calendar.walk("VEVENT"):
        uid = str(event.get("UID"))
        events[uid] = event
    return events


def handle_event_conflicts(event, existing_event, check_conflicts) -> bool:
    """
    Handles event conflicts (rescheduled or canceled).
    Returns True if the event should be skipped due to a conflict
    """
    if event.get("DTSTART") != existing_event.get("DTSTART") or event.get(
        "DTEND"
    ) != existing_event.get("DTEND"):
        # If syncing back and the event is rescheduled in `calendar_a`, log a warning
        if check_conflicts:
            click.echo(
                colored(
                    f"Conflict: Event '{event['SUMMARY']}' \
                        was rescheduled in the original calendar.",
                    "red",
                )
            )
            return True
    if event.get("STATUS") == "CANCELLED":
        return True
    return False


def sync_ics_files(
    from_file, to_file, add_prefix=None, filter_prefix=None, check_conflicts=None
):
    """Syncs events from the source calendar to the destination calendar."""
    # Create a new calendar for the merged events
    new_cal = Calendar()
    new_cal.add("prodid", "-//Calendar Sync App//EN")
    new_cal.add("version", "2.0")

    # Read destination calendar and get events
    to_calendar = read_calendar(to_file)
    destination_events = get_events_from_calendar(to_calendar)

    # Add destination events to the new calendar
    for event in destination_events.values():
        new_cal.add_component(event)

    # Read source calendar and process events
    from_calendar = read_calendar(from_file)
    source_events = get_events_from_calendar(from_calendar)

    for uid, event in source_events.items():
        # Skip events with filter prefix
        if filter_prefix and str(event.get("SUMMARY")).startswith(filter_prefix):
            continue

        # Event already exists in the destination calendar
        if uid in destination_events:
            existing_event = destination_events[uid]
            if handle_event_conflicts(event, existing_event, check_conflicts):
                continue  # Skip due to conflict

            # Remove old event and add the updated one
            new_cal.subcomponents.remove(existing_event)
            new_cal.add_component(event)
        else:
            # Only apply the prefix to new events from `from_file`
            summary = event.get("SUMMARY")
            if isinstance(summary, vText):
                summary = str(summary)  # Convert vText to string

            if add_prefix and not summary.startswith(add_prefix):
                event["SUMMARY"] = f"{add_prefix}{summary}"
                print(f"Updated event with prefix: {event.get('SUMMARY')}")
            new_cal.add_component(event)

    return new_cal
