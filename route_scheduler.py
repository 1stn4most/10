"""
Service Route Scheduler
A Python script for scheduling service technician routes with constraint satisfaction.
Designed to work with Excel files containing service locations and technician information.
"""

import pandas as pd
from datetime import datetime, timedelta
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')

# Configuration - File paths
INPUT_FILE = "Updated-SD-Route.xlsx"
OUTPUT_FILE = "Scheduled_Routes_Output.xlsx"

# Constants
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
MAX_JOBS_PER_DAY = 2
MIN_JOBS_PER_DAY = 1


def load_data(file_path):
    """
    Load service locations and technician data from Excel file.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        tuple: (service_locations_df, technicians_df)
    """
    try:
        print(f"Loading data from {file_path}...")
        
        # Read both sheets
        service_locations = pd.read_excel(file_path, sheet_name='Service Locations')
        technicians = pd.read_excel(file_path, sheet_name='Technicians')
        
        print(f"Loaded {len(service_locations)} service locations")
        print(f"Loaded {len(technicians)} technicians")
        
        return service_locations, technicians
    
    except FileNotFoundError:
        print(f"ERROR: File '{file_path}' not found.")
        print("Please ensure the Excel file is in the same directory as this script.")
        raise
    except Exception as e:
        print(f"ERROR loading data: {str(e)}")
        raise


def validate_data(service_locations, technicians):
    """
    Validate that required columns exist in the dataframes.
    
    Args:
        service_locations: DataFrame with service location data
        technicians: DataFrame with technician data
    """
    print("\nValidating data structure...")
    
    # Expected columns for service locations (flexible matching)
    required_service_cols = ['job', 'address', 'time', 'duration', 'skill', 'region']
    # Expected columns for technicians (flexible matching)
    required_tech_cols = ['name', 'skill', 'availability', 'location']
    
    # Check service locations columns
    service_cols_lower = [col.lower() for col in service_locations.columns]
    for req_col in required_service_cols:
        matches = [col for col in service_cols_lower if req_col in col]
        if not matches:
            print(f"WARNING: Could not find column matching '{req_col}' in Service Locations")
    
    # Check technicians columns
    tech_cols_lower = [col.lower() for col in technicians.columns]
    for req_col in required_tech_cols:
        matches = [col for col in tech_cols_lower if req_col in col]
        if not matches:
            print(f"WARNING: Could not find column matching '{req_col}' in Technicians")
    
    print("Data validation complete.")


def parse_time_window(time_str):
    """
    Parse time window string into start and end times.
    Handles formats like "9:00 AM - 11:00 AM" or "9-11" or "9:00-11:00"
    
    Args:
        time_str: String representing time window
        
    Returns:
        tuple: (start_time, end_time) as datetime.time objects
    """
    try:
        if pd.isna(time_str):
            # Default to business hours if no time specified
            return datetime.strptime("09:00", "%H:%M").time(), datetime.strptime("17:00", "%H:%M").time()
        
        time_str = str(time_str).strip()
        
        # Handle various formats
        if '-' in time_str:
            parts = time_str.split('-')
            start_str = parts[0].strip()
            end_str = parts[1].strip()
            
            # Parse start time
            if 'AM' in start_str.upper() or 'PM' in start_str.upper():
                start_time = datetime.strptime(start_str, "%I:%M %p").time()
            elif ':' in start_str:
                start_time = datetime.strptime(start_str, "%H:%M").time()
            else:
                start_time = datetime.strptime(start_str + ":00", "%H:%M").time()
            
            # Parse end time
            if 'AM' in end_str.upper() or 'PM' in end_str.upper():
                end_time = datetime.strptime(end_str, "%I:%M %p").time()
            elif ':' in end_str:
                end_time = datetime.strptime(end_str, "%H:%M").time()
            else:
                end_time = datetime.strptime(end_str + ":00", "%H:%M").time()
            
            return start_time, end_time
        else:
            # Single time specified, use as start with 2 hour window
            if 'AM' in time_str.upper() or 'PM' in time_str.upper():
                start_time = datetime.strptime(time_str, "%I:%M %p").time()
            else:
                start_time = datetime.strptime(time_str + ":00", "%H:%M").time()
            
            # Add 2 hours for end time
            start_dt = datetime.combine(datetime.today(), start_time)
            end_dt = start_dt + timedelta(hours=2)
            return start_time, end_dt.time()
            
    except Exception as e:
        print(f"WARNING: Could not parse time '{time_str}': {e}")
        # Return default business hours
        return datetime.strptime("09:00", "%H:%M").time(), datetime.strptime("17:00", "%H:%M").time()


