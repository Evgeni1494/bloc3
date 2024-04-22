from data_preparation import *
from model_training import *

# Chemin vers le fichier de données
data_path = '../archive/emissions.csv'

# Processus complet
data = load_data(data_path)
data = remove_outliers(data, 'value')
data = add_interactions(data, 'fuel-name', 'sector-name', 'fuel_sector_interaction')
features = ['year', 'state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction']
X, encoder = encode_features(data[features], features)  # Notez que l'on récupère l'encoder ici
y = data['value']

model, X_test, y_test = train_model(X, y)
mse, r2 = evaluate_model(model, X_test, y_test)
print(f"MSE: {mse}, R²: {r2}")

save_model(model, 'trained_model.pkl')
joblib.dump(encoder, 'encoder.pkl')  # Sauvegarde de l'encoder
