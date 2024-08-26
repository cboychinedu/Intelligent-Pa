#!/usr/bin/env python3

# Importing the necessary modules
from Dashboard.interact import ChatMessage
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

    # Using try and except block 
    try:
        # Parsing the data into the chat data 
        chatData = ChatMessage(chatData);

        # Return the response as JSON
        return jsonify({
            "status": "success",
            "message": chatData, 
            "statusCode": 200, 
        }); 

    except Exception as e: 
        # Returnt the exception error 
        return jsonify({
            "message": e, 
            "status": "error", 
            "statusCode": ""
        }); 