def parse_duration(duration_str):
    """
    Parse duration string into minutes.
    Handles formats like "2 hours", "90 minutes", "1.5 hrs", "90 min"
    
    Args:
        duration_str: String or number representing duration
        
    Returns:
        int: Duration in minutes
    """
    try:
        if pd.isna(duration_str):
            return 60  # Default 1 hour
        
        duration_str = str(duration_str).lower().strip()
        
        # If it's just a number, assume minutes
        if duration_str.replace('.', '').replace(',', '').isdigit():
            return int(float(duration_str.replace(',', '')))
        
        # Extract number from string
        import re
        numbers = re.findall(r'\d+\.?\d*', duration_str)
        if not numbers:
            return 60  # Default
        
        value = float(numbers[0])
        
        # Check units
        if 'hour' in duration_str or 'hr' in duration_str:
            return int(value * 60)
        else:  # Assume minutes
            return int(value)
            
    except Exception as e:
        print(f"WARNING: Could not parse duration '{duration_str}': {e}")
        return 60  # Default 1 hour


def calculate_distance(loc1, loc2):
    """
    Calculate distance between two locations.
    
    Args:
        loc1: Tuple of (latitude, longitude) or address string
        loc2: Tuple of (latitude, longitude) or address string
        
    Returns:
        float: Distance in miles (estimated if addresses not geocoded)
    """
    # For simplicity, return estimated distance based on address comparison
    # In production, would use geocoding service
    if isinstance(loc1, str) and isinstance(loc2, str):
        if loc1.lower() == loc2.lower():
            return 0.0
        # Estimate based on string similarity
        return 10.0  # Default estimate
    
    # If coordinates provided
    try:
        return geodesic(loc1, loc2).miles
    except:
        return 10.0  # Default estimate


def estimate_travel_time(distance_miles):
    """
    Estimate travel time based on distance.
    Assumes average speed of 30 mph in service areas.
    
    Args:
        distance_miles: Distance in miles
        
    Returns:
        int: Travel time in minutes
    """
    avg_speed_mph = 30
    return int((distance_miles / avg_speed_mph) * 60)


def check_technician_available(technician, weekday):
    """
    Check if technician is available on given weekday.
    
    Args:
        technician: Technician data row
        weekday: Weekday name (Monday, Tuesday, etc.)
        
    Returns:
        bool: True if available
    """
    # Look for availability column
    availability_cols = [col for col in technician.index if 'availab' in col.lower()]
    
    if not availability_cols:
        return True  # Assume available if no column specified
    
    availability = str(technician[availability_cols[0]]).lower()
    
    # Check if weekday is in availability string
    if weekday.lower() in availability or 'all' in availability or 'mon-fri' in availability:
        return True
    
    return False


def check_skill_match(job_skill, tech_skill):
    """
    Check if technician skill level matches job requirements.
    
    Args:
        job_skill: Required skill level for job
        tech_skill: Technician's skill level
        
    Returns:
        bool: True if technician can perform job
    """
    if pd.isna(job_skill) or pd.isna(tech_skill):
        return True  # Assume match if not specified
    
    job_skill_str = str(job_skill).lower().strip()
    tech_skill_str = str(tech_skill).lower().strip()
    
    # Define skill hierarchy
    skill_levels = {
        'junior': 1,
        'intermediate': 2,
        'senior': 3,
        'expert': 4,
        'advanced': 3,
        'basic': 1
    }
    
    job_level = skill_levels.get(job_skill_str, 2)
    tech_level = skill_levels.get(tech_skill_str, 2)
    
    # Technician must have equal or higher skill level
    return tech_level >= job_level


