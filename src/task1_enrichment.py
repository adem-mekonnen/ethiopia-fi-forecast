import pandas as pd
import numpy as np
from datetime import datetime
import os

def run_enrichment():
    # Update paths to match your .xlsx files in the screenshot
    raw_path = 'data/raw/ethiopia_fi_unified_data.xlsx'
    
    if not os.path.exists(raw_path):
        print(f"Error: Starter dataset not found at {raw_path}")
        return

    # Reading from Excel instead of CSV
    df = pd.read_excel(raw_path)
    print(f"Initial dataset loaded: {len(df)} records.")

    # 1. Define Enrichment Data
    # A. New Observation (e.g., Transaction Volume from NBE)
    new_obs = {
        'record_type': 'observation',
        'pillar': 'usage',
        'indicator': 'Mobile Money Transaction Volume (Billions ETB)',
        'indicator_code': 'USG_MM_VOL',
        'value_numeric': 4800.0,
        'observation_date': '2024-06-30',
        'source_name': 'NBE Annual Report 2023/24',
        'source_url': 'https://nbe.gov.et/',
        'confidence': 'high',
        'collected_by': 'Data Scientist',
        'collection_date': datetime.now().strftime('%Y-%m-%d'),
        'notes': 'Captures scale of transformation beyond simple ownership %.',
        'original_text': 'Total mobile money transfer reached 4.8 trillion ETB.'
    }

    # B. New Event (Fayda Digital ID rollout)
    new_evt = {
        'record_type': 'event',
        'parent_id': 'EVT_FAYDA_2024',
        'category': 'infrastructure',
        'event_name': 'Launch of Fayda Digital ID Mass Enrollment',
        'pillar': np.nan, 
        'observation_date': '2024-03-01',
        'source_name': 'National ID Program',
        'source_url': 'https://id.gov.et/',
        'confidence': 'high',
        'collected_by': 'Data Scientist',
        'collection_date': datetime.now().strftime('%Y-%m-%d'),
        'notes': 'Critical for solving KYC bottlenecks.',
        'original_text': 'Fayda ID rollout aimed at 90 million citizens.'
    }

    # C. New Impact Link
    new_link = {
        'record_type': 'impact_link',
        'parent_id': 'EVT_FAYDA_2024',
        'pillar': 'access',
        'related_indicator': 'ACC_OWNERSHIP',
        'impact_direction': 'positive',
        'impact_magnitude': 0.05,
        'lag_months': 6,
        'evidence_basis': 'India Aadhaar proxy study',
        'confidence': 'medium',
        'collected_by': 'Data Scientist',
        'collection_date': datetime.now().strftime('%Y-%m-%d')
    }

    # 2. Append and Save to Processed folder as CSV for easier use in EDA
    enriched_records = pd.DataFrame([new_obs, new_evt, new_link])
    df_final = pd.concat([df, enriched_records], ignore_index=True)

    os.makedirs('data/processed', exist_ok=True)
    
    # We save as CSV in processed because it's faster for Task 2 (EDA)
    output_file = 'data/processed/ethiopia_fi_enriched.csv'
    df_final.to_csv(output_file, index=False)
    
    print(f"\nEnrichment complete. Total records: {len(df_final)}")
    print(f"File saved to: {output_file}")

if __name__ == "__main__":
    run_enrichment()