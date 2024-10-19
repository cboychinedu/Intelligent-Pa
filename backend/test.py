#!/usr/bin/env python

# importing the necessary packages
#from sklearn.externals import joblib
import joblib
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from nltk import PorterStemmer as Stemmer


 
# # Loading the saved model from disk into memory...
filename = 'conversationModel'
model = joblib.load(filename)

# Defining a function to run and use the model for classfication
# Then return the index of the predicted values back .
def conversation_classifier(s):
    print(s); 
    result = model.predict([s])[0]
    return result


res = conversation_classifier("Hello, how are you")
print(res); 

