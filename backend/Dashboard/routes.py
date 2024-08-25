#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import datetime 
from flask import request, jsonify
from flask import Blueprint

# Creating the blueprint object 
dashboard = Blueprint('dashboard', 
                        __name__, 
                        template_folder='templates', 
                        static_folder='static'); 

# Creating a route for the Dashboard page 
@dashboard.route('/', methods=['POST'])
def Chat(): 
    # Getting the chat message 
    requestData = request.get_json()
    chatData = requestData["chatData"]

    print(chatData)

    # Process the message or generate a response (this is just an example)
    response_message = f"Received your message: '{chatData}'"
    
    # Return the response as JSON
    return jsonify({"message": response_message})