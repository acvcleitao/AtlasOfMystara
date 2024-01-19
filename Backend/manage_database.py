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

class User(Document):
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

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt

def create_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password, salt = hash_password(password)

    # Create a new user document
    new_user = User(username=username, password=hashed_password, salt=salt)
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



def main():
    command = input("Enter command: ")

    commands = {
        "create user": create_user,
        "create collection": create_collection,
        "create new map": create_new_map,
        # Add more commands as needed
    }

    if command in commands:
        commands[command]()
        print(f"{command.capitalize()} executed successfully.")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
