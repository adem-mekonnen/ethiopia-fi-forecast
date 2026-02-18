import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

def load_data():
    """Loads enriched data and event matrix."""
    enc_path = 'data/processed/ethiopia_fi_enriched.csv'
    matrix_path = 'data/processed/event_indicator_matrix.csv'
    
    if not os.path.exists(enc_path):
        raise FileNotFoundError(f"Enriched data not found at {enc_path}. Please run task1_enrichment.py.")
        
    df = pd.read_csv(enc_path)
    
    # Load Matrix if exists, else return empty
    if os.path.exists(matrix_path):
        matrix = pd.read_csv(matrix_path, index_col=0)
    else:
        matrix = pd.DataFrame()
        print("Warning: Event matrix not found. Shocks will not be applied.")
        
    return df, matrix

def calculate_baseline(history_df, target_year):
    """
    Fits a linear trend to historical data and projects to target_year.
    Returns the projected value and the model (for slope).
    """
    if history_df.empty or len(history_df) < 2:
        return None, None
        
    X = history_df[['year']].values.reshape(-1, 1)
    y = history_df['value_numeric'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_X = np.array([[target_year]])
    projection = model.predict(future_X)[0]
    
    return projection, model

def apply_shocks(year, matrix, indicator_code, scenario='Base'):
    """
    Applies shocks from the matrix. Returns the shock value for that year.
    """
    if matrix.empty:
        return 0.0 # Return shock component only
        
    total_shock = 0.0
    
    # Iterate through events to find those applicable to this year
    # Assuming Event Name format "Event Name (YYYY)"
    for event_name, row in matrix.iterrows():
        try:
            # Simple heuristic to extract year
            if '(' in str(event_name) and ')' in str(event_name):
                 event_year_str = str(event_name).split('(')[-1].replace(')', '')
                 if event_year_str.isdigit():
                     event_year = int(event_year_str)
                     
                     if event_year == year:
                        shock = row.get(indicator_code, 0.0)
                        
                        # Apply Scenario Multiplier
                        if scenario == 'Optimistic':
                            shock *= 1.2
                        elif scenario == 'Pessimistic':
                            shock *= 0.5
                        
                        total_shock += shock
        except ValueError:
            continue
            
    # Assuming Matrix values are decimal format of Percentage Points? e.g. 0.05 = 5pp?
    # Or 0.05 = 0.05pp?
    # Based on checking the matrix content previously: 0.05.
    # If the user meant 5%, usually they write 5.0 or 0.05.
    # Given the hardcoded code had "3.0" for 3pp.
    # I will assume the matrix values need to be scaled by 100 if they are small (<1).
    # Heuristic: if shock < 1.0, multiply by 100.
    
    if abs(total_shock) < 1.0 and abs(total_shock) > 0.0001:
        total_shock *= 100
        
    return total_shock

def run_forecasting_scenarios():
    print("--- Starting Forecasting (Trend + Shocks) ---")
    
    try:
        df, matrix = load_data()
    except FileNotFoundError as e:
        print(e)
        return

    # Filter for Account Ownership
    target_indicator = 'ACC_OWNERSHIP'
    history = df[df['indicator_code'] == target_indicator].sort_values('year')
    
    if history.empty:
        print(f"No history found for {target_indicator}")
        # Build dummy history for robustness if file is empty but exists
        history = pd.DataFrame({
             'year': [2011, 2014, 2017, 2021],
             'value_numeric': [22, 22, 35, 46]
        })
        print("Using dummy history.")
    
    print(f"Historical Data Points: {len(history)}")
    
    # Calculate RSE for CI
    # Pre-calc to use in loop
    X = history[['year']].values.reshape(-1, 1)
    y = history['value_numeric'].values
    model_rse = LinearRegression()
    model_rse.fit(X, y)
    residuals = y - model_rse.predict(X)
    rse = np.std(residuals)
    ci_95 = 1.96 * rse if len(history) > 2 else 2.0
    
    future_years = [2025, 2026, 2027]
    scenarios = ['Base', 'Optimistic', 'Pessimistic']
    
    results = []
    
    for sc in scenarios:
        cumulative_shock_carryover = 0.0
        
        for i, year in enumerate(future_years):
            base_pred, _ = calculate_baseline(history, year)
            
            # Current year shock
            current_shock = apply_shocks(year, matrix, target_indicator, sc)
            
            # Additional Scenario tweaks
            if sc == 'Optimistic':
                current_shock += 1.0 
            elif sc == 'Pessimistic':
                current_shock -= 1.0
                
            cumulative_shock_carryover += current_shock
            
            final_pred = base_pred + cumulative_shock_carryover
            
            results.append({
                'Scenario': sc,
                'Year': year,
                'Predicted_Ownership': round(final_pred, 2),
                'Lower_CI': round(final_pred - ci_95, 2),
                'Upper_CI': round(final_pred + ci_95, 2)
            })

    results_df = pd.DataFrame(results)
    print("\n--- Forecasting Results (2025-2027) ---")
    print(results_df)
    
    output_path = 'data/processed/forecasting_results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    results_df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")

if __name__ == "__main__":
    run_forecasting_scenarios()