#!/bin/bash
PORT=${PORT:-8000}
pip install -r requirements.txt
gunicorn -k uvicorn.workers.UvicornWorker api.main:app --bind 0.0.0.0:$PORT
