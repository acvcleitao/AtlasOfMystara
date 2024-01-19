import os
import uuid
import base64
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set the MongoDB URI from the environment variable
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
# Create a folder named 'NewMaps' within the backend's folder
NewMapsFolder = os.path.join(os.path.dirname(__file__), 'NewMaps')
os.makedirs(NewMapsFolder, exist_ok=True)
ApprovedMapsFolder = os.path.join(os.path.dirname(__file__), 'ApprovedMaps')
os.makedirs(NewMapsFolder, exist_ok=True)

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

        # Validate the input
        if not title or not image_data:
            return jsonify({'message': 'Title and image are required'}), 400

        # Decode base64 string and save the image to the server
        unique_identifier = str(uuid.uuid4())
        filename = secure_filename(f"{unique_identifier}_map.png")
        filepath = os.path.join(NewMapsFolder, filename)

        # Remove the 'data:image/png;base64,' prefix
        image_data = image_data.split(',')[1]
        image_binary = base64.b64decode(image_data)

        # Save the image to the server
        with open(filepath, 'wb') as file:
            file.write(image_binary)

        # Insert map data into the 'new_maps' collection
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        map_data = {
            'title': title,
            'image_path': filepath,
            'timestamp': timestamp,
        }
        mongo.db.new_maps.insert_one(map_data)

        return jsonify({'message': 'Map Uploaded Successfully'}), 200

    except Exception as e:
        print(f"Error uploading map: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    # For development with Flask's built-in server
    app.run(debug=True)
else:
    # For Gunicorn deployment
    gunicorn_cmd = f"gunicorn -c gunicorn_config.py AtlasBackend:app"
    os.system(gunicorn_cmd)