def check_time_conflict(scheduled_jobs, new_job_start, new_job_end):
    """
    Check if new job conflicts with already scheduled jobs.
    
    Args:
        scheduled_jobs: List of already scheduled jobs with times
        new_job_start: Start time of new job
        new_job_end: End time of new job
        
    Returns:
        bool: True if there is a conflict
    """
    for job in scheduled_jobs:
        existing_start = job['start_time']
        existing_end = job['end_time']
        
        # Check for overlap
        if (new_job_start < existing_end and new_job_end > existing_start):
            return True
    
    return False


def normalize_column_name(df, search_terms):
    """
    Find column name in dataframe that matches one of the search terms.
    
    Args:
        df: DataFrame to search
        search_terms: List of possible column name patterns
        
    Returns:
        str: Matched column name or None
    """
    df_cols_lower = {col.lower(): col for col in df.columns}
    
    for term in search_terms:
        for col_lower, col_original in df_cols_lower.items():
            if term.lower() in col_lower:
                return col_original
    
    return None


def schedule_jobs(service_locations, technicians):
    """
    Main scheduling algorithm.
    Assigns jobs to technicians respecting all constraints.
    
    Args:
        service_locations: DataFrame with job information
        technicians: DataFrame with technician information
        
    Returns:
        tuple: (schedule_dict, unscheduled_list)
    """
    print("\n" + "="*60)
    print("STARTING JOB SCHEDULING")
    print("="*60)
    
    # Normalize column names
    job_col = normalize_column_name(service_locations, ['job', 'job_id', 'service'])
    address_col = normalize_column_name(service_locations, ['address', 'location', 'site'])
    time_col = normalize_column_name(service_locations, ['time', 'window', 'schedule'])
    duration_col = normalize_column_name(service_locations, ['duration', 'length', 'time'])
    skill_col = normalize_column_name(service_locations, ['skill', 'level', 'requirement'])
    region_col = normalize_column_name(service_locations, ['region', 'area', 'zone'])
    instructions_col = normalize_column_name(service_locations, ['instruction', 'note', 'special'])
    
    name_col = normalize_column_name(technicians, ['name', 'technician', 'employee'])
    tech_skill_col = normalize_column_name(technicians, ['skill', 'level', 'expertise'])
    availability_col = normalize_column_name(technicians, ['availab', 'schedule', 'days'])
    tech_location_col = normalize_column_name(technicians, ['location', 'base', 'start'])
    
    # Initialize schedule structure
    schedule = {day: [] for day in WEEKDAYS}
    unscheduled = []
    
    # Track technician assignments per day
    tech_assignments = {day: {tech[name_col]: [] for _, tech in technicians.iterrows()} 
                       for day in WEEKDAYS}
    
    # Process each job
    for idx, job in service_locations.iterrows():
        job_id = job[job_col] if job_col else f"Job_{idx+1}"
        job_address = job[address_col] if address_col else "Unknown"
        job_time = job[time_col] if time_col else None
        job_duration_str = job[duration_col] if duration_col else 60
        job_skill = job[skill_col] if skill_col else None
        job_region = job[region_col] if region_col else "Unknown"
        job_instructions = job[instructions_col] if instructions_col else ""
        
        # Parse time and duration
        start_time, end_time_window = parse_time_window(job_time)
        duration_minutes = parse_duration(job_duration_str)
        
        assigned = False
        
        # Try to assign to a technician for each weekday
        for day in WEEKDAYS:
            if assigned:
                break
                
            # Find available technicians for this day
            available_techs = []
            
            for _, tech in technicians.iterrows():
                tech_name = tech[name_col] if name_col else f"Tech_{_}"
                tech_skill_level = tech[tech_skill_col] if tech_skill_col else None
                
                # Check if technician is available on this day
                if not check_technician_available(tech, day):
                    continue
                
                # Check if technician has right skill level
                if not check_skill_match(job_skill, tech_skill_level):
                    continue
                
                # Check if technician hasn't exceeded max jobs for the day
                if len(tech_assignments[day][tech_name]) >= MAX_JOBS_PER_DAY:
                    continue
                
                # Check if this job would conflict with existing assignments
                job_end_time = (datetime.combine(datetime.today(), start_time) + 
                              timedelta(minutes=duration_minutes)).time()
                
                if check_time_conflict(tech_assignments[day][tech_name], start_time, job_end_time):
                    continue
                
                # Calculate priority based on existing assignments and location
                tech_location = tech[tech_location_col] if tech_location_col else ""
                distance = calculate_distance(tech_location, job_address)
                
                available_techs.append({
                    'name': tech_name,
                    'distance': distance,
                    'current_jobs': len(tech_assignments[day][tech_name])
                })
            
            # Sort technicians by: fewest jobs first, then closest distance
            available_techs.sort(key=lambda x: (x['current_jobs'], x['distance']))
            
            # Assign to first available technician
            if available_techs:
                selected_tech = available_techs[0]['name']
                
                job_end_time = (datetime.combine(datetime.today(), start_time) + 
                              timedelta(minutes=duration_minutes)).time()
                
                assignment = {
                    'job_id': job_id,
                    'technician': selected_tech,
                    'address': job_address,
                    'start_time': start_time,
                    'end_time': job_end_time,
                    'duration': duration_minutes,
                    'skill_required': job_skill,
                    'region': job_region,
                    'instructions': job_instructions
                }
                
                schedule[day].append(assignment)
                tech_assignments[day][selected_tech].append(assignment)
                assigned = True
                
                print(f"✓ Assigned {job_id} to {selected_tech} on {day}")
        
        # If not assigned to any day, add to unscheduled
        if not assigned:
            reason = "No available technician with matching skills and time slot"
            unscheduled.append({
                'job_id': job_id,
                'address': job_address,
                'time_window': f"{start_time} - {end_time_window}",
                'skill_required': job_skill,
                'region': job_region,
                'reason': reason
            })
            print(f"✗ Could not assign {job_id}: {reason}")
    
    return schedule, unscheduled


