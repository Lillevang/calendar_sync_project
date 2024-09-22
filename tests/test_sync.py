from unittest.mock import patch, MagicMock
from calendar_sync.sync import (
    sync_ics_files,
    get_events_from_calendar,
    handle_event_conflicts,
)
from icalendar import Calendar, Event


def test_get_events_from_calendar():
    """Test that events are correctly extracted from a calendar."""
    cal = Calendar()
    event = Event()
    event.add("UID", "12345")
    cal.add_component(event)

    events = get_events_from_calendar(cal)
    assert len(events) == 1
    assert "12345" in events


def test_sync_ics_files():
    """Test the main sync logic."""
    mock_from_cal = Calendar()
    mock_to_cal = Calendar()

    event_a = Event()
    event_a.add("UID", "event-1")
    event_a.add("SUMMARY", "Event A")
    mock_from_cal.add_component(event_a)

    event_b = Event()
    event_b.add("UID", "event-2")
    event_b.add("SUMMARY", "Event B")
    mock_to_cal.add_component(event_b)

    # Mock read_calendar to return the mocked calendars
    with patch("calendar_sync.sync.read_calendar") as mock_read_calendar:
        mock_read_calendar.side_effect = [mock_from_cal, mock_to_cal]

        # Perform the sync
        new_cal = sync_ics_files("mock_from.ics", "mock_to.ics", add_prefix="[Synced]")

        # Debugging: Convert vText to string for proper comparison in the test
        event_summaries = [
            str(event.get("SUMMARY")) for event in new_cal.walk("VEVENT")
        ]
        print(f"Event summaries after sync: {event_summaries}")

        # Verify the merged calendar contains both events,
        # but only applies the prefix to `from_file` events
        assert (
            "[Synced]Event B" in event_summaries
        ), "Expected '[Synced]Event B' not found"
        assert (
            "Event A" in event_summaries
        ), "Expected 'Event A' not found (no prefix should be applied)"


def test_handle_event_conflicts_no_conflict():
    """Test conflict handling when there are no conflicts."""
    event = MagicMock()
    event.get.return_value = "2024-09-25 10:00"

    existing_event = MagicMock()
    existing_event.get.return_value = "2024-09-25 10:00"

    result = handle_event_conflicts(event, existing_event, check_conflicts=False)
    assert result is False  # No conflict, should not skip


def test_handle_event_conflicts_rescheduled():
    """Test conflict handling for a rescheduled event."""
    event = MagicMock()
    event.get.side_effect = ["2024-09-25 10:00", "2024-09-25 11:00"]

    existing_event = MagicMock()
    existing_event.get.side_effect = ["2024-09-26 10:00", "2024-09-26 11:00"]

    result = handle_event_conflicts(event, existing_event, check_conflicts=True)
    assert result is True  # Conflict, should skip
