import click
from calendar_sync.sync import sync_ics_files
from calendar_sync.file_writer import write_ics_file
from calendar_sync.conflict_checker import check_conflicts


@click.group()
def cli():
    """A CLI tool for syncing and managing calendar events."""
    pass


@cli.command(name="sync")
@click.option(
    "--from_file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the source ICS file (e.g., Calendar A)",
)
@click.option(
    "--to_file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the destination ICS file (e.g., Calendar B)",
)
@click.option(
    "--output",
    type=click.Path(),
    required=True,
    help="Path to the output ICS file",
)
@click.option(
    "--add-prefix",
    type=str,
    help="Prefix to add to event summaries when importing (e.g., '[Synced]')",
)
def sync(from_file, to_file, output, add_prefix):
    """
    Sync calendar events from source to destination,
    adding prefixes or replacing event summaries as needed.
    """
    click.echo(f"Syncing events from {from_file} to {to_file}")

    # Sync the two calendars, applying prefix and replace options if provided
    new_cal = sync_ics_files(from_file, to_file, add_prefix=add_prefix)

    # Write the merged/updated calendar to the output file
    write_ics_file(new_cal, output)
    click.echo(f"Synced calendar saved to {output}")


@cli.command(name="check_conflicts")
@click.option(
    "--from_file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the first ICS file (e.g., Calendar A)",
)
@click.option(
    "--to_file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the second ICS file (e.g., Calendar B)",
)
@click.option(
    "--days", type=int, default=7, help="Number of days ahead to check for conflicts"
)
def check_conflicts_cmd(from_file, to_file, days):
    """
    Check for conflicting events between two ICS files within the next X days.
    """
    click.echo(
        f"Checking conflicts between {from_file} and {to_file} for the next {days} days"
    )
    conflicts = check_conflicts(from_file, to_file, days)

    if conflicts:
        click.echo(f"Found {len(conflicts)} conflicts:")
        for event1, event2 in conflicts:
            click.echo(f"- Conflict: {event1['summary']} vs {event2['summary']}")
    else:
        click.echo("No conflicts found.")


if __name__ == "__main__":
    cli()
