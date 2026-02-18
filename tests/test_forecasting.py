import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.task4_forecasting import calculate_baseline, apply_shocks, load_data

def test_calculate_baseline_valid():
    # Create mock data
    df = pd.DataFrame({
        'year': [2011, 2014, 2021],
        'value_numeric': [22, 35, 46]
    })
    projection, model = calculate_baseline(df, 2025)
    
    assert projection > 46
    assert isinstance(projection, float)
    assert model is not None

def test_calculate_baseline_empty():
    df = pd.DataFrame(columns=['year', 'value_numeric'])
    projection, model = calculate_baseline(df, 2025)
    assert projection is None
    assert model is None

def test_apply_shocks_no_matrix():
    matrix = pd.DataFrame()
    # base_val removed from call
    result = apply_shocks(2025, matrix, 'ACC_OWNERSHIP')
    assert result == 0.0

def test_apply_shocks_with_matrix():
    # Mock Matrix
    matrix = pd.DataFrame({
        'ACC_OWNERSHIP': [0.05], # 5% shock
    }, index=['Event A (2025)'])
    
    # base_val removed from call
    shock = apply_shocks(2025, matrix, 'ACC_OWNERSHIP')
    
    # Logic: 0.05 < 1.0 -> multiplied by 100 -> 5.0
    assert shock == 5.0

@patch('src.task4_forecasting.os.path.exists')
@patch('src.task4_forecasting.pd.read_csv')
def test_load_data_success(mock_read_csv, mock_exists):
    mock_exists.return_value = True
    mock_read_csv.return_value = pd.DataFrame({'a': [1]})
    
    df, matrix = load_data()
    assert not df.empty
    assert not matrix.empty

@patch('src.task4_forecasting.os.path.exists')
def test_load_data_failure(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        load_data()