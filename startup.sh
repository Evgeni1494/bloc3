#!/bin/bash

echo "Installing dependencies"
pip install -r requirements.txt

echo "Starting application with Uvicorn"
uvicorn api.main:app --host 0.0.0.0 --port $PORT --log-level debug
