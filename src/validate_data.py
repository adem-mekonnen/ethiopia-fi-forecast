import pandas as pd
import sys
import os
from dateutil import parser

def validate_dataset(file_path):
    """
    Validates the Ethiopia Financial Inclusion Unified Dataset.
    """
    print(f"Validating file: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    # Load data
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print("Error: Unsupported file format. Please use .csv or .xlsx")
            sys.exit(1)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    print(f"Loaded {len(df)} records.\n")
    
    issues_found = 0

    # 1. Check for Missing Values in value_numeric
    # Only applies to 'observation' and 'impact_link' types where value is expected? 
    # The prompt says "Missing values in value_numeric", implying generally.
    # However, 'event' records might not have 'value_numeric' if strictly descriptive, 
    # but based on schema, value_numeric for events might be null.
    # Let's check based on record_type
    
    # According to README:
    # Observations: Must include value_numeric
    # Impact Links: Contain magnitude/confidence/lag, might use value_numeric for magnitude? 
    # The schema usually has 'value_numeric' for observations.
    
    missing_val_obs = df[
        (df['record_type'] == 'observation') & 
        (df['value_numeric'].isnull())
    ]
    
    if not missing_val_obs.empty:
        print(f"[FAIL] Found {len(missing_val_obs)} observations with missing 'value_numeric'.")
        print(missing_val_obs[['record_id', 'record_type', 'indicator_code']])
        issues_found += 1
    else:
        print("[PASS] No missing 'value_numeric' in observations.")

    # 2. Logic Check: Event types must not have a pillar assigned
    event_pillar_issues = df[
        (df['record_type'] == 'event') & 
        (df['pillar'].notnull())
    ]
    
    if not event_pillar_issues.empty:
        print(f"[FAIL] Found {len(event_pillar_issues)} events with a assigned pillar (Events should be neutral).")
        print(event_pillar_issues[['record_id', 'event_name', 'pillar']])
        issues_found += 1
    else:
        print("[PASS] All events have empty pillar assignment.")

    # 3. Temporal Range Check (2011-2024)
    # Check 'year' column if it exists, or parse 'date'
    
    invalid_date_records = []
    
    if 'year' in df.columns:
        # Check year column directly
        out_of_range = df[
            (df['year'].notnull()) & 
            (~df['year'].between(2011, 2024))
        ]
        if not out_of_range.empty:
             print(f"[FAIL] Found {len(out_of_range)} records with year outside 2011-2024.")
             invalid_date_records.extend(out_of_range['record_id'].tolist())
             issues_found += 1
    
    if 'date' in df.columns:
        # Check date column
        # Filter for non-null dates
        dates = df[df['date'].notnull()].copy()
        
        # Function to parse and check year
        def check_year(d):
            try:
                dt = pd.to_datetime(d)
                return 2011 <= dt.year <= 2024
            except:
                return False # Invalid format is also a fail, but here specifically range check

        # This is a bit safer if mixed formats
        dates['is_valid_range'] = pd.to_datetime(dates['date'], errors='coerce').dt.year.between(2011, 2024)
        
        out_of_range_dates = dates[~dates['is_valid_range']]
        
        if not out_of_range_dates.empty:
            print(f"[FAIL] Found {len(out_of_range_dates)} records with date outside 2011-2024.")
            # print(out_of_range_dates[['record_id', 'date']])
            issues_found += 1
        else:
             print("[PASS] All dates are within 2011-2024 range.")
    
    if not ('year' in df.columns or 'date' in df.columns):
        print("[WARN] No 'year' or 'date' column found to validate temporal range.")
    
    if issues_found == 0:
        print("\n\u2705 Dataset validation passed successfully!")
    else:
        print(f"\n\u274c Dataset validation failed with {issues_found} issues.")

if __name__ == "__main__":
    # Default path, but can be overridden
    default_path = "data/raw/ethiopia_fi_unified_data.xlsx"
    
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = default_path
        
    # Adjust for script location if running from root
    if not os.path.exists(target_file) and os.path.exists(os.path.join("..", target_file)):
         target_file = os.path.join("..", target_file)

    validate_dataset(target_file)
