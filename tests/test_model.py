import pytest
from sklearn.datasets import make_regression
from model.model_training import train_model, evaluate_model
import sqlite3

def setup_memory_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE training_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            model_type TEXT,
            mse REAL,
            r2 REAL
        )
    ''')
    conn.commit()
    return conn

def test_model_r2():
    # Setup in-memory database
    conn = setup_memory_db()
    
    # Generate a random regression problem
    X, y = make_regression(n_samples=100, n_features=10, noise=0.1)
    
    # Train the model
    model, X_test, y_test = train_model(X, y, db_path=':memory:')
    
    # Evaluate the model
    mse, r2 = evaluate_model(model, X_test, y_test, db_path=':memory:')
    
    # Check if R2 score is greater than 0.55
    assert r2 > 0.55, f"R2 score is too low: {r2}"
    
    # Close the in-memory database connection
    conn.close()

if __name__ == "__main__":
    pytest.main()
