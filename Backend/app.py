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
from skimage.metrics import structural_similarity as ssim # type: ignore
import pytesseract
# print(pytesseract.get_tesseract_version())


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
        author = data.get('mapAuthor')
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
        processMap(title, author, image_data, hex_mask_type, selected_color, combined_image)

        # Example response
        response = {
            'message': 'Map uploaded successfully',
            'title': title,
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error uploading map: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500


def processMap(title, author, image_data, hex_mask_type, selected_color, combined_image):
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
        # text_data = pytesseract.image_to_string(image)

        # Convert the combined_image from base64 to a NumPy array
        combined_image_data = base64.b64decode(combined_image.split(',')[1])
        combined_image_array = np.frombuffer(combined_image_data, np.uint8)
        combined_image = cv2.imdecode(combined_image_array, cv2.IMREAD_COLOR)
        if combined_image is None:
            raise ValueError("Failed to load the combined image")

        # Hexagonal grid processing
        # Grid color is BGR (160, 0, 0)
        grid_color_bgr = [160, 0, 0]
        
        # Detect hexagonal grid in the combined image
        mask = find_hexagonal_grid(combined_image, grid_color_bgr)
        
        # Automatically detect the radius of the hexagons
        hexagon_radius = get_hexagon_radius(mask)
        
        # Extract hexagons from the image
        hexagons = extract_hexagons(combined_image, mask)

        processedHexagons = processHexagons(hexagons, author)
        
        # Save the hexagons
        # TODO: delete this and the related function
        # save_hexagons(hexagons)

        response = {
            'message': 'Map processed successfully',
            'title': title,
            'hexMaskType': hex_mask_type,
            'selectedColor': selected_color,
            'isolatedColorPath': result_path,  # Include isolated color path in response
            # 'textData': text_data  # Include OCR text data
        }

        return jsonify(response), 200
    except ValueError as e:
        print(f"Error processing map: {str(e)}")
        return jsonify({'message': str(e)}), 400

def find_hexagonal_grid(image, target_color):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Convert target RGB color to HSV
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]
    
    # Create a range for the target color
    lower_color = np.array([target_color_hsv[0] - 10, 100, 100])
    upper_color = np.array([target_color_hsv[0] + 10, 255, 255])
    
    # Create a binary mask where the colors within the range are white
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    return mask

def get_hexagon_radius(mask):
    # Find contours of the hexagonal grid
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a copy of the mask image for visualization
    mask_with_contours = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Draw all contours on the mask image (for visualization)
    cv2.drawContours(mask_with_contours, contours, -1, (0, 255, 0), 2)  # Draw all contours in green with thickness 2
    
    # Calculate the radius from the bounding boxes
    radii = []
    for contour in contours:
        _, _, w, h = cv2.boundingRect(contour)
        radius = min(w, h) / 2
        radii.append(radius)
    
    # Find the most common radius
    radius_counts = np.bincount(np.round(radii).astype(int))
    most_common_radius = np.argmax(radius_counts)
    
    return most_common_radius

def extract_hexagons(image, mask):
    # Find contours of the hexagonal grid
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    hexagons = []
    for contour in contours:
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Create a mask for the hexagon
        hex_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.drawContours(hex_mask, [contour - [x, y]], -1, 1, -1)
        
        # Apply the hexagonal mask to the image
        hex_image = cv2.bitwise_and(image[y:y+h, x:x+w], image[y:y+h, x:x+w], mask=hex_mask)
        
        # Make the background transparent
        hex_image = cv2.cvtColor(hex_image, cv2.COLOR_BGR2BGRA)
        hex_image[:, :, 3] = hex_mask * 255
        
        hexagons.append(hex_image)
    
    return hexagons

def save_hexagons(hexagons):
    save_directory = os.path.join(os.getcwd(), 'Hexagons', 'Temp')
    os.makedirs(save_directory, exist_ok=True)  # Ensure the directory exists
    
    for i, hex_img in enumerate(hexagons):
        file_path = os.path.join(save_directory, f'hexagon_{i}.png')
        cv2.imwrite(file_path, hex_img)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_str_to_tuple(rgb_str):
    rgb_str = rgb_str.strip('rgb() ')
    return tuple(map(int, rgb_str.split(',')))


