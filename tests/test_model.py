import pytest
from model.model_training import train_model, evaluate_model
from model.data_preparation import load_data, remove_outliers, add_interactions, encode_features
import os

def test_r2_score():
    # Chemin absolu vers le fichier de données
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'archive', 'emissions.csv')

    # Processus complet de préparation des données
    data = load_data(data_path)
    data = remove_outliers(data, 'value')
    data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
    features = ['year', 'state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction']
    X, encoder = encode_features(data[features], features)
    y = data['value']

    # Entraîner le modèle
    model, X_test, y_test = train_model(X, y)

    # Évaluer le modèle
    mse, r2 = evaluate_model(model, X_test, y_test)

    # Vérification du R²
    assert r2 > 0.55, f"R² is less than 0.55, got {r2}"

if __name__ == "__main__":
    pytest.main(["-W", "ignore:DeprecationWarning"])
