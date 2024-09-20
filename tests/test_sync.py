import os
from calendar_sync.sync import sync_ics_files, parse_ics_file
from icalendar import Calendar


def test_sync_filtering(tmp_path):
    # Load example calendar file
    input_ics_path = os.path.join("examples", "example_calendar_1.ics")
    output_ics_path = tmp_path / "output_calendar.ics"

    # Run the sync function with filtering (remove "ATP:" prefixed events)
    sync_ics_files(
        "calendar_a_to_b", input_ics_path, output_ics_path, filter_prefix="ATP:"
    )

    # Load the generated ICS file and verify the filtering
    with open(output_ics_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    # There should be only one event after filtering ("ATP:" event removed)
    events = [comp for comp in cal.walk() if comp.name == "VEVENT"]
    assert len(events) == 1
    assert events[0].get("SUMMARY") == "Test Event 1"


def test_sync_add_prefix(tmp_path):
    # Load example calendar file
    input_ics_path = os.path.join("examples", "example_calendar_1.ics")
    output_ics_path = tmp_path / "output_calendar.ics"

    # Run the sync function with prefix addition (add "ClientA:" to events)
    sync_ics_files(
        "calendar_b_to_a", input_ics_path, output_ics_path, add_prefix="ClientA: "
    )

    # Load the generated ICS file and verify the prefix was added
    with open(output_ics_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    # Verify that the prefix was added to the event summaries
    events = [comp for comp in cal.walk() if comp.name == "VEVENT"]
    assert len(events) == 2
    assert events[0].get("SUMMARY") == "ClientA: Test Event 1"
    assert events[1].get("SUMMARY") == "ClientA: ATP: Test Event 2"


def test_event_parsing():
    # Load example calendar file
    input_ics_path = os.path.join("examples", "example_calendar_1.ics")

    # Parse the ICS file
    events = parse_ics_file(input_ics_path)

    # Verify event details
    assert len(events) == 2
    assert events[0]["summary"] == "Test Event 1"
    assert events[1]["summary"] == "ATP: Test Event 2"