def processHexagons(hexagon_images, author):
    # hexagon_images is a list of hexagons to be processed
    # each author should, idealy have its own tile set which corresponds to a folder

    author_folder = findAuthorFolder(author)

    # Save each hexagon image into the author's folder
    for idx, hexagon_image in enumerate(hexagon_images):
        image_path = os.path.join(author_folder, f'hexagon_{idx}.png')
        cv2.imwrite(image_path, hexagon_image)
        print(f"Saved hexagon image {idx} for author {author} at {image_path}")
        MSE_results = processHexagonMSE(hexagon_image, author)        # Mean Square Error approach
        PSNR_results = processHexagonPSNR(hexagon_image, author)       # Peak Signal to Noise Ratio approach
        SSIM_results = processHexagonSSIM(hexagon_image, author)       # Structural Similarity Index approach
        NN_results = processHexagonNN(hexagon_image, author)         # Neural Network approach TODO: Implement this

def processHexagonMSE(hexagon_image, author):
    # Store the MSE values for all images in the folder
    mse_values = []
    author_folder = findAuthorFolder(author)
    
    # Iterate over all files in the folder
    for filename in os.listdir(author_folder):
        file_path = os.path.join(author_folder, filename)
        
        try:
            # Load the current image
            current_image = load_image(file_path)
            
            # Resize images if necessary to ensure they have the same dimensions
            if hexagon_image.shape != current_image.shape:
                current_image = cv2.resize(current_image, (hexagon_image.shape[1], hexagon_image.shape[0]))
            
            # Calculate the MSE
            error = mse(hexagon_image, current_image)
            
            # Append the result
            mse_values.append((filename, error))
        except Exception as e:
            print(f"Could not process file {file_path}: {e}")
    
    # Sort the MSE values in ascending order (lower MSE means more similar)
    mse_values.sort(key=lambda x: x[1])
    
    # Return the top 5 most similar images
    return mse_values[:5]

def mse(imageA, imageB):
    # Ensure the images have the same dimensions
    if imageA.shape != imageB.shape:
        raise ValueError("Images must have the same dimensions for MSE calculation")
    
    # Calculate the Mean Squared Error between the two images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1] * imageA.shape[2])
    
    return err

def load_image(image_path):
    # Load the image from the specified path
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"No image found at {image_path}")
    
    return image

def processHexagonPSNR(hexagon_image, author):
    # Store the PSNR values for all images in the folder
    psnr_values = []
    author_folder = findAuthorFolder(author)
    
    # Iterate over all files in the folder
    for filename in os.listdir(author_folder):
        file_path = os.path.join(author_folder, filename)
        
        try:
            # Load the current image
            current_image = load_image(file_path)
            
            # Resize images if necessary to ensure they have the same dimensions
            if hexagon_image.shape != current_image.shape:
                current_image = cv2.resize(current_image, (hexagon_image.shape[1], hexagon_image.shape[0]))
            
            # Calculate the PSNR
            similarity = psnr(hexagon_image, current_image)
            
            # Append the result
            psnr_values.append((filename, similarity))
        except Exception as e:
            print(f"Could not process file {file_path}: {e}")
    
    # Sort the PSNR values in descending order (higher PSNR means more similar)
    psnr_values.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top 5 most similar images
    return psnr_values[:5]

def psnr(imageA, imageB):
    # Ensure the images have the same dimensions
    if imageA.shape != imageB.shape:
        raise ValueError("Images must have the same dimensions for PSNR calculation")
    
    mse = np.mean((imageA - imageB) ** 2)
    if mse == 0:
        return float('inf')  # PSNR is infinite if there is no noise
    
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

