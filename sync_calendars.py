import click
from calendar_sync.sync import sync_ics_files
from calendar_sync.conflict_checker import check_conflicts


@click.group()
def cli():
    """A CLI tool for syncing and managing calendar events between two calendars."""
    pass


@cli.command()
@click.option(
    "--direction",
    type=click.Choice(["calendar_a_to_b", "calendar_b_to_a"]),
    required=True,
    help="Direction to sync calendars",
)
@click.option(
    "--ics_file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the ICS file to sync",
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
def sync(direction, ics_file, output_file, filter_prefix, add_prefix):
    """
    Sync calendar events between two calendars, filtering and adding prefixes as needed.
    """
    click.echo(f"Syncing {direction} using {ics_file}")
    sync_ics_files(direction, ics_file, output_file, filter_prefix, add_prefix)


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
    check_conflicts(file1, file2, days)


if __name__ == "__main__":
    cli()