def format_time(time_obj):
    """Format time object to readable string."""
    if isinstance(time_obj, datetime):
        return time_obj.strftime("%I:%M %p")
    return time_obj.strftime("%I:%M %p")


def create_output_tables(schedule, unscheduled):
    """
    Create formatted output tables for each weekday and unscheduled jobs.
    
    Args:
        schedule: Dictionary with daily schedules
        unscheduled: List of unscheduled jobs
        
    Returns:
        dict: Dictionary of DataFrames for each day plus unscheduled
    """
    print("\n" + "="*60)
    print("CREATING OUTPUT TABLES")
    print("="*60)
    
    output_tables = {}
    
    # Create table for each weekday
    for day in WEEKDAYS:
        day_schedule = schedule[day]
        
        if not day_schedule:
            print(f"\n{day}: No jobs scheduled")
            output_tables[day] = pd.DataFrame({
                'Technician': ['No assignments'],
                'Job ID': [''],
                'Address': [''],
                'Start Time': [''],
                'End Time': [''],
                'Duration (min)': [''],
                'Special Instructions': ['']
            })
        else:
            # Sort by technician name, then start time
            day_schedule.sort(key=lambda x: (x['technician'], x['start_time']))
            
            table_data = []
            for assignment in day_schedule:
                table_data.append({
                    'Technician': assignment['technician'],
                    'Job ID': assignment['job_id'],
                    'Address': assignment['address'],
                    'Start Time': format_time(assignment['start_time']),
                    'End Time': format_time(assignment['end_time']),
                    'Duration (min)': assignment['duration'],
                    'Special Instructions': str(assignment['instructions'])[:50] if assignment['instructions'] else ''
                })
            
            output_tables[day] = pd.DataFrame(table_data)
            print(f"\n{day}: {len(day_schedule)} jobs scheduled")
    
    # Create unscheduled jobs table
    if unscheduled:
        unscheduled_data = []
        for job in unscheduled:
            unscheduled_data.append({
                'Job ID': job['job_id'],
                'Address': job['address'],
                'Time Window': job['time_window'],
                'Skill Required': job['skill_required'],
                'Region': job['region'],
                'Reason Not Scheduled': job['reason']
            })
        
        output_tables['Unscheduled'] = pd.DataFrame(unscheduled_data)
        print(f"\nUnscheduled: {len(unscheduled)} jobs could not be assigned")
    else:
        output_tables['Unscheduled'] = pd.DataFrame({
            'Message': ['All jobs successfully scheduled!']
        })
        print("\nAll jobs successfully scheduled!")
    
    return output_tables


