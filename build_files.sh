#!/bin/bash
echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.12 -m venv venv

# activate the virtual environment
source venv/bin/activate
# Install Python dependencies
pip install -r requirements.txt

# Run the Flask app to ensure it works
python app.py
echo "BUILD END"