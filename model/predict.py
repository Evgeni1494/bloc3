import pandas as pd
import joblib
import mlflow

def load_model(filepath):
    """
    Load the trained model from a .pkl file.

    Args:
        filepath (str): The path to the model file.

    Returns:
        The loaded model.
    """
    return joblib.load(filepath)

def load_encoder(filepath):
    """
    Load the encoder from a .pkl file.

    Args:
        filepath (str): The path to the encoder file.

    Returns:
        The loaded encoder.
    """
    return joblib.load(filepath)

def create_input_dataframe():
    """
    Create a DataFrame from user inputs.

    Returns:
        DataFrame: The created DataFrame with user input data.
    """
    year = input("Enter the year (e.g., 2020): ")
    state_name = input("Enter the state name (e.g., California): ")
    sector_name = input("Enter the sector name (e.g., Residential): ")
    fuel_name = input("Enter the fuel name (e.g., Gasoline): ")

    # Create the DataFrame
    data = pd.DataFrame({
        'year': [year],
        'state-name': [state_name],
        'sector-name': [sector_name],
        'fuel-name': [fuel_name],
        'fuel_sector_interaction': [fuel_name + "_" + sector_name]
    })
    return data

def make_prediction(model, encoder, data):
    """
    Make predictions using the trained model and encoder.

    Args:
        model: The trained model.
        encoder: The encoder used for preprocessing.
        data (DataFrame): The input data for making predictions.

    Returns:
        array: The predictions made by the model.
    """
    with mlflow.start_run(run_name="Prediction"):
        features = ['year', 'state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction']
        data = data[features]
        X = encoder.transform(data)
        predictions = model.predict(X)
        mlflow.log_metric("prediction", predictions[0])
        return predictions

# Load the model and the encoder
model_path = 'trained_model.pkl'
encoder_path = 'encoder.pkl'
model = load_model(model_path)
encoder = load_encoder(encoder_path)

# Create user input DataFrame
input_data = create_input_dataframe()

# Make prediction
predictions = make_prediction(model, encoder, input_data)
print("Predicted value:", predictions[0])