def save_output(output_tables, output_file):
    """
    Save output tables to Excel file.
    
    Args:
        output_tables: Dictionary of DataFrames
        output_file: Output file path
    """
    print(f"\nSaving output to {output_file}...")
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for sheet_name, df in output_tables.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✓ Output saved successfully to {output_file}")
    except Exception as e:
        print(f"ERROR saving output: {e}")
        raise


def print_summary(output_tables):
    """
    Print formatted summary of schedules to console.
    
    Args:
        output_tables: Dictionary of DataFrames with schedules
    """
    print("\n" + "="*60)
    print("SCHEDULE SUMMARY")
    print("="*60)
    
    for day in WEEKDAYS:
        print(f"\n{day.upper()}")
        print("-" * 60)
        
        if day in output_tables:
            df = output_tables[day]
            if len(df) > 0 and 'Technician' in df.columns:
                if df['Technician'].iloc[0] != 'No assignments':
                    print(df.to_string(index=False))
                else:
                    print("No jobs scheduled for this day")
        print()
    
    print("\nUNSCHEDULED JOBS")
    print("-" * 60)
    if 'Unscheduled' in output_tables:
        df = output_tables['Unscheduled']
        print(df.to_string(index=False))
    print()


def main():
    """
    Main execution function.
    Orchestrates the entire scheduling process.
    """
    print("="*60)
    print("SERVICE ROUTE SCHEDULER")
    print("="*60)
    print()
    
    try:
        # Load data
        service_locations, technicians = load_data(INPUT_FILE)
        
        # Validate data structure
        validate_data(service_locations, technicians)
        
        # Perform scheduling
        schedule, unscheduled = schedule_jobs(service_locations, technicians)
        
        # Create output tables
        output_tables = create_output_tables(schedule, unscheduled)
        
        # Print summary to console
        print_summary(output_tables)
        
        # Save to Excel
        save_output(output_tables, OUTPUT_FILE)
        
        print("\n" + "="*60)
        print("SCHEDULING COMPLETE")
        print("="*60)
        print(f"\nResults saved to: {OUTPUT_FILE}")
        print("You can now review and upload this file to Excel.")
        
    except FileNotFoundError:
        print("\n" + "="*60)
        print("ERROR: Input file not found")
        print("="*60)
        print(f"\nPlease ensure '{INPUT_FILE}' is in the same directory as this script.")
        print("The file should contain two sheets:")
        print("  1. 'Service Locations' - with job details")
        print("  2. 'Technicians' - with technician information")
        
    except Exception as e:
        print("\n" + "="*60)
        print("ERROR OCCURRED")
        print("="*60)
        print(f"\nError details: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
