from icalendar import Calendar


def sync_ics_files(
    direction, ics_file1, ics_file2=None, filter_prefix=None, add_prefix=None
):
    """
    Syncs ICS files by filtering out or adding prefixes to event titles.

    direction: The sync direction (merge_a_to_b or merge_b_to_a).
    ics_file1: Path to the first ICS file (Calendar A).
    ics_file2: Path to the second ICS file (Calendar B) if syncing two files.
    filter_prefix: If provided, events with this prefix in the title will be skipped.
    add_prefix: If provided, this prefix will be added to the title of each event.
    """
    # Read the input ICS files
    with open(ics_file1, "rb") as f1:
        cal1 = Calendar.from_ical(f1.read())

    cal2 = None
    if ics_file2:
        with open(ics_file2, "rb") as f2:
            cal2 = Calendar.from_ical(f2.read())

    # Create a new calendar for the merged/modified events
    new_cal = Calendar()
    new_cal.add("prodid", "-//Calendar Sync App//EN")
    new_cal.add("version", "2.0")

    # Track added UIDs to avoid duplicates
    added_uids = set()

    # Helper function to add an event only if its UID hasn't been added yet
    def add_event(event):
        uid = str(event.get("UID"))
        if uid not in added_uids:
            added_uids.add(uid)
            new_cal.add_component(event)

    # Process the direction, merge events between calendars or sync within a single file
    if direction == "merge_a_to_b":
        for event in cal1.walk("VEVENT"):
            if add_prefix and "SUMMARY" in event:
                event["SUMMARY"] = f"{add_prefix}{event['SUMMARY']}"
            add_event(event)  # Add event from Calendar A

        for event in cal2.walk("VEVENT"):
            if (
                filter_prefix
                and "SUMMARY" in event
                and str(event["SUMMARY"]).startswith(filter_prefix)
            ):
                continue  # Skip the event if it matches the filter prefix
            add_event(event)  # Add event from Calendar B

    elif direction == "merge_b_to_a":
        for event in cal2.walk("VEVENT"):
            if add_prefix and "SUMMARY" in event:
                event["SUMMARY"] = f"{add_prefix}{event['SUMMARY']}"
            add_event(event)  # Add event from Calendar B

        for event in cal1.walk("VEVENT"):
            if (
                filter_prefix
                and "SUMMARY" in event
                and str(event["SUMMARY"]).startswith(filter_prefix)
            ):
                continue  # Skip the event if it matches the filter prefix
            add_event(event)  # Add event from Calendar A

    else:
        # Single file sync (apply filter or prefix to one file only)
        for event in cal1.walk("VEVENT"):
            if (
                filter_prefix
                and "SUMMARY" in event
                and str(event["SUMMARY"]).startswith(filter_prefix)
            ):
                continue  # Skip events with the filter prefix

            if add_prefix and "SUMMARY" in event:
                event["SUMMARY"] = f"{add_prefix}{event['SUMMARY']}"
            add_event(event)  # Add event from Calendar A

    return new_cal


def write_ics_file(calendar, output_file):
    """Writes the Calendar object to an ICS file."""
    with open(output_file, "wb") as f:
        f.write(calendar.to_ical())
