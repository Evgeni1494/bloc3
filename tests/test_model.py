import pytest
from model.model_training import train_model, evaluate_model
from model.data_preparation import load_data, remove_outliers, add_interactions, encode_features
import os

def test_r2_score():
    """
    Test the model's R² score to ensure it meets the expected performance threshold.

    This test loads the data, preprocesses it, trains the model, and evaluates it.
    It verifies that the R² score of the model is greater than 0.55.

    Raises:
        AssertionError: If the R² score is less than or equal to 0.55.
    """
    # Absolute path to the data file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'archive', 'emissions.csv')

    # Complete data preparation process
    data = load_data(data_path)
    data = remove_outliers(data, 'value')
    data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
    features = ['year', 'state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction']
    X, encoder = encode_features(data[features], features)
    y = data['value']

    # Train the model
    model, X_test, y_test = train_model(X, y)

    # Evaluate the model
    mse, r2 = evaluate_model(model, X_test, y_test)

    # Verify the R² score
    assert r2 > 0.55, f"R² is less than 0.55, got {r2}"

def test_mse_score():
    """
    Test the model's Mean Squared Error (MSE) to ensure it meets the expected performance threshold.

    This test loads the data, preprocesses it, trains the model, and evaluates it.
    It verifies that the MSE of the model is less than 1000.

    Raises:
        AssertionError: If the MSE is greater than or equal to 1000.
    """
    # Absolute path to the data file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'archive', 'emissions.csv')

    # Load the data
    data = load_data(data_path)

    # Prepare the data
    data = remove_outliers(data, 'value')
    data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
    features = ['year', 'state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction']
    X, encoder = encode_features(data[features], features)
    y = data['value']

    # Train the model
    model, X_test, y_test = train_model(X, y)

    # Evaluate the model
    mse, r2 = evaluate_model(model, X_test, y_test)

    # Verify the MSE
    assert mse < 1000, f"MSE is greater than 1000, got {mse}"

if __name__ == "__main__":
    pytest.main(["-W", "ignore:DeprecationWarning"])
