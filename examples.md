# Salary Scheduler Usage Examples

## Basic Usage Examples

### 1. One-Time Update

To run the script once and update all month references in a document:

```bash
python salary_scheduler.py --doc-id "1ABC...xyz" --run-once
```

This will:
- Update all month references (e.g., January → February, Feb → Mar)
- Exit after completion
- Log all changes made

### 2. Scheduled Monthly Update

To schedule the script to run on the first day of each month at 9 AM:

```bash
python salary_scheduler.py --doc-id "1ABC...xyz" --schedule-day 1 --schedule-time "09:00"
```

### 3. Custom Schedule with Default Time

Run on the 15th of each month at midnight (default time):

```bash
python salary_scheduler.py --doc-id "1ABC...xyz" --schedule-day 15
```

## Real-World Scenarios

### Scenario 1: Payroll Schedule Document

```bash
# Schedule updates for the last day of the month at 11 PM
python salary_scheduler.py --doc-id "your_payroll_doc_id" --schedule-day 28 --schedule-time "23:00"
```

Before update:
```
Payment Schedule:
- January payroll will be processed on January 30th
- February preliminary review on January 25th
```

After update:
```
Payment Schedule:
- February payroll will be processed on February 28th
- March preliminary review on February 25th
```

### Scenario 2: Multiple Documents Update

You can create a shell script to update multiple documents:

```bash
#!/bin/bash
# update_all_schedules.sh

# Update salary schedules
python salary_scheduler.py --doc-id "salary_doc_id" --run-once

# Update bonus schedules
python salary_scheduler.py --doc-id "bonus_doc_id" --run-once

# Update payment schedules
python salary_scheduler.py --doc-id "payment_doc_id" --run-once
```

Make it executable and run:
```bash
chmod +x update_all_schedules.sh
./update_all_schedules.sh
```

### Scenario 3: Development and Testing

For testing changes in a development environment:

```bash
# Test run with detailed logging
python -u salary_scheduler.py --doc-id "test_doc_id" --run-once 2>&1 | tee update.log
```

## Common Patterns and Tips

### 1. Running in Background

Using nohup to run in background:
```bash
nohup python salary_scheduler.py --doc-id "your_doc_id" --schedule-day 1 --schedule-time "00:00" &
```

### 2. Running with Python Virtual Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python salary_scheduler.py --doc-id "your_doc_id" --run-once
```

### 3. Running with Cron

Add to crontab to run monthly:
```bash
# Edit crontab
crontab -e

# Add line to run at 00:00 on the 1st of every month
0 0 1 * * cd /path/to/salary-scheduler && /path/to/python salary_scheduler.py --doc-id "your_doc_id" --run-once
```

## Error Handling Examples

### 1. Handling Authentication Errors

If you encounter authentication errors:
```bash
# Remove existing token and re-authenticate
rm token.pickle
python salary_scheduler.py --doc-id "your_doc_id" --run-once
```

### 2. Debugging Mode

For troubleshooting, you can modify the logging level in the script:
```python
# Change logging level to DEBUG
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

Remember to:
- Always backup important documents before running updates
- Test changes on a copy of the document first
- Keep credentials.json and token.pickle secure
- Monitor logs for any errors or unexpected behavior
