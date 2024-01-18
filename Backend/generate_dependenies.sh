#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Create the requirements.txt file
pip freeze > requirements.txt

# Deactivate the virtual environment
deactivate
