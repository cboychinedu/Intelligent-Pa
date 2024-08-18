#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import bcrypt
from mongo import MongoDB
from flask import request, jsonify
from flask import Blueprint, session 

# Creating the blueprint object 
home = Blueprint('home', __name__, template_folder='templates', static_folder='static');

# Creating an instance of the database 
db = MongoDB(); 

# Creating the home page 
@home.route('/', methods=["POST"])
def Register(): 
    # Get the firstname, email and password data
    requestData = request.get_json()
    fullname = requestData["fullname"]
    email = requestData["emailAddress"]
    password = requestData["password"]

    # Connecting to the Mongodb database, and save the users data 
    db.connect('mongodb://localhost:27017/', 'intelligent_pa')

    # Checking to see if the datat base data is present
    databaseData = db.retrieve_data('users', email=email)

    # 
    if databaseData == None:
        # Hashing the password 
        hashPassword = bcrypt.hashpw(password.encode('utff-8'), bcrypt.gensalt(10))
        hashPassword = hashPassword.decode('utf-8')

        # Request data 
        userData = {
            "fullname": fullname, 
            "email": email, 
            "password": hashPassword
        }

        # Save the user data 
        result = db.save_data("users", userData)


    # Register the user 
    return jsonify({ 
        "token": "dddd"
    })