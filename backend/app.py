#!/usr/bin/env python3 

# Importing the necessary modules 
import bcrypt
from flask import Flask, url_for, session 
from flask_cors import CORS
from datetime import timedelta

# Creating the flask application 
app = Flask(__name__, static_folder=None, template_folder=None)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "kdsd8*DEKFE!@$#$$REDKDNI*(KEHE&E&^^$D"
app.permanent_session_lifetime = timedelta(days=24)

# Setting the cors application 
CORS(app) 

# Importing the views 
from Home.routes import home 
from Dashboard.routes import dashboard

# Register the views using the "app.register" function 
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(dashboard, url_prefix="/dashboard")

# Running the flask application 
if __name__ == "__main__": 
    app.run(port=3001, host="localhost", debug=True)
    app.run() 
