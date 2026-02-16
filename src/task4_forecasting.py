
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def run_forecasting_scenarios():
    print("--- Starting Forecasting (Trend + Shocks) ---")

    # 1. Historical Data (N=5 Findex Points) - Example: Account Ownership %
    # Using approximate values for Ethiopia: 2011=22%, 2014=22%, 2017=35%, 2021=46%, 2024=50% (Projected)
    history = pd.DataFrame({
        'year': [2011, 2014, 2017, 2021, 2024],
        'ownership': [22, 22, 35, 46, 50]
    })
    
    # 2. Fit Linear Trend (The "Business as Usual" Baseline)
    X = history[['year']]
    y = history['ownership']
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_years = [2025, 2026, 2027]
    baseline_pred = model.predict(pd.DataFrame({'year': future_years}))
    
    # Calculate simplistic 95% Confidence Interval based on Residual Standard Error (RSE)
    residuals = y - model.predict(X)
    rse = np.std(residuals)
    ci_95 = 1.96 * rse # Approx margin of error
    
    print(f"Baseline Trend Slope: +{model.coef_[0]:.2f} pp/year")
    print(f"95% CI Margin: +/- {ci_95:.2f} pp")

    # 3. Define Future Shock Events & Impacts (in percentage points)
    # These base impacts come from our Impact Modeling/Association Matrix step.
    # Event 1: EthSwitch Interoperability (2025) -> +3pp
    # Event 2: Fayda ID Full Rollout (2026) -> +4pp
    
    shocks = {
        2025: 3.0, 
        2026: 4.0,  # Cumulative carrying over? Or specific new shock? 
                    # Assuming structural shift adding to the level.
        2027: 1.0   # Diminishing returns from new users
    }
    
    # 4. Scenario Calculations
    scenarios = {
        'Base': {'multiplier': 1.0, 'macro_penalty': 0},
        'Optimistic': {'multiplier': 1.2, 'macro_penalty': 0, 'innovation_boost': 2.0},
        'Pessimistic': {'multiplier': 0.5, 'macro_penalty': -3.0}
    }
    
    results = []
    
    for sc_name, params in scenarios.items():
        current_val = history['ownership'].iloc[-1] # Start from 2024 actual
        
        # We need to project year by year to accumulate
        # Actually, let's just add the shock to the trend prediction for simplicity in this demo.
        # Trend prediction gives the base level.
        
        for i, year in enumerate(future_years):
            trend_val = baseline_pred[i]
            
            # Shocks are usually cumulative structural changes. 
            # If 2025 has a shock of +3, then 2026 effectively starts 3 higher than trend?
            # Or is the trend capturing organic growth and shocks are ON TOP?
            # Let's assume Shocks are additive to the Trend level.
            
            shock_val = shocks.get(year, 0) * params['multiplier']
            
            # Add specific scenario adjustments
            if sc_name == 'Optimistic':
                shock_val += params.get('innovation_boost', 0)
            elif sc_name == 'Pessimistic':
                shock_val += params.get('macro_penalty', 0)
                
            # For 2026, we should likely include 2025's shock too if it's a permanent level shift.
            # Simplified: Cumulative sum of previous shocks + current shock + current trend.
            # But 'baseline_pred' from linear regression already includes the time component.
            # We just need to add the cumulative shocks.
            
            past_shocks = sum([shocks.get(y,0) for y in range(2025, year)]) * params['multiplier']
            
            # Pessimistic: penalty applies every year? Or just once? Let's say annual drag.
            # This logic can be refined.
            
            final_pred = trend_val + past_shocks + shock_val
            
            if sc_name == 'Pessimistic':
                 # Apply cumulative penalty
                 final_pred += (i+1) * params.get('macro_penalty', 0)
            
            results.append({
                'Scenario': sc_name,
                'Year': year,
                'Predicted_Ownership': round(final_pred, 2),
                'Lower_CI': round(final_pred - ci_95, 2),
                'Upper_CI': round(final_pred + ci_95, 2)
            })

    results_df = pd.DataFrame(results)
    print("\n--- Forecasting Results (2025-2027) ---")
    print(results_df)
    
    # Save results
    results_df.to_csv('data/processed/forecasting_results.csv', index=False)
    print("\nSaved to data/processed/forecasting_results.csv")

if __name__ == "__main__":
    run_forecasting_scenarios()