import os
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
import bcrypt
from mongoengine import Document, StringField, connect

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
    # Define your fields here
    field1 = StringField(required=True)
    field2 = StringField(required=True)

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

    # Create a new CollectionItem document
    new_item = CollectionItem(
        field1=input("Enter field1: "),
        field2=input("Enter field2: "),
        # Add more fields as needed
    )
    new_item.save()

def main():
    command = input("Enter command: ")

    commands = {
        "create user": create_user,
        "create collection": create_collection,
        # Add more commands as needed
    }

    if command in commands:
        commands[command]()
        print(f"{command.capitalize()} executed successfully.")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
