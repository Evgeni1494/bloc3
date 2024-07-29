from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd
import joblib
import secrets
import sqlite3
import os

app = FastAPI()

# OAuth2 configuration with token retrieval URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Simulate a user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "secret",
        "token": "secrettoken"
    }
}

def load_model(filepath):
    """
    Load a trained model from a file.

    Args:
        filepath (str): Path to the model file.

    Returns:
        The loaded model.
    """
    return joblib.load(os.path.join(os.path.dirname(__file__), '..', filepath))

def load_encoder(filepath):
    """
    Load an encoder from a file.

    Args:
        filepath (str): Path to the encoder file.

    Returns:
        The loaded encoder.
    """
    return joblib.load(os.path.join(os.path.dirname(__file__), '..', filepath))

class InputData(BaseModel):
    """
    Pydantic model for input data for prediction.

    Attributes:
        year (int): The year.
        state_name (str): The name of the state.
        sector_name (str): The name of the sector.
        fuel_name (str): The name of the fuel.
    """
    year: int
    state_name: str
    sector_name: str
    fuel_name: str

def log_prediction(prediction, input_data, user):
    """
    Log the prediction to the database.

    Args:
        prediction (float): The prediction result.
        input_data (str): The input data used for prediction.
        user (str): The user who made the prediction.
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'BDD', 'model_logs.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO prediction_logs (datetime, prediction, input_data, user) VALUES (datetime('now'), ?, ?, ?)",
              (prediction, input_data, user))
    conn.commit()
    conn.close()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate the user and return a token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.

    Returns:
        dict: The access token and token type.
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not secrets.compare_digest(form_data.password, user_dict["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict["token"], "token_type": "bearer"}

def authenticate_token(token: str = Depends(oauth2_scheme)):
    """
    Verify the token to access the prediction endpoint.

    Args:
        token (str): The OAuth2 token.

    Returns:
        str: The username if the token is valid.

    Raises:
        HTTPException: If the token is invalid.
    """
    if not secrets.compare_digest(token, fake_users_db["admin"]["token"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return fake_users_db["admin"]["username"]

@app.post("/predict/")
def predict(data: InputData, user: str = Depends(authenticate_token)):
    """
    Make a CO2 prediction based on the input data.

    Args:
        data (InputData): The input data for the prediction.
        user (str): The authenticated user.

    Returns:
        dict: The CO2 prediction result.
    """
    model = load_model('model/trained_model.pkl')
    encoder = load_encoder('model/encoder.pkl')
    
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
