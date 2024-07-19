import pytest
from sklearn.datasets import make_regression
from model.model_training import train_model, evaluate_model

def test_model_r2():
    # Generate a random regression problem
    X, y = make_regression(n_samples=100, n_features=10, noise=0.1)
    
    # Train the model
    model, X_test, y_test = train_model(X, y)
    
    # Evaluate the model
    mse, r2 = evaluate_model(model, X_test, y_test)
    
    # Check if R2 score is greater than 0.55
    assert r2 > 0.55, f"R2 score is too low: {r2}"

if __name__ == "__main__":
    pytest.main()
