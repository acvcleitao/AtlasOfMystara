import os
import uuid
import base64
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
import bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime
import jsonschema
import sys
from config import create_app, configure_folders, configure_mongo
from schemas import new_map_schema
from data_utils import build_new_map_data

load_dotenv()
app = create_app()
NewMapsFolder, ApprovedMapsFolder = configure_folders(app)
mongo = configure_mongo(app)

# Root URL
@app.route('/')
def hello():
    return jsonify(message='Hello, Flask is running!')

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Use 'users_collection' instead of 'User'
    user = mongo.db.users.find_one({'username': username})

    if user:
        # Print debug information
        print(f"Stored Password: {user['password']}")
        print(f"Entered Password: {bcrypt.hashpw(password.encode('utf-8'), user['salt'])}")

        if bcrypt.checkpw(password.encode('utf-8'), user['password']):

            response_data = {
                'message': 'Login successful',
            }
            return jsonify(response_data), 200
        else:
            return jsonify({'message': 'Invalid password'}), 401

    return jsonify({'message': 'Invalid username or password'}), 401

# Get the new maps count
@app.route('/getNewMapsCount', methods=['GET'])
def get_new_maps_count():
    # Count the number of new maps in the collection
    new_maps_count = mongo.db.new_maps.count_documents({})
    return jsonify({'newMapsCount': new_maps_count}), 200


# Route for uploading a new map
@app.route('/uploadMap', methods=['POST'])
def upload_map():
    try:
        # Get form data
        title = request.form.get('title')
        image_data = request.form.get('image')

        # Build map data and validate against the schema
        map_data = build_new_map_data(title, image_data, NewMapsFolder)

        # Insert map data into the 'new_maps' collection
        mongo.db.new_maps.insert_one(map_data)

        return jsonify({'message': 'Map Uploaded Successfully'}), 200

    except jsonschema.ValidationError as e:
        return jsonify({'message': f'Invalid Data: {e.message}'}), 400

    except Exception as e:
        print(f"Error uploading map: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500
    

# Route for getting the list of new maps
@app.route('/getNewMaps', methods=['GET'])
def get_new_maps():
    try:
        # Retrieve the list of new maps from the 'new_maps' collection
        new_maps = list(mongo.db.new_maps.find({}, {'_id': 0}))
        return jsonify({'maps': new_maps}), 200
    except Exception as e:
        print(f"Error fetching new maps: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500


# Route for getting new maps with URL
@app.route('/getNewMapsWithURL', methods=['GET'])
def get_new_maps_with_url():
    try:
        # Fetch all new maps from the 'new_maps' collection
        new_maps_cursor = mongo.db.new_maps.find()

        # Convert cursor to a list of dictionaries
        new_maps = list(new_maps_cursor)

        # Add '_id' field to each map
        for map_data in new_maps:
            map_data['_id'] = str(map_data['_id'])  # Convert ObjectId to string

        # Build URLs for images
        base_image_url = "http://127.0.0.1:5000/static/images/"
        for map_data in new_maps:
            map_data['image_url'] = f"{base_image_url}{map_data['image_path'].replace('\\', '/').split('/')[-1]}"

        return jsonify({'maps': new_maps}), 200

    except Exception as e:
        print(f"Error fetching new maps: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500



# Serve images statically
@app.route('/static/images/<path:image_filename>')
def serve_image(image_filename):
    return send_from_directory(NewMapsFolder, image_filename)

# Route for getting details of a specific map
@app.route('/getMapDetails/<id>', methods=['GET'])
def get_map_details(id):
    try:
        print(f"Received map ID: {id}")

        # Convert the received ID to ObjectId
        map_id = ObjectId(id)
        
        # Find the map in the 'new_maps' collection based on the provided ID
        map_data = mongo.db.new_maps.find_one({'_id': map_id})
        
        if map_data:
            # Convert ObjectId to string
            map_data['_id'] = str(map_data['_id'])
            # Build URL for image
            base_image_url = "http://127.0.0.1:5000/static/images/"
            map_data['image_url'] = f"{base_image_url}{map_data['image_path'].replace('\\', '/').split('/')[-1]}"
            return jsonify({'map': map_data}), 200
        else:
            print(f"Map not found for ID: {id}")
            return jsonify({'message': 'Map not found'}), 404

    except Exception as e:
        print(f"Error fetching map details: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500



if __name__ == '__main__':
    # For development with Flask's built-in server
    app.run(debug=True)
else:
    # For Gunicorn deployment
    gunicorn_cmd = f"gunicorn -c gunicorn_config.py AtlasBackend:app"
    os.system(gunicorn_cmd)

