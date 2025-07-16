#!/bin/bash

echo "Installing dependencies..."
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt
python3.12 -m pip install whitenoise --upgrade

echo "Creating static directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear

echo "Build completed!"
