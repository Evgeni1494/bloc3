import pytest
import os
from model.data_preparation import load_data, remove_outliers, add_interactions, encode_features, prepare_data
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from numpy.testing import assert_array_equal

# Configuration pour trouver le fichier CSV de test
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'archive', 'emissions.csv')

def test_load_data():
    """Teste si les données sont chargées correctement."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '../archive/emissions.csv')
    data = load_data(data_path)
    assert not data.empty, "Data should not be empty"


def test_remove_outliers():
    """Test pour la fonction remove_outliers."""
    data = load_data(data_path)
    data_no_outliers = remove_outliers(data, 'value')
    assert len(data_no_outliers) < len(data), "Data without outliers should have fewer rows"

def test_add_interactions():
    """Test pour la fonction add_interactions."""
    data = load_data(data_path)
    data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
    assert 'fuel_sector_interaction' in data.columns, "New interaction column should be in data"

def test_prepare_data():
    """Test pour la fonction prepare_data."""
    final_data = prepare_data(data_path)
    assert final_data.shape[0] > 0, "Final data should not be empty"
    assert final_data.shape[1] > 0, "Final data should have columns"
    assert os.path.exists('encoder.pkl'), "Encoder file should be saved"

if __name__ == "__main__":
    pytest.main(["-W", "ignore:DeprecationWarning"])