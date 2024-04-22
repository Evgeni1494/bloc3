import pytest
from model.data_preparation import load_data, prepare_data

def test_load_data():
    """Teste si les données sont chargées correctement."""
    data = load_data('path_to_data.csv')
    assert not data.empty, "Data should not be empty"

def test_prepare_data():
    """Teste la fonction de préparation des données pour s'assurer qu'elle fonctionne correctement."""
    data = prepare_data('path_to_data.csv')
    assert 'fuel_sector_interaction' in data.columns, "Interaction column missing"
    assert data.isnull().sum().sum() == 0, "There should be no missing values"
