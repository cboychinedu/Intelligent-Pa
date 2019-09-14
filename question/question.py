#!/usr/bin/env python3

# Importing the necessary Packages.
import numpy as np
import pandas as pd
import matplotlib as plt
import random
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer as Stemmer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB




# Cleaning the text by creating a function for it.
def process(text):
    # Trun the text into lowercase
    text = text.lower()
    # remove the punctuation
    text = ''.join([t for t in text if t not in string.punctuation])
    # remove stopwords
    text = [t for t in text.split() if t not in stopwords.words('english')]
    # Stemming the words
    stemmer = Stemmer()
    text = [stemmer.stem(t) for t in text]
    # Return the token list
    return text

#
tfidfv = TfidfVectorizer(analyzer=process)

# Building the model.
model = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())
])

# Reading in the dataset into memory
#filename = 'finalized_model.sav'
#[df, model] = joblib.load(filename)


def question(message):
    result = model.predict([message])[0]
    if result == 'wiki_question':
        val = random.choice(d['wiki_question'])
        print(val)
        print('passing the sentence into a stemmer, and noun filter to find a single word.')

    if result == 'bio_question':
        print('')
        val = random.choice(d['age'])
        print(val)

