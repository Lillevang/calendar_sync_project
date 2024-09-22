from typing import List, Tuple, Dict
from calendar_sync.event_loader import load_events


def check_conflicts(file1: str, file2: str, days: int) -> List[Tuple[Dict, Dict]]:
    """
    Check for conflicting events between two ICS files within the next 'days' days.

    Parameters:
    - file1 (str): Path to the first ICS file.
    - file2 (str): Path to the second ICS file.
    - days (int): Number of days to look ahead for events.

    Returns:
    - List[Tuple[Dict, Dict]]: A list of tuples, each containing two conflicting events.
    """
    events1 = load_events(file1, days)
    events2 = load_events(file2, days)

    conflicts = []

    # Create a set of event times for faster lookup
    event_times1 = {(event["start"], event["end"], event["uid"]) for event in events1}
    event_times2 = {(event["start"], event["end"], event["uid"]) for event in events2}

    # Check for overlapping or identical time events
    for start1, end1, uid1 in event_times1:
        for start2, end2, uid2 in event_times2:
            # Only consider conflicts if UIDs are different
            if uid1 != uid2:
                # Detect conflicts when time slots overlap or match exactly
                if (start1 < end2 and end1 > start2) or (
                    start1 == start2 and end1 == end2
                ):
                    # Retrieve the event details from the original list
                    event1 = next(event for event in events1 if event["uid"] == uid1)
                    event2 = next(event for event in events2 if event["uid"] == uid2)
                    conflicts.append((event1, event2))

    return conflicts
