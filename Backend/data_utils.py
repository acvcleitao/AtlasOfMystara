import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import jsonschema

def build_new_map_data(title, image, new_map_schema):
    """
    Build new map data, validate it against the schema, and return the data.

    Parameters:
    - title: The title of the map.
    - image: The image file.
    - new_map_schema: The JSON schema for new map data.

    Returns:
    - dict: The validated and formatted map data.
    """
    # Validate the input
    if not title or not image:
        raise ValueError('Title and image are required')

    # Save the image to the 'NewMaps' folder within the backend's directory
    unique_identifier = str(uuid.uuid4())
    filename = secure_filename(f"{unique_identifier}_{image.filename}")
    filepath = os.path.join(NewMapsFolder, filename)
    image.save(filepath)

    # Build map data
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    map_data = {
        'title': title,
        'image_path': filepath,
        'timestamp': timestamp,
    }

    # Validate map data against the schema
    jsonschema.validate(map_data, new_map_schema)

    return map_data
