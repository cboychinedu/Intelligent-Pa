#!/usr/bin/env python3

# Importing the necessary Packages.
import string
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import PorterStemmer as Stemmer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
#from sklearn.externals import joblib

#
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

# Passing the stemmed words into a vectorizer to convert the words into
# vectors and hold numbers of the word count of each individual words.
tfidfv = TfidfVectorizer(analyzer = process)

# Building The model using Naive Bayes Classifier
question_model = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())

])

# Loading the saved model from disk.
filename = 'question/finalized_model.sav'
# load the model from disk
question_model = joblib.load(filename)


# Defining a function to run and use the model for classfication and return the
# Values back to the user.
def question_classifier(s):
    result = question_model.predict([s])[0]
    return result

