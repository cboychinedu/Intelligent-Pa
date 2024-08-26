#!/usr/bin/env python

# importing the necessary packages
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Cleaning the text
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer as Stemmer
def process(text):
    # turn the texts into lowercase
    text = text.lower()
    # remove punctuation
    text = ''.join([t for t in text if t not in string.punctuation])
    # remove stopwords
    text = [t for t in text.split() if t not in stopwords.words('english')]
    # Stemming the words
    stemmer = Stemmer()
    text = [stemmer.stem(t) for t in text]
    # Return the token list
    return text


tfidfv = TfidfVectorizer(analyzer = process)

# Building a model
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

question_model = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())

])

filename = 'conversation/finalized_model.sav'
# load the model from disk
question_model = joblib.load(filename)


# Defining a function to run and use the model for classfication.
def conversation(s):
    result = question_model.predict([s])[0]
    return result

