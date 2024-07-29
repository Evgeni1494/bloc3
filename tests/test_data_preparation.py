import pytest
import os
from model.data_preparation import load_data, remove_outliers, add_interactions, encode_features, prepare_data
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from numpy.testing import assert_array_equal

# Configuration to find the test CSV file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'archive', 'emissions.csv')

def test_load_data():
    """
    Test if the data is loaded correctly from a CSV file.

    This test verifies that the data is loaded into a DataFrame and is not empty.
    It ensures that the function `load_data` correctly reads the CSV file and 
    returns a valid DataFrame.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '../archive/emissions.csv')
    data = load_data(data_path)
    assert not data.empty, "Data should not be empty"

def test_remove_outliers():
    """
    Test the `remove_outliers` function to ensure it correctly removes outliers.

    This test checks that the number of rows in the DataFrame decreases after
    removing outliers, indicating that outliers were successfully removed.
    The `remove_outliers` function should use z-scores to identify and filter out
    rows that are considered outliers in the specified column.
    """
    data = load_data(data_path)
    data_no_outliers = remove_outliers(data, 'value')
    assert len(data_no_outliers) < len(data), "Data without outliers should have fewer rows"

def test_add_interactions():
    """
    Test the `add_interactions` function to ensure it adds a new interaction column.

    This test verifies that a new column, resulting from the interaction of two
    specified columns, is correctly added to the DataFrame. It ensures that the
    interaction column is present in the DataFrame after the function is called.
    """
    data = load_data(data_path)
    data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
    assert 'fuel_sector_interaction' in data.columns, "New interaction column should be in data"

def test_prepare_data():
    """
    Test the `prepare_data` function to ensure it processes data correctly.

    This test checks that the `prepare_data` function completes all steps including
    loading data, removing outliers, adding interaction columns, and encoding categorical
    features. It verifies that the resulting DataFrame is not empty, has columns, and that
    the encoder is saved to a file.
    """
    final_data = prepare_data(data_path)
    assert final_data.shape[0] > 0, "Final data should not be empty"
    assert final_data.shape[1] > 0, "Final data should have columns"
    assert os.path.exists('encoder.pkl'), "Encoder file should be saved"

if __name__ == "__main__":
    pytest.main(["-W", "ignore:DeprecationWarning"])
