import pytest
import pandas as pd
import numpy as np
from src.forecasting import calculate_baseline

def test_calculate_baseline_valid():
    # Create mock data
    df = pd.DataFrame({
        'indicator_code': ['ACC_OWNERSHIP', 'ACC_OWNERSHIP'],
        'record_type': ['observation', 'observation'],
        'year': [2011, 2024],
        'value_numeric': [22, 49]
    })
    result = calculate_baseline(df, 'ACC_OWNERSHIP', 2027)
    assert result > 49  # Trend should be upward
    assert isinstance(result, float)

def test_calculate_baseline_empty():
    df = pd.DataFrame(columns=['indicator_code', 'record_type', 'year', 'value_numeric'])
    result = calculate_baseline(df, 'ACC_OWNERSHIP', 2027)
    assert result == 0.0