#!/bin/bash

# Install required system packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment (for Windows)
source venv/Scripts/activate

# Install Python dependencies
pip install flask flask-cors flask-pymongo python-dotenv bcrypt requests beautifulsoup4 pymongo jsonschema

# Install MongoDB (if needed)
# Add instructions to install MongoDB if it's a dependency

# Run Flask app
echo "App setup complete. You can now run the Flask app using 'flask run' command."
