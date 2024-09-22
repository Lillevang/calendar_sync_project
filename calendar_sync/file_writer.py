def write_ics_file(calendar, output_file_path):
    """Writes the calendar to the specified output file."""
    with open(output_file_path, "wb") as f:
        f.write(calendar.to_ical())
