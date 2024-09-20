from icalendar import Calendar


def sync_ics_files(
    direction, input_ics_file, output_ics_file, filter_prefix=None, add_prefix=None
):
    """
    Syncs ICS files by filtering out or adding prefixes to event titles.

    direction: The sync direction (calendar_a_to_b or calendar_b_to_a).
    input_ics_file: Path to the input ICS file.
    output_ics_file: Path to the output ICS file.
    filter_prefix: If provided, events with this prefix in the title will be skipped.
    add_prefix: If provided, this prefix will be added to the title of each event.
    """
    # Read the input ICS file
    with open(input_ics_file, "rb") as f:
        gcal = Calendar.from_ical(f.read())

    # Create a new calendar for the filtered/modified events
    new_cal = Calendar()
    new_cal.add("prodid", "-//Calendar Sync App//EN")
    new_cal.add("version", "2.0")

    # Process events based on the direction and provided prefixes
    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = str(component.get("SUMMARY"))
            print(f"Processing event summary: {summary}")  # Debugging output

            # Filter out events with the given filter_prefix
            if filter_prefix and summary and summary.startswith(filter_prefix):
                print(f"Skipping event: {summary}")  # Debugging output
                continue  # Skip events with the filter prefix

            # Add the add_prefix to the event's summary if required
            if add_prefix and summary:
                component["SUMMARY"] = f"{add_prefix}{summary}"
                print(
                    f"Updated event summary with prefix: {component['SUMMARY']}"
                )  # Debugging output

            # Add the event to the new calendar ONLY if it passed filtering
            new_cal.add_component(component)

    # Write the filtered/modified events to the output ICS file
    with open(output_ics_file, "wb") as f:
        f.write(new_cal.to_ical())
