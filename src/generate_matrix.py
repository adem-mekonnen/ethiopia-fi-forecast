import pandas as pd
import numpy as np
import os

def generate_matrix():
    data_path = 'data/processed/ethiopia_fi_enriched.csv'
    output_path = 'data/processed/event_indicator_matrix.csv'

    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    df = pd.read_csv(data_path)

    # 1. Isolate and Clean
    links = df[df['record_type'] == 'impact_link'].copy()
    events = df[df['record_type'] == 'event'].copy()

    # Clean IDs
    links['parent_id'] = links['parent_id'].astype(str).str.strip()
    events['parent_id'] = events['parent_id'].astype(str).str.strip()

    # 2. Prepare a clean event lookup table (only 2 columns)
    # This prevents the event_name_x / event_name_y error
    events['event_display_name'] = events['indicator'].fillna(events['parent_id'])
    event_lookup = events[['parent_id', 'event_display_name']].drop_duplicates()

    # 3. Merge
    # We join the links with our clean lookup table
    impact_model_df = pd.merge(links, event_lookup, on='parent_id', how='inner')

    if impact_model_df.empty:
        print("❌ Error: Merge resulted in empty dataframe.")
        return

    # 4. Standardize numeric and column names
    impact_model_df['impact_magnitude'] = pd.to_numeric(impact_model_df['impact_magnitude'], errors='coerce').fillna(0)
    
    # Check which indicator column to use
    if 'related_indicator' in impact_model_df.columns:
        ind_col = 'related_indicator'
    else:
        ind_col = 'indicator_code'

    # 5. Pivot Table
    try:
        matrix = impact_model_df.pivot_table(
            index='event_display_name', 
            columns=ind_col, 
            values='impact_magnitude', 
            aggfunc='sum'
        ).fillna(0)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        matrix.to_csv(output_path)
        print(f"✅ Success! Matrix saved to {output_path}")
        print("You can now run Task 4 and start your Dashboard.")
        
    except Exception as e:
        print(f"❌ Pivot failed: {e}")

if __name__ == "__main__":
    generate_matrix()