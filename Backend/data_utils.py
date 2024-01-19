import base64
import os
import uuid
from flask import jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import jsonschema
from schemas import new_map_schema;

def build_new_map_data(title, image_data, NewMapsFolder):
    """
    Build new map data, validate it against the schema, and return the data.

    Parameters:
    - title: The title of the map.
    - image: The image file.
    - NewMapsFolder: The folder used to store new maps.

    Returns:
    - dict: The validated and formatted map data.
    """
    # Validate the input
    if not title or not image_data:
        return jsonify({'message': 'Title and image are required'}), 400

    # Decode base64 string and save the image to the server
    unique_identifier = str(uuid.uuid4())
    filename = secure_filename(f"{title}_{unique_identifier}.png")
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

    # Validate map data against the schema
    jsonschema.validate(map_data, new_map_schema)

    return map_data
