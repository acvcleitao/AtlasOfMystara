#!/bin/bash

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Linux or macOS
# or
# .\venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
