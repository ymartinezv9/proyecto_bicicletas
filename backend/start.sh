#!/bin/bash
export FLASK_APP=backend/server.py
export FLASK_ENV=production
flask run --host=0.0.0.0 --port=$PORT
