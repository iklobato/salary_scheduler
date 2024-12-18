# Salary Scheduler

A Python script that automatically updates month references in Google Docs documents. This tool is particularly useful for maintaining salary schedules or other documents that need regular month updates.

## Features

- Automatically updates both full month names and three-letter abbreviations (e.g., "January"/"Jan")
- Supports scheduled monthly updates or one-time execution
- Configurable run time and date
- Google Docs API integration with secure authentication
- Comprehensive logging
- Command-line interface for flexible usage

## Prerequisites

- Python 3.x
- Google Cloud Project with Google Docs API enabled
- OAuth 2.0 credentials from Google Cloud Console

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd salary-scheduler
```

2. Install required dependencies:
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dateutil schedule
```

3. Set up Google Cloud credentials:
   - Create a project in Google Cloud Console
   - Enable the Google Docs API
   - Create OAuth 2.0 credentials
   - Download the credentials and save as `credentials.json` in the project directory

## Usage

### Command Line Arguments

- `--doc-id`: (Required) The Google Document ID to update
- `--run-once`: Run the script once and exit
- `--schedule-day`: Day of the month to run the scheduler (default: 15)
- `--schedule-time`: Time to run the scheduler in HH:MM format (default: "00:00")

### Examples

Run once:
```bash
python salary_scheduler.py --doc-id YOUR_DOCUMENT_ID --run-once
```

Run scheduled:
```bash
python salary_scheduler.py --doc-id YOUR_DOCUMENT_ID --schedule-day 1 --schedule-time "09:00"
```

## How It Works

1. The script authenticates with Google Docs API using OAuth 2.0
2. Determines the current month and the next two months
3. Creates a mapping of current/next month names (both full and abbreviated)
4. Searches the document for month references
5. Replaces all found instances with the corresponding next month
6. Logs the changes and any potential errors

## Authentication Flow

1. Checks for existing token in `token.pickle`
2. If no token exists or it's expired:
   - Uses credentials.json to start OAuth 2.0 flow
   - Opens browser for user authentication
   - Saves new token for future use

## Error Handling

- Comprehensive logging of all operations
- Graceful handling of API errors
- Token refresh automation
- Failed updates are logged with error details

## Scheduling

- Can be run as a one-time update or scheduled monthly
- Configurable run date and time
- Runs checks hourly when in scheduled mode
- Uses the `schedule` library for reliable timing

## Best Practices

1. Keep `credentials.json` and `token.pickle` secure and never commit them to version control
2. Run initial tests with `--run-once` flag to verify correct document access and updates
3. Monitor logs for any potential errors or issues
4. Ensure the service account has appropriate access to the Google Doc

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]
