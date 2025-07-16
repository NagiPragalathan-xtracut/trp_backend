#!/bin/bash
# Make script executable
chmod +x build_files.sh

echo "Installing dependencies..."
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt

echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear

echo "Build completed!"
