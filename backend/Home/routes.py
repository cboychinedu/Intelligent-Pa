#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
from flask import request, jsonify
from flask import Blueprint, session 

# Creating the blueprint object 
home = Blueprint('home', __name__, template_folder='templates', static_folder='static');

# Creating the home page 
@home.route('/', methods=["POST"])
def Register(): 
    # Get the firstname, email and password data
    requestData = request.get_json()
    firstname = requestData["firstname"]
    email = requestData["emailAddress"]
    password = requestData["password"]

    #  


    # Register the user 
    return jsonify({ 
        "token": "dddd"
    })