import pytest
from model.data_preparation import load_data, prepare_data

def test_load_data():
    """Teste si les données sont chargées correctement."""
    data = load_data('../archive/emissions.csv')
    assert not data.empty, "Data should not be empty"





