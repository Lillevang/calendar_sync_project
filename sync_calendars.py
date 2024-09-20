import click
from calendar_sync.sync import sync_ics_files, write_ics_file
from calendar_sync.conflict_checker import check_conflicts


@click.group()
def cli():
    """A CLI tool for syncing and managing calendar events."""
    pass


@cli.command()
@click.option(
    "--ics_file1",
    type=click.Path(exists=True),
    required=True,
    help="Path to the first ICS file (e.g., Calendar A)",
)
@click.option(
    "--ics_file2",
    type=click.Path(exists=True),
    required=False,  # Optional, only needed for two-file sync
    help="Path to the second ICS file (e.g., Calendar B)",
)
@click.option(
    "--merge",
    type=click.Choice(["merge_a_to_b", "merge_b_to_a"]),
    required=False,  # Only required if syncing two calendars
    help="Merge events between two ICS files (Calendar A to B or B to A)",
)
@click.option(
    "--output_file",
    type=click.Path(),
    required=True,
    help="Path to the output ICS file",
)
@click.option(
    "--filter-prefix", type=str, help="Prefix to filter out events (e.g., 'ATP:')"
)
@click.option("--add-prefix", type=str, help="Prefix to add to events when importing")
def sync(ics_file1, ics_file2, merge, output_file, filter_prefix, add_prefix):
    """
    Sync calendar events, filtering and adding prefixes as needed.
    If syncing between two ICS files, specify the direction with the --merge option.
    """
    if ics_file2 and not merge:
        raise click.UsageError(
            "The --merge option is required when syncing between two calendars."
        )

    if ics_file2:
        if merge == "merge_a_to_b":
            click.echo(f"Merging events from {ics_file1} into {ics_file2}")
        elif merge == "merge_b_to_a":
            click.echo(f"Merging events from {ics_file2} into {ics_file1}")
        # Sync two calendars based on the merge direction
        new_cal = sync_ics_files(merge, ics_file1, ics_file2, filter_prefix, add_prefix)
    else:
        click.echo(f"Syncing single calendar: {ics_file1}")
        # Single-file sync (just apply filter/prefix)
        new_cal = sync_ics_files(
            None, ics_file1, output_file, filter_prefix, add_prefix
        )

    # Write the merged/filtered calendar to the output file
    write_ics_file(new_cal, output_file)
    click.echo(f"Calendar saved to {output_file}")


@cli.command()
@click.option(
    "--file1",
    type=click.Path(exists=True),
    required=True,
    help="Path to the first ICS file (e.g., Calendar A)",
)
@click.option(
    "--file2",
    type=click.Path(exists=True),
    required=True,
    help="Path to the second ICS file (e.g., Calendar B)",
)
@click.option(
    "--days", type=int, default=7, help="Number of days ahead to check for conflicts"
)
def check_conflicts_cmd(file1, file2, days):
    """
    Check for conflicting events between two ICS files within the next X days.
    """
    click.echo(
        f"Checking conflicts between {file1} and {file2} for the next {days} days"
    )
    conflicts = check_conflicts(file1, file2, days)

    if conflicts:
        click.echo(f"Found {len(conflicts)} conflicts:")
        for event1, event2 in conflicts:
            click.echo(f"- Conflict: {event1['summary']} vs {event2['summary']}")
    else:
        click.echo("No conflicts found.")


if __name__ == "__main__":
    cli()
