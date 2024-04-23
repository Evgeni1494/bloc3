from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd
import joblib
import secrets
import sqlite3

app = FastAPI()

# Configuration OAuth2 avec URL de récupération du token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Simuler une base de données d'utilisateurs
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "secret",
        "token": "secrettoken"
    }
}

# Fonction pour charger le modèle entraîné
def load_model(filepath):
    return joblib.load(filepath)

# Fonction pour charger l'encodeur
def load_encoder(filepath):
    return joblib.load(filepath)

# Modèle Pydantic pour les données d'entrée pour la prédiction
class InputData(BaseModel):
    year: int
    state_name: str
    sector_name: str
    fuel_name: str

def log_prediction(prediction, input_data, user):
    conn = sqlite3.connect('../BDD/model_logs.db')
    c = conn.cursor()
    c.execute("INSERT INTO prediction_logs (datetime, prediction, input_data, user) VALUES (datetime('now'), ?, ?, ?)",
              (prediction, input_data, user))
    conn.commit()
    conn.close()


# Authentifier l'utilisateur et retourner le token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not secrets.compare_digest(form_data.password, user_dict["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict["token"], "token_type": "bearer"}

# Vérifier le token pour accéder à l'endpoint de prédiction
def authenticate_token(token: str = Depends(oauth2_scheme)):
    if not secrets.compare_digest(token, fake_users_db["admin"]["token"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return fake_users_db["admin"]["username"]

@app.post("/predict/")
def predict(data: InputData, user: str = Depends(authenticate_token)):
    model = load_model('../model/trained_model.pkl')
    encoder = load_encoder('../model/encoder.pkl')
    
    input_df = pd.DataFrame([{
        'year': data.year,
        'state-name': data.state_name,
        'sector-name': data.sector_name,
        'fuel-name': data.fuel_name,
        'fuel_sector_interaction': data.fuel_name + "_" + data.sector_name
    }])
    
    features = ['year', 'state-name', 'sector-name', 'fuel-name', 'fuel_sector_interaction']
    X = encoder.transform(input_df[features])
    prediction = model.predict(X)
    
    # Log prediction
    log_prediction(prediction[0], str(input_df.iloc[0].to_dict()), user)
    
    return {"prediction du CO2": prediction[0]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
