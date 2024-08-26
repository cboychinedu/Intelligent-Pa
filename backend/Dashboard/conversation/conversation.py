#!/usr/bin/env python

# importing the necessary packages
#from sklearn.externals import joblib
import joblib
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from nltk import PorterStemmer as Stemmer

#
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
model = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())

])
 
# # Loading the saved model from disk into memory...
filename = 'conversationModel'
model = joblib.load(filename)

# Defining a function to run and use the model for classfication
# Then return the index of the predicted values back .
def conversation_classifier(s):
    print(s); 
    # result = model.predict([s])[0]
    # return result

