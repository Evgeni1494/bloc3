#!/bin/bash

echo "Installing dependencies"
PORT=${PORT:-8000}

pip install -r requirements.txt
echo "Starting application"
gunicorn -k uvicorn.workers.UvicornWorker api.main:app --bind 0.0.0.0:8000
