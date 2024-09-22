import pytest
from unittest.mock import patch
from calendar_sync.conflict_checker import check_conflicts

# Sample event data for testing
mock_events_file1 = [
    {"start": "2024-09-25 10:00", "end": "2024-09-25 11:00", "uid": "event-1"},
    {"start": "2024-09-25 12:00", "end": "2024-09-25 13:00", "uid": "event-2"},
]

mock_events_file2 = [
    {
        "start": "2024-09-25 10:30",
        "end": "2024-09-25 11:30",
        "uid": "event-3",
    },  # Partial overlap with event-1
    {
        "start": "2024-09-25 12:00",
        "end": "2024-09-25 13:00",
        "uid": "event-4",
    },  # Exact match with event-2
]


@pytest.fixture
def mock_load_events():
    """Fixture to mock load_events function."""
    with patch("calendar_sync.conflict_checker.load_events") as mock_load:
        yield mock_load


def test_check_conflicts_with_overlap(mock_load_events):
    """Test that check_conflicts detects overlapping and exact match events."""

    # Mock the load_events function to return predefined events
    mock_load_events.side_effect = [mock_events_file1, mock_events_file2]

    # Call the function under test
    result = check_conflicts("calendar_a.ics", "calendar_b.ics", days=7)

    # Sort the result by UID for consistent comparison
    result = sorted(result, key=lambda x: x[0]["uid"])  # Sort by the first event's UID

    # Debugging output
    print(f"Conflicts found: {result}")

    # Assert that two conflicts are found (one partial overlap and one exact match)
    assert len(result) == 2, f"Expected 2 conflicts, but got {len(result)}"

    # Verify the partial overlap conflict
    assert (
        result[0][0]["uid"] == "event-1"
    ), f"Expected 'event-1', but got {result[0][0]['uid']}"  # Event from file1
    assert (
        result[0][1]["uid"] == "event-3"
    ), f"Expected 'event-3', but got {result[0][1]['uid']}"  # Event from file2

    # Verify the exact match conflict
    assert (
        result[1][0]["uid"] == "event-2"
    ), f"Expected 'event-2', but got {result[1][0]['uid']}"  # Event from file1
    assert (
        result[1][1]["uid"] == "event-4"
    ), f"Expected 'event-4', but got {result[1][1]['uid']}"  # Event from file2


def test_check_conflicts_no_overlap(mock_load_events):
    """Test that check_conflicts detects no conflicts when events don't overlap."""

    # Modify events to ensure no overlap
    mock_events_file2_no_overlap = [
        {"start": "2024-09-25 13:30", "end": "2024-09-25 14:30", "uid": "event-3"},
        {"start": "2024-09-25 15:00", "end": "2024-09-25 16:00", "uid": "event-4"},
    ]

    # Mock the load_events function to return non-overlapping events
    mock_load_events.side_effect = [mock_events_file1, mock_events_file2_no_overlap]

    # Call the function under test
    result = check_conflicts("calendar_a.ics", "calendar_b.ics", days=7)

    # Debugging output
    print(f"Conflicts found: {result}")

    # Assert that no conflicts are found
    assert len(result) == 0, f"Expected no conflicts, but got {len(result)}"


def test_check_conflicts_same_events(mock_load_events):
    """Test that check_conflicts ignores identical events
    (same UID, start, and end times)."""

    # Modify the second event set to be identical to the first
    mock_events_file2_same = mock_events_file1

    # Mock the load_events function to return identical events
    mock_load_events.side_effect = [mock_events_file1, mock_events_file2_same]

    # Call the function under test
    result = check_conflicts("calendar_a.ics", "calendar_b.ics", days=7)

    # Debugging output
    print(f"Conflicts found: {result}")

    # Assert that no conflicts are found
    # (identical events should not be considered conflicts)
    assert len(result) == 0, f"Expected no conflicts, but got {len(result)}"
