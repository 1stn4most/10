# Service Route Scheduler

A Python script for scheduling service technician routes with constraint satisfaction.

## Overview

This script automatically assigns service jobs to technicians while respecting:
- Time windows and job durations
- Technician skill levels and job requirements
- Technician availability (weekdays only)
- Maximum of 2 jobs per technician per day
- Minimum of 1 job per technician (when possible)
- Travel time optimization within regions

## Requirements

- Python 3.7 or higher
- Required packages (install with: `pip install -r requirements.txt`):
  - pandas
  - openpyxl
  - geopy

## Input File Format

The script expects an Excel file named `Updated-SD-Route.xlsx` with two sheets:

### Sheet 1: "Service Locations"
Columns (flexible naming):
- Job ID / Job / Service
- Address / Location / Site
- Time Window / Time / Schedule (e.g., "9:00 AM - 11:00 AM")
- Duration (e.g., "90 minutes", "1.5 hours")
- Skill Level Required / Skill / Level
- Region / Area / Zone
- Special Instructions / Notes (optional)

### Sheet 2: "Technicians"
Columns (flexible naming):
- Name / Technician / Employee
- Skill Level / Skill / Expertise (e.g., "Junior", "Intermediate", "Senior")
- Availability / Schedule / Days (e.g., "Monday-Friday", "Monday,Wednesday,Friday")
- Starting Location / Base / Start Location
- Ending Location (optional)

## Usage

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Place your Excel file in the same directory as the script

3. Run the scheduler:
```bash
python route_scheduler.py
```

4. Review the output file: `Scheduled_Routes_Output.xlsx`

## Output Format

The output Excel file contains:
- One sheet per weekday (Monday - Friday) with scheduled jobs
- Each sheet shows:
  - Technician name
  - Job ID
  - Address
  - Start and end times
  - Duration
  - Special instructions
- "Unscheduled" sheet listing any jobs that could not be assigned with reasons

## Features

### Constraint Satisfaction
- ✅ Respects time windows for each job
- ✅ Matches technician skills to job requirements
- ✅ Only schedules on available days
- ✅ Prevents double-booking technicians
- ✅ Limits jobs per technician (1-2 per day)
- ✅ Balances workload across technicians

### Optimization
- Minimizes travel time by prioritizing nearby assignments
- Distributes jobs evenly across the work week
- Prioritizes technicians with fewer assignments

### Error Handling
- Validates input file structure
- Reports missing columns
- Handles various time formats
- Lists unscheduled jobs with explanations

### Adaptability
- Automatically detects column names (flexible naming)
- Works with different regions/counties
- Handles various date/time formats
- Scales to different numbers of technicians and jobs

## Example Use Cases

### Standard County Route File
The script works with the standard "Updated-SD-Route.xlsx" format out of the box.

### New County/Region
To use with a different county:
1. Ensure the Excel file has the same two-sheet structure
2. Use similar column names (the script will match them automatically)
3. Update the `INPUT_FILE` variable in the script if using a different filename

### Custom Constraints
To modify constraints (e.g., change max jobs per day):
1. Edit the constants at the top of `route_scheduler.py`:
   - `MAX_JOBS_PER_DAY` (default: 2)
   - `MIN_JOBS_PER_DAY` (default: 1)

## Sample Data

A sample data generator is included (`create_sample_data.py`) for testing:
```bash
python create_sample_data.py
```

This creates a sample `Updated-SD-Route.xlsx` file with test data.

## Troubleshooting

### "File not found" error
- Ensure the Excel file is in the same directory as the script
- Check the filename matches exactly (default: "Updated-SD-Route.xlsx")

### "Missing columns" warning
- The script will try to match column names flexibly
- Ensure your sheets contain the required information
- Column names can vary (e.g., "Job ID", "Job", or "Service" all work)

### Jobs showing as unscheduled
Common reasons:
- No technician with required skill level available
- Time conflicts with other jobs
- All technicians at max capacity for that day
- Technician not available on required days

## Code Structure

The script is organized into clear functions:
- `load_data()` - Reads Excel file
- `validate_data()` - Checks data structure
- `schedule_jobs()` - Main scheduling algorithm
- `create_output_tables()` - Formats results
- `save_output()` - Writes Excel file

Each function includes detailed comments explaining the logic.

## Support

For issues or questions:
1. Check that input file format matches requirements
2. Review console output for specific error messages
3. Verify all required packages are installed
4. Check sample data works with your setup

## License

This script is provided as-is for service route scheduling purposes.
