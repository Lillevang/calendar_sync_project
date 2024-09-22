from icalendar import Calendar


def read_ics(file_path: str):
    """Read events from an ICS file
    and return a list of (start_time, end_time, summary)."""
    with open(file_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            start = component.get("dtstart").dt
            end = component.get("dtend").dt
            summary = component.get("summary")
            events.append((start, end, summary))

    return events


def check_overlap(events_a, events_b):
    """Check if events from two calendars overlap."""
    overlaps = []
    for start_a, end_a, summary_a in events_a:
        for start_b, end_b, summary_b in events_b:
            if max(start_a, start_b) < min(end_a, end_b):  # Check for overlap
                overlaps.append((summary_a, start_a, end_a, summary_b, start_b, end_b))

    return overlaps


def validate_overlap(file_a: str, file_b: str):
    """Validate if the events in two ICS files overlap."""
    events_a = read_ics(file_a)
    events_b = read_ics(file_b)

    overlaps = check_overlap(events_a, events_b)

    if overlaps:
        print(f"Found {len(overlaps)} overlapping events:")
        for overlap in overlaps:
            print(
                f"""- {overlap[0]} ({overlap[1]} to {overlap[2]})
                overlaps with {overlap[3]} ({overlap[4]} to {overlap[5]})"""
            )
    else:
        print("No overlapping events found.")


if __name__ == "__main__":
    file_a = "../tests/test_data/calendar_a.ics"  # Path to the first ICS file
    file_b = "../tests/test_data/calendar_b.ics"  # Path to the second ICS file

    validate_overlap(file_a, file_b)
