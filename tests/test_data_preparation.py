import pytest
import os
from model.data_preparation import load_data, prepare_data

def test_load_data():
    """Teste si les données sont chargées correctement."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '../archive/emissions.csv')
    data = load_data(data_path)
    assert not data.empty, "Data should not be empty"
