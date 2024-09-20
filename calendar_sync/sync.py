from icalendar import Calendar


def sync_ics_files(
    direction, input_ics_file, output_ics_file, filter_prefix=None, add_prefix=None
):
    """Syncs ICS files by filtering out or adding prefixes to event titles."""

    # Read the input ICS file
    with open(input_ics_file, "rb") as f:
        gcal = Calendar.from_ical(f.read())

    # Create a new calendar for the filtered or modified events
    new_cal = Calendar()
    new_cal.add("prodid", "-//Calendar Sync App//EN")
    new_cal.add("version", "2.0")

    # Process events based on the direction and provided prefixes
    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get("SUMMARY")

            # Filter out events with the given filter_prefix
            if filter_prefix and summary and summary.startswith(filter_prefix):
                continue  # Skip events with the filter prefix

            # Add the add_prefix to the event's summary if required
            if add_prefix and summary:
                component["SUMMARY"] = f"{add_prefix}{summary}"

            # Add the event to the new calendar
            new_cal.add_component(component)

    # Write the filtered/modified events to the output ICS file
    with open(output_ics_file, "wb") as f:
        f.write(new_cal.to_ical())


def parse_ics_file(ics_file):
    """Stub for parsing an ICS file."""
    # Returning a mock list of events for now
    return [
        {
            "summary": "Test Event 1",
            "start": "2024-09-20T10:00:00",
            "end": "2024-09-20T11:00:00",
        },
        {
            "summary": "ATP: Test Event 2",
            "start": "2024-09-21T12:00:00",
            "end": "2024-09-21T13:00:00",
        },
    ]
