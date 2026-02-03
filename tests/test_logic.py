import pandas as pd
import os

def test_data_files_exist():
    """Check if the necessary processed files were generated."""
    assert os.path.exists("data/processed/ethiopia_fi_enriched.csv")
    assert os.path.exists("data/processed/event_indicator_matrix.csv")
    assert os.path.exists("data/processed/final_forecasts_2027.csv")

def test_forecast_logic():
    """Verify that the forecast output has the correct scenarios."""
    df = pd.read_csv("data/processed/final_forecasts_2027.csv")
    expected_scenarios = ['Base', 'Optimistic', 'Pessimistic']
    assert all(scen in df['Scenario'].unique() for scen in expected_scenarios)