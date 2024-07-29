from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '/home/utilisateur/Documents/Certification_IA/END_Project/bloc3')

from api.main import app

client = TestClient(app)

def test_login():
    """
    Test the login endpoint to obtain an access token.

    This test sends a POST request to the /token endpoint with valid user credentials
    and verifies that the response status is 200 and contains an access token.
    """
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_predict():
    """
    Test the predict endpoint to make a CO2 prediction.

    This test first obtains an access token by logging in with valid user credentials.
    Then, it sends a POST request to the /predict endpoint with the required prediction
    parameters and the access token in the authorization header. It verifies that the
    response status is 200 and contains a prediction result.
    """
    token = client.post("/token", data={"username": "admin", "password": "secret"}).json()['access_token']
    response = client.post("/predict", json={"year": 2020, "state_name": "New York", "sector_name": "Transport", "fuel_name": "Gasoline"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "prediction du CO2" in response.json()
