import pandas as pd
import numpy as np
import os

def run_forecasting():
    # File Paths
    data_path = 'data/processed/ethiopia_fi_enriched.csv'
    matrix_path = 'data/processed/event_indicator_matrix.csv'
    output_path = 'data/processed/final_forecasts_2027.csv'

    # 1. Load Data
    if not os.path.exists(data_path) or not os.path.exists(matrix_path):
        print("❌ Error: Required files missing. Run Task 1 and Task 3 scripts first.")
        return

    df = pd.read_csv(data_path)
    
    # --- FIX: Ensure 'year' column exists ---
    if 'year' not in df.columns:
        print("🔧 Extracting 'year' from 'observation_date'...")
        # Use format='mixed' to handle the different date formats in your enriched file
        df['observation_date'] = pd.to_datetime(df['observation_date'], errors='coerce')
        df['year'] = df['observation_date'].dt.year
    
    # Drop rows where year couldn't be determined
    df = df.dropna(subset=['year', 'value_numeric'])

    # Load the matrix from Task 3
    matrix = pd.read_csv(matrix_path, index_col=0)

    # 2. Define Target Indicators
    target_access = 'ACC_OWNERSHIP'
    target_usage = 'ACC_MM_ACCOUNT'
    
    forecast_years = [2025, 2026, 2027]

    # 3. Baseline Trend Function
    def calculate_baseline(indicator_code, target_year):
        hist = df[(df['indicator_code'] == indicator_code) & (df['record_type'] == 'observation')]
        
        if hist.empty:
            return 0
        
        # Sort by the newly created year column
        hist = hist.sort_values('year')
        x = hist['year'].values
        y = hist['value_numeric'].values
        
        if len(x) < 2:
            return y[-1] if len(y) > 0 else 0
        
        m, b = np.polyfit(x, y, 1)
        return m * target_year + b

    # 4. Impact Lift Calculation
    total_lifts = matrix.sum().to_dict()

    # 5. Generate Scenarios
    scenarios = {
        'Base': 1.0,
        'Optimistic': 1.2,
        'Pessimistic': 0.7
    }

    ramp_up = {2025: 0.4, 2026: 0.8, 2027: 1.0}

    results = []

    print("--- Starting Forecast Calculation ---")
    for year in forecast_years:
        for name, multiplier in scenarios.items():
            base_acc = calculate_baseline(target_access, year)
            base_usg = calculate_baseline(target_usage, year)

            lift_acc = total_lifts.get(target_access, 0) * ramp_up[year] * multiplier
            lift_usg = total_lifts.get(target_usage, 0) * ramp_up[year] * multiplier

            results.append({
                'Year': year,
                'Scenario': name,
                'Access_Rate': round(base_acc + lift_acc, 2),
                'Usage_Rate': round(base_usg + lift_usg, 2)
            })

    # 6. Save Results
    forecast_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    forecast_df.to_csv(output_path, index=False)
    
    print(f"✅ Success! Projections saved to {output_path}")
    print("\nPreview of 2027 Projections (Base Scenario):")
    print(forecast_df[(forecast_df['Year'] == 2027) & (forecast_df['Scenario'] == 'Base')])

if __name__ == "__main__":
    run_forecasting()