import os
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
import bcrypt
from mongoengine import Document, StringField, connect
from datetime import datetime

load_dotenv()

app_config = {
    'MONGO_URI': os.getenv("MONGO_URI")
}

# Set the MongoDB URI for Flask app
app = Flask(__name__)
app.config['MONGO_URI'] = app_config['MONGO_URI']

mongo = PyMongo(app)
connect(db='AtlasOfMystara', host=app_config['MONGO_URI'])

class Users(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    salt = StringField(required=True)

class CollectionItem(Document):
    field1 = StringField(required=True)
    field2 = StringField(required=True)

class NewMap(Document):
    title = StringField(required=True)
    image_path = StringField(required=True)
    timestamp = StringField(required=True)
from mongoengine import Document, StringField, IntField

class Hexagon(Document):
    type = StringField(required=True)
    x_coordinate = IntField(required=True)
    y_coordinate = IntField(required=True)
    imageUrl = StringField(required=True)
    zoomLevel = IntField(required=True)
    author = StringField(required=True)


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt

def create_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password, salt = hash_password(password)

    # Create a new user document
    new_user = Users(username=username, password=hashed_password, salt=salt)
    new_user.save()

def create_collection():
    collection_name = input("Enter collection name: ")

    # Create a new empty CollectionItem document
    new_collection = CollectionItem()
    new_collection.save(collection_name)

def create_new_map():
    title = input("Enter map title: ")
    image_path = input("Enter image path: ")

    # Ask the user if they want to use the current timestamp
    use_current_timestamp = input("Do you want to use the current timestamp? (y/n): ").lower() == 'y'

    # Set the timestamp accordingly
    timestamp = str(datetime.now()) if use_current_timestamp else input("Enter timestamp: ")

    # Create a new NewMap document
    new_map = NewMap(title=title, image_path=image_path, timestamp=timestamp)
    new_map.save()

def create_hexagon():
    hexagon_type = input("Enter hexagon type: ")
    x_coordinate = int(input("Enter X coordinate: "))
    y_coordinate = int(input("Enter Y coordinate: "))
    image_url = input("Enter hexagon image URL: ")
    zoom_level = input("Enter zoom level: ")
    author = input("Enter author: ")

    # Create a new Hexagon document
    new_hexagon = Hexagon(type=hexagon_type, x_coordinate=x_coordinate, y_coordinate=y_coordinate,
                          imageUrl=image_url, zoomLevel=zoom_level, author=author)
    new_hexagon.save()
    print("Hexagon added successfully.")

def add_hexagons():
    hexagon_type = "farmland"
    image_url = "Thorf/forest_1fc07fc451a247108eb2dfaa24f9d065.png"
    author = "Thorf"
    zoom_level = 2

    # Define the starting and ending coordinates
    start_x, start_y = 5, 5
    end_x, end_y = 100, 20

    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            # Create a new Hexagon document
            new_hexagon = Hexagon(type=hexagon_type, x_coordinate=x, y_coordinate=y, imageUrl=image_url, 
                                  zoomLevel=zoom_level, author=author)
            new_hexagon.save()

    print("100 hexagons added successfully.")

def main():
    command = input("Enter command: ")

    commands = {
        "create user": create_user,
        "create collection": create_collection,
        "create new map": create_new_map,
        "add hexagon": create_hexagon,
        "test hexagon": add_hexagons,
        # Add more commands as needed
    }

    if command in commands:
        commands[command]()
        print(f"{command.capitalize()} executed successfully.")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
