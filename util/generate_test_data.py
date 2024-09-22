import sys
from typing import List
from datetime import datetime, timedelta
from icalendar import Event, Calendar
import random
import os


def create_event(summary, start_time, end_time, uid):
    """Helper function to create an event."""
    event = Event()
    event.add("summary", summary)
    event.add("dtstart", start_time)
    event.add("dtend", end_time)
    event.add("dtstamp", datetime.now())
    event.add("uid", uid)
    return event


def create_test_ics(file_name: str, events: List[Event]):
    """Write a list of events to an ICS file in the ../tests/test_data directory."""
    # Define the relative directory path
    directory = "../tests/test_data"

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Full file path including the directory
    file_path = os.path.join(directory, file_name)

    # Create the calendar and add events
    cal = Calendar()
    for event in events:
        cal.add_component(event)

    # Ensure unique filename if a file already exists
    base_name, ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base_name}_{counter}{ext}"
        counter += 1

    # Write the calendar to the file
    with open(file_path, "wb") as f:
        f.write(cal.to_ical())

    print(f"Created ICS file: {file_path}")


def generate_events(
    num_events: int, start_time: datetime, overlap: bool, shared_uids: List[str] = None
):
    """Generate a list of events with optional overlap and some shared UIDs."""
    events = []

    for i in range(num_events):
        event_start = start_time + timedelta(hours=i)
        event_end = event_start + timedelta(hours=1)
        summary = f"Event {i + 1}"

        # Use a shared UID for specific events (for testing rescheduled events)
        if shared_uids and i < len(shared_uids):
            uid = shared_uids[i]
        else:
            uid = f"event-{random.randint(1000, 9999)}@example.com"

        event = create_event(summary, event_start, event_end, uid)
        events.append(event)

    return events


def generate_overlapping_events(events_a: List[Event], shared_uids: List[str]):
    """Generate overlapping events for a second calendar."""
    overlapping_events = []

    for event in events_a:
        event_start = event["dtstart"].dt
        event_end = event["dtend"].dt

        # Create an overlapping event that starts before or after the original event
        overlap_start = event_start - timedelta(
            minutes=random.randint(10, 45)
        )  # Overlaps from before
        overlap_end = event_end + timedelta(
            minutes=random.randint(10, 45)
        )  # Extends beyond

        overlap_summary = f"Overlapping Event with {event['summary']}"
        if event["uid"] in shared_uids:
            overlap_uid = event["uid"]
        else:
            overlap_uid = f"event-{random.randint(1000, 9999)}@example.com"
        overlapping_event = create_event(
            overlap_summary, overlap_start, overlap_end, overlap_uid
        )

        overlapping_events.append(overlapping_event)

    return overlapping_events


def generate_ics_files(num_events: int, overlap: bool = False, same_uid: bool = False):
    """Generate two ICS files with specified options."""
    if num_events <= 0:
        print("No events to generate. Please provide a positive number of events.")
        return

    # First calendar: events generated from the base time
    start_time_a = datetime.now() + timedelta(days=1)
    events_a = generate_events(num_events, start_time_a, overlap)

    shared_uids = []

    # If same_uid is enabled, generate shared UIDs for a random subset of events
    if same_uid:
        shared_uids = [
            event["uid"]
            for event in random.sample(events_a, k=random.randint(1, num_events))
        ]

    # Second calendar: events generated with a random
    # time offset unless overlapping is specified
    if overlap:
        events_b = generate_overlapping_events(events_a, shared_uids)
    else:
        # Apply a random offset to make sure
        # events are not at exactly the same time as in calendar A
        random_offset = timedelta(
            days=random.randint(1, 10)
        )  # Random time offset between 5 and 60 minutes
        start_time_b = start_time_a + random_offset
        events_b = generate_events(num_events, start_time_b, overlap, shared_uids)

    create_test_ics("calendar_a.ics", events_a)
    create_test_ics("calendar_b.ics", events_b)

    print(
        f"""Generated {num_events} events for each calendar.
         Overlap: {overlap}, Same UID: {same_uid}"""
    )
    if same_uid:
        print(f"Number of events with the same UID: {len(shared_uids)}")


def main():
    # Parse arguments from sys.argv
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_test_data.py <num_events> [--overlap] [--same-uid]"
        )
        sys.exit(1)

    num_events = int(sys.argv[1])
    overlap = "--overlap" in sys.argv
    same_uid = "--same-uid" in sys.argv

    generate_ics_files(num_events, overlap=overlap, same_uid=same_uid)


if __name__ == "__main__":
    main()
