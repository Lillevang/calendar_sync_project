# calendar_sync/conflict_checker.py


def check_conflicts(file1, file2, days):
    """Stub for checking conflicts between two ICS files."""
    print(f"Checking conflicts between {file1} and {file2} for the next {days} days")
    # Return a mock conflict for testing
    return [
        (
            {
                "UID": "event-1@example.com",
                "SUMMARY": "Test Event 1",
                "start": "2024-09-20T10:00:00",
                "end": "2024-09-20T11:00:00",
            },
            {
                "UID": "event-3@example.com",
                "SUMMARY": "Test Event 3",
                "start": "2024-09-20T10:30:00",
                "end": "2024-09-20T11:30:00",
            },
        )
    ]
