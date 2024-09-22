# Calendar Sync CLI

A CLI tool for syncing and managing calendar events between two calendars using ICS files. The tool allows you to filter events by prefix, add prefixes to event summaries, and check for conflicting events between two calendars.

## Features

- Sync events from one calendar to another using ICS files.
- Filter events based on a prefix (e.g., remove events that start with XYZ:).
- Add a prefix to events being synced to distinguish events from different calendars.
- Detect conflicting events between two calendars over a specified number of days.


## Usage

### Syncing Calendars

You can sync calendars by specifying a source calendar (from_file) and a destination calendar (to_file).

#### Example Usage:

- Sync from "Calendar A" to "Calendar B", filtering out events prefixed with `XYZ`:

```bash
calendar-sync sync --from_file path/to/calendar_a.ics --to_file path/to/calendar_b.ics --output path/to/output_calendar_b.ics --filter-prefix "XYZ:"
```

- Sync from "Calendar B" to "Calendar A", adding a prefix ClientA: to the synced events:

```bash
calendar-sync sync --from_file path/to/calendar_b.ics --to_file path/to/calendar_a.ics --output path/to/output_calendar_a.ics --add-prefix "ClientA: "
```

### Checking for conflicts

Check for conflicting events between two ICS files within the next X days:

```bash
calendar-sync check_conflicts --from_file path/to/calendar_a.ics --to_file path/to/calendar_b.ics --days 7
```

This command will output a list of conflicting events between the two calendars.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Lillevang/calendar_sync_project.git
cd calendar_sync_project
```

2. Set up a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate # On windows, use .venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements
```

### Running Tests

To run the tests for the project, use the following command:

```bash
pytest
```

Tests are located in the `tests/` directory and include test cases for syncing and conflict detection.

### Code Formatting and Linting

The project uses **Black** for code formatting and **Flake8** for linting.

#### Formatting code

To format code using **Black**, run:

```bash
black .
```

#### Linting Code

To lint the code using **Flake8**, run:

```bash
flake8
```

Make sure to address any linting errors or warnings.

### Configuration

#### Flake8

The `.flake8` configuration is located in the root of the project. It includes rules for linting and ignores certain directories like `.venv`.

#### Black

**Black** uses a default configuration with a maximum line length of 88 characters. This can be configured in the `pyproject.toml` file.

## License

This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for more details.
