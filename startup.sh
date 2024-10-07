#!/bin/bash

echo "Installing dependencies"
pip install -r requirements.txt

# Utilisation de la variable d'environnement PORT fournie par Azure
echo "Starting application on port $PORT"
gunicorn -k uvicorn.workers.UvicornWorker api.main:app --bind 0.0.0.0:$PORT
