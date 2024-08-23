#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import jwt
import bcrypt
import datetime
from mongo import MongoDB
from flask import request, jsonify
from flask import Blueprint, session 

# Creating the blueprint object 
home = Blueprint('home', __name__, template_folder='templates', static_folder='static');

# Getting the secret key 
jwtSecretKey = os.getenv("JWT_KEY")

# Creating an instance of the database 
db = MongoDB(); 

# Creating a route for the login user
@home.route("/login", methods=["POST"])
def Login(): 
    # Get the email and password data 
    requestData = request.get_json() 
    email = requestData["emailAddress"]
    password = requestData["password"]

    # Getting the user's data by connecting to the mongodb database server 
    db.connect('mongodb://localhost:27017/', 'intelligent_pa') 
    databaseData = db.retrieve_data('users', email=email)

    # If the user is found on the database with the specified email address, execute 
    # the block of code below 
    if databaseData: 
        # Validate the user's password to see if it is correct 
        passwordCondition = bcrypt.checkpw(password.encode('utf-8'), databaseData['password'].encode('utf-8'))

        # Checking if the password condition returned a True, or False value 
        if (passwordCondition == True): 
            # Create a user token and send it back to the client 
            payload = {
                "userId": str(databaseData["_id"]), 
                "emailAddress": email,
                "fullname": str(databaseData["fullname"]),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }

            # Creating the jwt token 
            token = jwt.encode(payload, jwtSecretKey, algorithm='HS256')

            # Return the token 
            return jsonify({
                "status": "success", 
                "message": "User logged in", 
                "x-auth-token": token, 
                "statusCode": 200
            })
        
        # Else if the password was not correct 
        else: 
            # 
            return jsonify({
                "status": "error", 
                "message": "Invalid email or password", 
                "statusCode": 404
            })
        
    # Else if the user' is not found on the database 
    else:
        # 
        return jsonify({
            "status": "error", 
            "message": "Invalid email or password", 
            "statusCode": 500
        })
    


# Creating the home page 
@home.route('/register', methods=["POST"])
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

    # If the user does not exist on the database, execute the block 
    # of code below 
    if databaseData == None:
        # Hashing the password 
        hashPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
        hashPassword = hashPassword.decode('utf-8')

        # Request data 
        userData = {
            "fullname": fullname, 
            "email": email, 
            "password": hashPassword
        }

        # Save the user data 
        result = db.save_data("users", userData)

        # If the data was saved 
        if (result): 
            # Return a success message
            return jsonify({
                "status": "success", 
                "message": "User data saved on the database", 
                "statusCode": 200
            })

        else: 
            # Else if the data was not saved on the database 
            return jsonify({
                "status": "error", 
                "message": "User data not saved on the database", 
                "statusCode": 500
            })
        
    else:
        # If the user exists on the database, execute the block of code 
        # below 
        return jsonify({
            "status": "error", 
            "message": "The user already exists on the database", 
            "statusCode": 501
        })