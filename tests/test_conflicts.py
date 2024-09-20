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

    # There should be one conflict between event-2 and event-4
    assert len(conflicts) == 1
    assert conflicts[0][0]["uid"] == "event-2@example.com"
    assert conflicts[0][1]["uid"] == "event-4@example.com"
