#!/usr/bin/env python3 

# Importing the necessary modules 
import json 
from pymongo import MongoClient 
from flask import jsonify

# Getting the URI for the mongodb database 
# client = MongoClient('mongodb://localhost:27017/')
# db = client['car_tyre_analysis']
# collection = db['users']

# Creating a class for handling the database connections 
class MongoDB: 
    def __init__(self): 
        self.client = None 
        self.db = None 

    # Creating a method for connecting into the database 
    def connect(self, uri, db_name): 
        self.client = MongoClient(uri) 
        self.db = self.client[db_name]

    # Creating a method for retrieving only important user's info 
    def user_infomation(self, collection_name, email): 
        # Setting the query 
        query = { 'email': email }
        collection = self.db[collection_name]

        # Find one data by the specified email address 
        data = collection.find_one(query, {
            "_id": 1, 
            "firstname": 1, 
            "lastname": 1, 
            "email": 1
        }); 

        # if the returned type is a None type, execute the block 
        # of code below 
        if data == None: 
            # return None as a data type 
            return None; 

        # Convert the MongoDB documents into a json object 
        json_data = json.dumps(dict(data), default=str)
        json_data = jsonify(json_data); 

        # Return the json object 
        return json_data; 

    # Creating a method for retriving the data from the mongodb database 
    def retrieve_data(self, collection_name, email): 
        # Setting the query 
        query = { 'email': email }
        collection = self.db[collection_name]

        # Find one data by the specified email address 
        data = collection.find_one(query); 

        # if the returned type is a None type, execute the block 
        # of code below 
        if data == None: 
            # return None as a data type 
            return None; 

        # Convert the MongoDB documents into a json object 
        json_data = json.dumps(dict(data), default=str)
        json_data = jsonify(json_data); 

        # Return the json object 
        return json_data;  

    # Creating a method for saving the data into the mongodb database 
    # Server 
    def save_data(self, collection_name, data): 
        collection = self.db[collection_name]
        result = collection.insert_one(data) 

        # Returning the result 
        return result.acknowledged