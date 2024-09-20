from calendar_sync.event_loader import load_events


def check_conflicts(file1, file2, days):
    """
    Check for conflicts between two ICS files within the next 'days' days.

    Args:
        file1 (str): Path to the first ICS file.
        file2 (str): Path to the second ICS file.
        days (int): Number of days ahead to check for conflicts.

    Returns:
        list: A list of conflicting events.
    """
    events1 = load_events(file1, days)
    events2 = load_events(file2, days)

    conflicts = []

    # Check for overlapping events
    for event1 in events1:
        for event2 in events2:
            if event1["start"] < event2["end"] and event1["end"] > event2["start"]:
                conflicts.append((event1, event2))

    return conflicts
