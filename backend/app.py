#!/usr/bin/env python3 

# Importing the necessary modules 
from flask import Flask
from flask_cors import CORS
from datetime import timedelta
import joblib
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from nltk import PorterStemmer as Stemmer

# Creating the flask application 
app = Flask(__name__, static_folder=None, template_folder=None)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "kdsd8*DEKFE!@$#$$REDKDNI*(KEHE&E&^^$D"
app.permanent_session_lifetime = timedelta(days=24)

# Setting the cors application 
CORS(app) 

# Load the machine learing model 
def process(text):
    # turn the texts into lowercase
    text = text.lower()
    # remove punctuation
    text = ''.join([t for t in text if t not in string.punctuation])
    # remove stopwords
    # text = [t for t in text.split() if t not in stopwords.words('english')]
    # Stemming the words
    stemmer = Stemmer()
    text = [stemmer.stem(t) for t in text]
    # Return the token list
    return text


# Building The model using Naive Bayes Classifier and vectorizer to
# Convert the words into vectors with number of word count.
conversationModel = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())

])

# Question model 
questionModel = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())

])

# Loading the model 
filename = "conversationModel"
conversationModel = joblib.load(filename)

# loading the model 
filename = "questionModel"
questionModel = joblib.load(filename)

# Storing the model 
app.config['conversationModel'] = conversationModel
app.config['questionModel'] = questionModel

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

# app.run(port=3001, host="localhost", debug=True)
