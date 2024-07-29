import pandas as pd
from scipy import stats
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
import mlflow

def load_data(filepath):
    """
    Load data from a CSV file.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        DataFrame: The loaded data.
    """
    return pd.read_csv(filepath)

def remove_outliers(data, column):
    """
    Remove outliers from a specified column in the data.

    Args:
        data (DataFrame): The data from which to remove outliers.
        column (str): The column name from which to remove outliers.

    Returns:
        DataFrame: The data with outliers removed.
    """
    return data[(abs(stats.zscore(data[column])) < 3)]

def add_interactions(data, col1, col2, new_col_name):
    """
    Add an interaction column between two features.

    Args:
        data (DataFrame): The data to which the interaction column will be added.
        col1 (str): The first column for the interaction.
        col2 (str): The second column for the interaction.
        new_col_name (str): The name of the new interaction column.

    Returns:
        DataFrame: The data with the added interaction column.
    """
    data[new_col_name] = data[col1] + "_" + data[col2]
    return data

def encode_features(data, categorical_features):
    """
    One-hot encode categorical variables and return the fitted encoder along with the transformed data.

    Args:
        data (DataFrame): The data containing categorical features.
        categorical_features (list): A list of column names to be one-hot encoded.

    Returns:
        tuple: A tuple containing the transformed data and the fitted encoder.
    """
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')
    transformer = ColumnTransformer(transformers=[('cat', one_hot_encoder, categorical_features)], remainder='passthrough')
    transformed_data = transformer.fit_transform(data)
    return transformed_data, transformer

def prepare_data(filepath):
    """
    Prepare the data by loading it, removing outliers, adding interaction columns, and encoding categorical features.
    The transformer is saved as a pickle file and logged with MLflow.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        DataFrame: The final prepared data.
    """
    with mlflow.start_run(run_name="Data Preparation"):
        data = load_data(filepath)
        data = remove_outliers(data, 'value')
        data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
        final_data, transformer = encode_features(data, ['state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction'])
        
        # Log transformer
        joblib.dump(transformer, 'encoder.pkl')
        mlflow.log_artifact('encoder.pkl')
        
        return final_data
