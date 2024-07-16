from io import BytesIO
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
import cv2
import numpy as np
from PIL import Image
from config import create_app, configure_folders, configure_mongo
from schemas import new_map_schema
from data_utils import build_new_map_data
import requests
from bs4 import BeautifulSoup
import pytesseract
print(pytesseract.get_tesseract_version())


load_dotenv()
app = create_app()
NewMapsFolder, ApprovedMapsFolder = configure_folders(app)
mongo = configure_mongo(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEXAGONS_FOLDER = os.path.join(BASE_DIR, 'Hexagons')

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

@app.route('/getHexagonTypes', methods=['GET'])
def get_hexagon_types():
    try:
        # Query the database for distinct hexagon types grouped by author
        pipeline = [
            {
                '$group': {
                    '_id': '$author',
                    'hexTypes': {'$addToSet': '$type'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'author': '$_id',
                    'hexTypes': 1
                }
            }
        ]
        hexagon_types = list(mongo.db.hexagon.aggregate(pipeline))

        # Return the hexagon types grouped by author as a JSON response
        return jsonify({'hexagonTypes': hexagon_types}), 200

    except Exception as e:
        print(f"Error fetching hexagon types: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

def isolate_ocean(image_data, target_color):
    # Convert base64 image data to a NumPy array
    image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of the target color in HSV
    lower_color = np.array([target_color[0] - 10, 100, 100])
    upper_color = np.array([target_color[0] + 10, 255, 255])

    # Create a mask to isolate the target color
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Create a result image that keeps only the target color
    result = cv2.bitwise_and(image, image, mask=mask)

    # Save the result image
    result_path = os.path.join(HEXAGONS_FOLDER, f'isolated_{uuid.uuid4()}.png')
    cv2.imwrite(result_path, result)

    return result_path

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_str_to_tuple(rgb_str):
    rgb_str = rgb_str.strip('rgb() ')
    rgb_tuple = tuple(map(int, rgb_str.split(',')))
    if len(rgb_tuple) != 3:
        raise ValueError(f"Invalid RGB color: {rgb_str}")
    return rgb_tuple

# Route for uploading a new map
@app.route('/uploadMap', methods=['POST'])
def upload_map():
    try:
        # Get form data
        data = request.get_json()

        title = data.get('mapName')
        image_data = data.get('uploadedImage')
        hex_mask_type = data.get('hexMaskType')
        selected_color = data.get('selectedColor')
        combined_image = data.get('combinedImage')

        # Save or process the combined image as needed
        # For now, we'll just save it
        combined_image_path = os.path.join(HEXAGONS_FOLDER, f'combined_{uuid.uuid4()}.png')
        with open(combined_image_path, 'wb') as f:
            f.write(base64.b64decode(combined_image.split(',')[1]))
        

        # Call the isolate_ocean function to isolate ocean color
        processMap(title, image_data, hex_mask_type, selected_color, combined_image)

        # Example response
        response = {
            'message': 'Map uploaded successfully',
            'title': title,
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error uploading map: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

# Process map function
def processMap(title, image_data, hex_mask_type, selected_color, combined_image):
    try:
        if selected_color.startswith('#'):
            # Convert the selected_color from hex to RGB
            selected_color_rgb = hex_to_rgb(selected_color)
        elif selected_color.startswith('rgb'):
            # Convert the selected_color from RGB string to RGB tuple
            selected_color_rgb = rgb_str_to_tuple(selected_color)
        else:
            raise ValueError(f"Invalid color format: {selected_color}")

        # Convert the RGB color to HSV
        selected_color_hsv = cv2.cvtColor(np.uint8([[selected_color_rgb]]), cv2.COLOR_RGB2HSV)[0][0]

        result_path = isolate_ocean(image_data, selected_color_hsv)
        print(f"Isolated ocean image saved at: {result_path}")

        image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))
        text_data = pytesseract.image_to_string(image)

        response = {
            'message': 'Map processed successfully',
            'title': title,
            'hexMaskType': hex_mask_type,
            'selectedColor': selected_color,
            'isolatedColorPath': result_path,  # Include isolated color path in response
            'textData': text_data  # Include OCR text data
        }

        return jsonify(response), 200
    except ValueError as e:
        print(f"Error processing map: {str(e)}")
        return jsonify({'message': str(e)}), 400

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
            map_data['image_url'] = base_image_url + map_data['image_path'].replace('\\', '/').split('/')[-1]

        return jsonify({'maps': new_maps}), 200

    except Exception as e:
        print(f"Error fetching new maps: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

# Serve images statically
@app.route('/static/images/<path:image_filename>')
def serve_image(image_filename):
    return send_from_directory(NewMapsFolder, image_filename)

@app.route('/static/hexagons/<path:image_filename>')
def serve_hexagon(image_filename):
    try:
        return send_from_directory(HEXAGONS_FOLDER, image_filename)
    except FileNotFoundError:
        return 'Image not found', 404

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
            map_data['image_url'] = base_image_url + map_data['image_path'].replace('\\', '/').split('/')[-1]
            return jsonify({'map': map_data}), 200
        else:
            print(f"Map not found for ID: {id}")
            return jsonify({'message': 'Map not found'}), 404

    except Exception as e:
        print(f"Error fetching map details: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/hexagons/<author>/<hex_type>')
def get_hexagon_image(author, hex_type):
    hexagon_path = os.path.join(HEXAGONS_FOLDER, author)
    # Find the correct filename by checking all possible extensions
    for extension in ['.png', '.jpg', '.jpeg', '.gif']:  # Add more if needed
        filename = f"{hex_type}{extension}"
        if os.path.exists(os.path.join(hexagon_path, filename)):
            return send_from_directory(hexagon_path, filename)
    # If none of the extensions exist, return 404
    return 'Image not found', 404

# Route for getting hexagons based on zoom level, author, and coordinates
@app.route('/getHexagons', methods=['GET'])
def get_hexagons():
    try:
        # Get query parameters from the request
        zoom_level = int(request.args.get('zoomLevel'))
        author = request.args.get('author')
        top_left = list(map(float, request.args.get('topLeft').split(',')))
        bottom_right = list(map(float, request.args.get('bottomRight').split(',')))

        # Separate coordinates
        top_left_x, top_left_y = top_left
        bottom_right_x, bottom_right_y = bottom_right

        # Query the database for hexagons based on the provided parameters
        # If author is not given it searches for all authors
        if author == "":
            hexagons = list(mongo.db.hexagon.find({
                'zoomLevel': zoom_level,
                '$and': [
                    {'x_coordinate': {'$gte': top_left_x, '$lte': bottom_right_x}},
                    {'y_coordinate': {'$gte': top_left_y, '$lte': bottom_right_y}}
                ]
            }))
        else:
            hexagons = list(mongo.db.hexagon.find({
                'zoomLevel': zoom_level,
                'author': author,
                '$and': [
                    {'x_coordinate': {'$gte': top_left_x, '$lte': bottom_right_x}},
                    {'y_coordinate': {'$gte': top_left_y, '$lte': bottom_right_y}}
                ]
            }))

        # Group hexagons by type
        grouped_hexagons = {}
        for hexagon in hexagons:
            hex_type = hexagon['type']
            if hex_type not in grouped_hexagons:
                grouped_hexagons[hex_type] = {'coordinates': [], 'imageURL': hexagon['imageUrl']}
            grouped_hexagons[hex_type]['coordinates'].append((hexagon['x_coordinate'], hexagon['y_coordinate']))

        # Format the grouped hexagons into the desired structure
        formatted_hexagons = [{'type': hex_type, 'coordinates': group['coordinates'], 'imageURL': group['imageURL']} for hex_type, group in grouped_hexagons.items()]
        print(formatted_hexagons)
        # Return the formatted hexagons as a JSON response
        return jsonify({'hexagons': formatted_hexagons}), 200

    except Exception as e:
        print(f"Error fetching hexagons: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/updateHexType', methods=['POST'])
def update_hex_type():
    try:
        data = request.get_json()
        hex_id = data.get('hexId')
        new_hex_type = data.get('hexType')

        # Extract the hexagon properties from the hex_id
        author, zoom_level, x, y = hex_id.split('_')
        zoom_level = int(zoom_level)
        x = float(x)
        y = float(y)

        # Update the hexagon in the database
        result = mongo.db.hexagon.update_one(
            {'author': author, 'zoomLevel': zoom_level, 'x_coordinate': x, 'y_coordinate': y},
            {'$set': {'type': new_hex_type}}
        )

        if result.matched_count == 0:
            return jsonify({'message': 'Hexagon not found'}), 404

        return jsonify({'message': 'Hexagon updated successfully'}), 200

    except Exception as e:
        print(f"Error updating hexagon type: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

# Find map information for a place in Mystara
def find_mystara_info(place):
    try:
        # Construct the URLs for the main Atlas page, Maps page, and search
        atlas_url = "https://www.pandius.com/atlas.html"
        maps_url = "https://www.pandius.com/maps.html"
        search_url = f"https://www.pandius.com/search.html?q={place}&s=Search"
        
        # Send a GET request to the Atlas page
        atlas_response = requests.get(atlas_url)
        
        # Check if the request to the Atlas page was successful
        if atlas_response.status_code == 200:
            # Parse the HTML content of the Atlas page
            atlas_soup = BeautifulSoup(atlas_response.content, 'html.parser')
            
            # Search for the place name in the Atlas page
            atlas_result = atlas_soup.find('a', string=place)
            
            # If the place is found in the Atlas page, return the URL
            if atlas_result:
                return f"More information: {atlas_result['href']}"
            
        # If the place is not found in the Atlas page, proceed to the Maps page
        maps_response = requests.get(maps_url)
        
        # Check if the request to the Maps page was successful
        if maps_response.status_code == 200:
            # Parse the HTML content of the Maps page
            maps_soup = BeautifulSoup(maps_response.content, 'html.parser')
            
            # Search for the place name in the Maps page
            maps_result = maps_soup.find('a', string=place)
            
            # If the place is found in the Maps page, return the URL
            if maps_result:
                return f"More information: {maps_result['href']}"
        
        # If the place is not found in both the Atlas and Maps pages, use the search
        search_response = requests.get(search_url)
        
        # Check if the request to the search page was successful
        if search_response.status_code == 200:
            # Parse the HTML content of the search page
            search_soup = BeautifulSoup(search_response.content, 'html.parser')
            
            # Find relevant information in the search results
            results = search_soup.find_all('div', class_='Result')
            
            # Check if there are any results
            if results:
                # Extract the first result
                first_result = results[0]
                
                # Extract the title and URL
                title = first_result.find('a').text.strip()
                url = first_result.find('a')['href']
                
                return f"Title: {title}\nMore information: {url}"
            
        return "No information found for that place."

    except Exception as e:
        print(f"Error finding map information for place {place}: {str(e)}")
        return None

# Route for getting details of a specific map
@app.route('/getMapFromVault/<place>', methods=['GET'])
def get_map_from_vault(place):
    try:
        print(f"Received place: {place}")

        # Call the find_mystara_info function to search for map information based on the provided place
        map_info = find_mystara_info(place)
        
        if map_info:
            # Return the map information as JSON response
            return jsonify({'map_info': map_info}), 200
        else:
            print(f"No map information found for place: {place}")
            return jsonify({'message': 'Map information not found'}), 404

    except Exception as e:
        print(f"Error fetching map details: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/getAuthors', methods=['GET'])
def get_authors():
    try:
        authors = list(mongo.db.authors.find({}, {'_id': 0, 'name': 1}))
        author_names = [author['name'] for author in authors]
        return jsonify({'authors': author_names}), 200
    except Exception as e:
        print(f"Error fetching authors: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500
    

if __name__ == '__main__':
    # For development with Flask's built-in server
    app.run(debug=True)
else:
    # For Gunicorn deployment
    gunicorn_cmd = f"gunicorn -c gunicorn_config.py AtlasBackend:app"
    os.system(gunicorn_cmd)

