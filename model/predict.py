import pandas as pd
import joblib
import mlflow

# Fonction pour charger le modèle entraîné
def load_model(filepath):
    """ Charge le modèle entraîné depuis un fichier .pkl. """
    return joblib.load(filepath)

# Fonction pour charger l'encodeur
def load_encoder(filepath):
    """ Charge l'encodeur depuis un fichier .pkl. """
    return joblib.load(filepath)

# Fonction pour créer un DataFrame à partir des entrées utilisateur
def create_input_dataframe():
    """ Crée un DataFrame à partir des entrées utilisateur. """
    year = input("Entrez l'année (par exemple, 2020): ")
    state_name = input("Entrez le nom de l'État (par exemple, California): ")
    sector_name = input("Entrez le nom du secteur (par exemple, Residential): ")
    fuel_name = input("Entrez le nom du combustible (par exemple, Gasoline): ")
    # Création du DataFrame
    data = pd.DataFrame({
        'year': [year],
        'state-name': [state_name],
        'sector-name': [sector_name],
        'fuel-name': [fuel_name],
        'fuel_sector_interaction': [fuel_name + "_" + sector_name]
    })
    return data

# Fonction pour faire des prédictions
def make_prediction(model, encoder, data):
    with mlflow.start_run(run_name="Prediction"):
        features = ['year', 'state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction']
        data = data[features]
        X = encoder.transform(data)
        predictions = model.predict(X)
        mlflow.log_metric("prediction", predictions[0])
        return predictions

# Chargement du modèle et de l'encoder
model_path = 'trained_model.pkl'
encoder_path = 'encoder.pkl'
model = load_model(model_path)
encoder = load_encoder(encoder_path)

# Création de l'entrée utilisateur
input_data = create_input_dataframe()

# Prédiction
predictions = make_prediction(model, encoder, input_data)
print("Prédiction de la valeur :", predictions)
