import pandas as pd
from scipy import stats
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
import mlflow

def load_data(filepath):
    """ Charge les données depuis un fichier CSV. """
    return pd.read_csv(filepath)

def remove_outliers(data, column):
    """ Élimine les valeurs aberrantes d'une colonne spécifiée. """
    return data[(abs(stats.zscore(data[column])) < 3)]

def add_interactions(data, col1, col2, new_col_name):
    """ Ajoute une colonne d'interaction entre deux caractéristiques. """
    data[new_col_name] = data[col1] + "_" + data[col2]
    return data

def encode_features(data, categorical_features):
    """ Encodage One-hot des variables catégorielles et retourne l'encoder ajusté avec les données transformées. """
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')
    transformer = ColumnTransformer(transformers=[('cat', one_hot_encoder, categorical_features)], remainder='passthrough')
    transformed_data = transformer.fit_transform(data)
    return transformed_data, transformer


def prepare_data(filepath):
    with mlflow.start_run(run_name="Data Preparation"):
        data = load_data(filepath)
        data = remove_outliers(data, 'value')
        data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
        final_data, transformer = encode_features(data, ['state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction'])
        
        # Log transformer
        joblib.dump(transformer, 'encoder.pkl')
        mlflow.log_artifact('encoder.pkl')
        
        return final_data
