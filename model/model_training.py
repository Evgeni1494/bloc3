import mlflow
from mlflow import log_metric, log_param, log_artifacts
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import sqlite3
import os

def train_model(data, target):
    """
    Train a Ridge regression model on the provided data and log the training process with MLflow.

    Args:
        data (DataFrame or array-like): The feature data for training.
        target (Series or array-like): The target variable for training.

    Returns:
        tuple: The trained model, test features, and test targets.
    """
    with mlflow.start_run():
        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=0)
        
        # Initializing the Ridge regression model with alpha parameter
        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)

        # Evaluate the model on the test data
        mse, r2 = evaluate_model(model, X_test, y_test)

        # Logging parameters and metrics to MLflow
        mlflow.log_param("alpha", 1.0)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)

        # Logging the Ridge model to MLflow
        mlflow.sklearn.log_model(model, "ridge_model")

        # Return the model and the test dataset for further validation if necessary
        return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model on the test data and log the results.

    Args:
        model (Estimator): The trained model.
        X_test (DataFrame or array-like): The test features.
        y_test (Series or array-like): The test targets.

    Returns:
        tuple: The mean squared error and R2 score of the model on the test data.
    """
    # Making predictions on the test data
    y_pred = model.predict(X_test)
    
    # Calculating Mean Squared Error and R2 Score
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Log training results to the database
    log_training_results(mse, r2)

    return mse, r2

def log_training_results(mse, r2):
    """
    Log the training results to the SQLite database.

    Args:
        mse (float): The mean squared error of the model.
        r2 (float): The R2 score of the model.
    """
    # Use an absolute path for the database
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'BDD', 'model_logs.db')
    
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO training_logs (datetime, model_type, mse, r2) VALUES (datetime('now'), ?, ?, ?)", 
              ('Ridge', mse, r2))
    conn.commit()
    conn.close()

def save_model(model, filename):
    """
    Save the trained model to a file and log it as an artifact in MLflow.

    Args:
        model (Estimator): The trained model.
        filename (str): The file path to save the model.
    """
    # Save the trained model to a file
    joblib.dump(model, filename)
    print(f"Model saved as: {filename}")
    
    # Logging the model file as an artifact in MLflow
    mlflow.log_artifact(filename)

# Example usage:
# Assuming `X` and `y` are your features and target variables loaded elsewhere in your code
if __name__ == "__main__":
    model, X_test, y_test = train_model(X, y)
