
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_or_mock_data():
    """
    Attempts to load the enriched dataset. If not found, creates a mock DataFrame
    representing the expected structure for demonstration purposes.
    """
    file_path = 'data/processed/ethiopia_fi_enriched.csv'
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            print("Successfully loaded enriched data.")
            return df
        except Exception as e:
            print(f"Error reading file: {e}. Generating mock data.")
    else:
        print("Enriched data not found at expected path. Generating mock data.")

    # Mock Data Generation (2017-2024 trends)
    years = np.arange(2017, 2025)
    
    # Simulating 4G Coverage (Growing steadily)
    coverage_4g = [10, 15, 25, 40, 65, 80, 90, 95] 
    
    # Simulating Adoption (Lagged but accelerating)
    adoption = [5, 6, 8, 12, 18, 28, 45, 50]
    
    data = []
    
    for y, c, a in zip(years, coverage_4g, adoption):
        # Observation for 4G Coverage
        data.append({
            'year': y,
            'indicator_code': 'INF_4G_COVERAGE',
            'value_numeric': c
        })
        # Observation for Digital Payment Adoption
        # Note: Using usage pillar indicator for adoption
        data.append({
            'year': y,
            'indicator_code': 'USG_DIGITAL_ADOPTION', # Hypothetical code for demonstration
            'value_numeric': a
        })
        
    return pd.DataFrame(data)

def plot_dual_axis_chart(df):
    """
    Generates a dual-axis line chart comparing 4G Coverage and Digital Payment Adoption.
    """
    # Filter data for the relevant indicators
    # Note: Adjust indicator codes based on your actual data enrichment log if different
    # Assuming: 'INF_4G_COVERAGE' and 'USG_DIGITAL_ADOPTION' (or similar proxy)
    
    # Helper to pivot dataset for plotting
    try:
        # Check if 'year' column exists, if not extract from 'observation_date'
        if 'year' not in df.columns and 'observation_date' in df.columns:
            df['year'] = pd.to_datetime(df['observation_date']).dt.year
            
        pivot_df = df.pivot_table(
            index='year', 
            columns='indicator_code', 
            values='value_numeric',
            aggfunc='mean'
        )
        
        # We need two specific columns. If they don't exist in the real data, 
        # we might need to fallback or warn.
        # For the mock function above, we used specific codes.
        # Let's ensure we are creating the plot based on available columns or the mock ones.
        
        target_cols = ['INF_4G_COVERAGE', 'USG_DIGITAL_ADOPTION']
        
        # If using real data, adjust these target_cols to match what's in your CSV
        # For example, from previous steps we added 'USG_MM_VOL' maybe? 
        # But the prompt asks for "Digital Payment Adoption" vs "4G Coverage".
        # If 'USG_DIGITAL_ADOPTION' is not there, we will just use whatever IS there for demonstration.
        
        missing_cols = [c for c in target_cols if c not in pivot_df.columns]
        
        if missing_cols:
            print(f"Warning: Missing columns in data for plotting: {missing_cols}")
            # Identify potential substitutes if real data has different names
            # For now, if mock data is used, these columns WILL exist.
            if len(pivot_df.columns) >= 2:
                 target_cols = pivot_df.columns[:2] # Fallback to first two columns
                 print(f"Falling back to columns: {target_cols}")
            else:
                print("Not enough data columns to plot dual-axis chart.")
                return

        # Plotting
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Digital Payment Adoption (%)', color=color)
        ax1.plot(pivot_df.index, pivot_df[target_cols[1]], color=color, marker='o', label=target_cols[1])
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, linestyle='--', alpha=0.7)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:orange'
        ax2.set_ylabel('4G Coverage (%)', color=color)  # we already handled the x-label with ax1
        ax2.plot(pivot_df.index, pivot_df[target_cols[0]], color=color, marker='s', linestyle='--', label=target_cols[0])
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title('Impact of Infrastructure on Financial Inclusion (2017-2024)')
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        
        output_path = 'reports/figures'
        os.makedirs(output_path, exist_ok=True)
        save_path = os.path.join(output_path, 'dual_axis_4g_adoption.png')
        plt.savefig(save_path)
        print(f"Chart saved to {save_path}")
        # plt.show() # Commented out for non-interactive environments

    except Exception as e:
        print(f"An error occurred during plotting: {e}")

if __name__ == "__main__":
    # Ensure dependencies are installed (in your environment): pandas, matplotlib, seaborn
    print("Starting Deep-Dive EDA Script...")
    df = load_or_mock_data()
    if df is not None and not df.empty:
        plot_dual_axis_chart(df)
    else:
        print("No data available to plot.")
