from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '/home/utilisateur/Documents/Certification_IA/END_Project/bloc3')

from api.main import app


client = TestClient(app)

def test_login():
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_predict():
    token = client.post("/token", data={"username": "admin", "password": "secret"}).json()['access_token']
    response = client.post("/predict", json={"year": 2020, "state_name": "New York", "sector_name": "Transport", "fuel_name": "Gasoline"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "prediction du CO2" in response.json()

