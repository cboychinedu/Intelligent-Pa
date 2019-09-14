#!/usr/bin/env python

# Importing the necessary packages.
import nltk
import tflearn
import tensorflow as tf
import random
import json
import pickle
from gtts import gTTS
from nltk.stem.lancaster import LancasterStemmer
from subprocess import call
from time import sleep
import numpy as np
import random
import wikipedia as wiki
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer as Stemmer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from spellchecker import SpellChecker


# Creating a Dictionary for responses
response = {}
response['age'] = ["I am 18 years old!", "AIPA is just only 18 years old", "APIA is 18 years old.", "well, since you asked, i am 18 years old"]
response['greeting'] = ['Hello, how can Aipa help you today?', 'Hello, how can Analytics Intelligence Assistant Help you today?', 'Hello, How are you doing?']
response['task'] = ["""Good., Do you know that I can perform credit scoring, web analysis and Data analysis.\nBut just tell me what you need and i'll give you the accurate results.."""]
response['bio_question'] = ['fine fine, yours?', "Fine okay, yours?", 'Nahhh, we all good, and bless God for that....']
response['name'] = ['My name is Aipa, and i am a Personal Assistant for analytics intelligence. I can perform credit scoring, web analysis and Data Analytics.']
response['good_reply'] = ['Yeah sure, Anytime ok', 'Perfect...', 'Ok Great...']

correct = []
d = {}
d['wiki_question'] = ['Your answers would be extracted from wikipedia, are you okay with this?']
d['age'] = ['My name is Aipa, and i am a Personal Assistant at Analytics Intelligence, and i am also 18 years old.', 'My is Aipa, I am a Personal Assistant for Analytics Intelligence, and i am 18years young.']
stop_words = stopwords.words('english')
spell = SpellChecker()

# Loading in the dataset
with open("model/model_1.json") as file:
    data = json.load(file)

##
# Cleaning the text by creating a function for it.
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



# Defining a function to Extract a Noun.
def extract_noun(sentence):
    grammar = r"""
    NBAR:
        # Nouns and Adjectives, terminated with Nouns
        {<NN.*>*<NN.*>}

    NP:
        {<NBAR>}
        # Above, connected with in/of/etc...
        {<NBAR><IN><NBAR>}

    """
    chunker = nltk.RegexpParser(grammar)
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sentence)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne



#
tfidfv = TfidfVectorizer(analyzer=process)

# Building the model.
model_2 = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())
])


# creating a function to take in questions and pass it into the wikipedia application programming
# Interface.
def question(message):
    result = model_2.predict([message])[0]
    if result == 'wiki_question':
        val = random.choice(d['wiki_question'])
        print(val)
        msg = input('You: ')
        if msg.lower().replace(' ', '') == 'yes':
            #print('Ok great, so you want the Description or Definition of {}'.format(id))
            # import the question script and pass the input question into the function.
            for i in message.split():
                if (i not in stop_words):
                    correct.append(i)

        # N/B TRY AND EXCEPT METHOD WOULD BE IMPLEMENTED HERE LATER FOR ANSWERING
        # QUESTIONS FROM THE DEFAULT DATASET FIRSTLY, BEFORE EXCEPTION WHICH WOULD BE
        # IT SENDS THE MESSAGE INTO WIKIPEDIA FOR THE OTHER RESULT.

            try:
                new_val = " ".join(correct)
                corrected_message = extract_noun(new_val)
                wikipedia_message = wiki.summary(corrected_message, sentences=5)
                print(wikipedia_message)

            except:
                print('Please Rephrase, Currently unable to get your result...')

        else:
            print('Please Rephrase your question, Currently unable to retrive your Answers...')
            pass

    if result == 'bio_question':
        print('')
        val = random.choice(d['age'])
        print(val)



# Reading in the dataset into memory
filename = 'question/finalized_model.sav'
[df, model_2] = joblib.load(filename)


#
stemmer = LancasterStemmer()
# Defining a speech function to speak out
# the predicted text.
def speech(result):
    tts = gTTS(result)
    tts.save('voice.mp3')
    call('mpg321 voice.mp3 2>/dev/null', shell=True)
    call('rm voice.mp3', shell=True)


try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tf.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model/model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model/model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)



def chat():
    dict_pickle = []
    while True:
        inp = input("You: ")
        if inp.lower().replace(' ', '') == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]
        #
        dict_pickle.append([tag, inp])

        if tag == 'question':
            print('wikipedia or other Questions...')
            question(inp)
            sleep(2)


        elif tag == 'conversation':
           
            from conversation.conversation_script import conversation
            convo = conversation(inp)

            if convo == 'greeting':
                reply = random.choice(response['greeting'])
                print(reply)
            elif convo == 'bio_question':
                reply = random.choice(response['bio_question'])
                print(reply)
            elif convo == 'task':
                reply = random.choice(response['task'])
                print(reply)
            elif convo == 'age':
                reply = random.choice(response['age'])
                print(reply)
            elif convo == 'name':
                reply = random.choice(response['name'])
                print(reply)
            elif convo == 'good_reply':
                reply = random.choice(response['good_reply'])
                print(reply)


        for i in dict_pickle:
            with open('inputdata.csv', 'a+') as f:
                f.write('{}\n'.format(i))


def interaction(value, interactive_message):
    if value == 'question':
        message = interactive_message.lower()
        # Run it along a new model that classifies on inputs and responses.
        ## or start an interactive breakdown on how the question is passed.
    elif value == 'conversation':
        pass
        # Start an interactive conversation on how the first question was asked.


chat()
