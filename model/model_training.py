from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib 

def train_model(data, target):
    """ Entraîne un modèle Ridge sur les données fournies. """
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=0)
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    """ Évalue le modèle sur l'ensemble de test. """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

def save_model(model, filename):
    """ Sauvegarde le modèle entraîné en format .pkl. """
    joblib.dump(model, filename)
    print(f"Modèle sauvegardé sous : {filename}")