def processHexagonSSIM(hexagon_image, author):
    # Store the SSIM values for all images in the folder
    ssim_values = []
    author_folder = findAuthorFolder(author)

    # Iterate over all files in the folder
    for filename in os.listdir(author_folder):
        file_path = os.path.join(author_folder, filename)
        
        try:
            # Load the current image
            current_image = load_image(file_path)
            
            # Convert the current image to grayscale if it's not already
            if current_image.shape[2] == 4:  # Check if the image has an alpha channel
                current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGRA2GRAY)
            else:
                current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
            
            # Resize images if necessary to ensure they have the same dimensions
            if hexagon_image.shape != current_image_gray.shape:
                current_image_gray = cv2.resize(current_image_gray, (hexagon_image.shape[1], hexagon_image.shape[0]))
            
            # Calculate the SSIM
            similarity = ssim(hexagon_image, current_image_gray)
            
            # Append the result
            ssim_values.append((filename, similarity))
        except Exception as e:
            print(f"Could not process file {file_path}: {e}")
    
    # Sort the SSIM values in descending order (higher SSIM means more similar)
    ssim_values.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top 5 most similar images
    return ssim_values[:5]

def processHexagonNN(hexagon_image, author):
    return "Not Yet Implemented"


def sift_features(image):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors

def compare_sift_color(image, folder_path):
    kp1, des1 = sift_features(image)
    bf = cv2.BFMatcher()
    matches_dict = {}
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        current_image = cv2.imread(file_path)
        kp2, des2 = sift_features(current_image)
        
        if des2 is not None and des1 is not None:
            matches = bf.knnMatch(des1, des2, k=2)
            good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
            matches_dict[filename] = len(good_matches)
    
    sorted_matches = sorted(matches_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_matches[:5]

def surf_features(image):
    surf = cv2.xfeatures2d.SURF_create()
    keypoints, descriptors = surf.detectAndCompute(image, None)
    return keypoints, descriptors

def compare_surf_color(image, folder_path):
    kp1, des1 = surf_features(image)
    bf = cv2.BFMatcher()
    matches_dict = {}
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        current_image = cv2.imread(file_path)
        kp2, des2 = surf_features(current_image)
        
        if des2 is not None and des1 is not None:
            matches = bf.knnMatch(des1, des2, k=2)
            good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
            matches_dict[filename] = len(good_matches)
    
    sorted_matches = sorted(matches_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_matches[:5]

def orb_features(image):
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return keypoints, descriptors

def compare_orb_color(image, folder_path):
    kp1, des1 = orb_features(image)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches_dict = {}
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        current_image = cv2.imread(file_path)
        kp2, des2 = orb_features(current_image)
        
        if des2 is not None and des1 is not None:
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)
            matches_dict[filename] = len(matches)
    
    sorted_matches = sorted(matches_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_matches[:5]



def findAuthorFolder(author):
    # Normalize author name to lowercase for case insensitivity
    author_lower = author.lower()
    
    # Path to the main "Hexagons" folder
    hexagons_folder = os.path.join(os.getcwd(), 'Hexagons')
    
    # Flag to track if we found a matching folder directly
    found_direct_match = False
    
    # Iterate over folders in the "Hexagons" directory
    for folder_name in os.listdir(hexagons_folder):
        folder_path = os.path.join(hexagons_folder, folder_name)
        if os.path.isdir(folder_path):
            # Check if the folder name matches the author directly
            if folder_name.lower() == author_lower:
                author_folder = folder_path
                found_direct_match = True
                break
    
    # If no direct match was found, check aliases
    if not found_direct_match:
        for folder_name in os.listdir(hexagons_folder):
            folder_path = os.path.join(hexagons_folder, folder_name)
            if os.path.isdir(folder_path):
                # Check if the folder has an alias.txt file and if author matches any alias
                if check_alias(folder_path, author_lower):
                    author_folder = folder_path
                    break
        else:
            # If no matching author folder or alias folder is found, create a new one
            author_folder = os.path.join(hexagons_folder, author_lower)
            os.makedirs(author_folder)

    return author_folder

def check_alias(folder_path, author_lower):
    # Check if alias.txt exists in the folder
    alias_file = os.path.join(folder_path, 'alias.txt')
    if not os.path.isfile(alias_file):
        return False
    
    # Read aliases from alias.txt
    with open(alias_file, 'r') as f:
        aliases = [alias.strip().lower() for alias in f.readlines()]
    
    # Check if author_lower matches any alias
    return author_lower in aliases


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

