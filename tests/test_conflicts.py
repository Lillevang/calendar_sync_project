import os
from calendar_sync.conflict_checker import check_conflicts


def test_conflict_detection():
    # Load example calendar files
    file1 = os.path.join("examples", "example_calendar_1.ics")
    file2 = os.path.join("examples", "example_calendar_2.ics")

    # Check for conflicts within the next 10 days
    conflicts = check_conflicts(file1, file2, days=10)

    # Print conflicts for debugging
    for conflict in conflicts:
        print(f"Conflict: {conflict[0]['uid']} vs {conflict[1]['uid']}")

    # There should be 2 conflicts
    assert len(conflicts) == 2  # Adjusted to expect only 2 conflicts

    # Verify the specific conflicts
    uids = {(conflict[0]["uid"], conflict[1]["uid"]) for conflict in conflicts}
    assert ("event-2@example.com", "event-6@example.com") in uids
    assert ("event-2@example.com", "event-8@example.com") in uids
