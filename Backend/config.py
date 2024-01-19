import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Set the MongoDB URI from the environment variable
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")
    return app

def configure_folders(app):
    # Create a folder named 'NewMaps' within the backend's folder
    NewMapsFolder = os.path.join(os.path.dirname(__file__), 'NewMaps')
    os.makedirs(NewMapsFolder, exist_ok=True)
    ApprovedMapsFolder = os.path.join(os.path.dirname(__file__), 'ApprovedMaps')
    os.makedirs(ApprovedMapsFolder, exist_ok=True)

    return NewMapsFolder, ApprovedMapsFolder

def configure_mongo(app):
    mongo = PyMongo(app)
    return mongo
