#!/usr/bin/env python3

# importing the necessary modules
import nltk
import tflearn
import random
import json
import string
import pickle
import joblib
import numpy as np
import tensorflow as tf
import wikipedia as wiki
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk import PorterStemmer as Stemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from flask import current_app
from spellchecker import SpellChecker


# Creating a Dictionary for  the individual responses
response = {}
response['age'] = ["I am 18 years old!", "Well, Aipa is just only 18 years old", "Well, Aipa is just 18 years old.", "well, since you asked, i am 18 years old, and My name is Aipa."]
response['greeting'] = ['Hi ', 'Hello, how are you', 'Hello, How are you doing?']
response['task'] = ["""Good., So i can  perform credit scoring, web analysis and Data analysis.\nBut just tell me what you need and i'll give you the accurate results.."""]
response['bio_question'] = ['fine fine, Its Really nice of you to ask tho..', "Fine okay,  What about you?", 'i Am Doing Good, Thanks for asking...']
response['name'] = ['My name is Aipa, and i am a Personal Assistant for analytics intelligence', 'My Name is Aipa, and i can help you out with Credit scoring, Web analytics and Data Analytics']
response['good_reply'] = ['Ok Perfect...', 'Perfect...', 'Ok, Thats Good tho..', 'Alright...']

# Creating a Dictionary for the responses given back to the user if the question asked is going to be passed into wikipedia
d = {}
d['wiki_question'] = ['Your answers would be extracted from wikipedia, are you okay with this?']
d['age'] = ['My name is Aipa, and i am a Personal Assistant at Analytics Intelligence, and i am also 18 years old.', 'My is Aipa, I am a Personal Assistant for Analytics Intelligence, and i am 18years young.']
stop_words = set(stopwords.words('english'))

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

# Assigning a variable called spell to check and correct the spelling of the input word
# or sentences passed into the system.
spell = SpellChecker()
value = 'doc'

# Loading in the  json dataset for classification between a Question and a Conversation.
with open("Dashboard/model/model_1.json") as file:
    data = json.load(file)


# Defining a function to Extract a Noun From the Sentence passed into it.
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


# Building the model using Naive Bayes from sklearn Module.
model_2 = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())
])

# Wiki pedia question
def wikipediaQustion(message):
    _correct = []
    val = random.choice(d["wiki_question"])
    #
    for i in message.split():
        if i not in stop_words:
            corrected_word = spell.correction(i)
            _correct.append(corrected_word)

    #
    try:
        new_val = " ".join(_correct)
        corrected_message = extract_noun(new_val)
        wikipedia_message = wiki.summary(corrected_message, sentences=2)
        # print("Bot: ", wikipedia_message)
        # lang = "en"
        # speech = Speech(wikipedia_message, lang)
        # speech.play()
        return wikipedia_message


    except:
        return "Unable to get your question on wikipedia"


# Initializing the stemming function to stem the words passed into the system.
stemmer = LancasterStemmer()

# Setting a try and exception method to load the pickle file into memory or
# Create a new one if it is present.
try:
    with open("Dashbaord/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    # Converting the values in the json dataset into words then tokenize them and append them into
    # the created lists above.
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        # Setting an if statement to check if the words present in labels are there, and if present
        # skip , but if not present append them to the list labels.
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    # Convert the words into lower case letters, them stem them and save them into a variable called words.
    # Then sort the word in the set and save the values into a variable called words.
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    # Assigning the variable labels to hold the sorted words in the list labels.
    labels = sorted(labels)

    # Creating an empty list to hold both the training and output list.
    training = []
    output = []

    # Assigning the length of words in the labels variables into a new variable called out_empty..
    out_empty = [0 for _ in range(len(labels))]

    # Creating a for loop to loop through the values in docs_x and enumerate them and create a new empty list called bag
    # that would hold the numerical values for the words.
    # Then Stemming the words in docs_x and turning them into lower case letters before appending the index value
    # to the bag of words list
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

        # then append the values or numerical values in the bag of words list into a training list that would be use to
        # train the machine learning classifier
        training.append(bag)
        output.append(output_row)

    # Converting the values or numbers  of both the training and output list
    # into a numpy matrix and saving it into a list called training
    training = np.array(training)
    output = np.array(output)

    # Saving the Cleaned dataset into a pickle file
    with open("Dashboard/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# Building the model by adding 8 neurons for 3 layers and Resetting the Tensorflow graph.
tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# Loading the model into memory and saving it as model for predictions.
try:
    model.load("Dashboard/model/model.tflearn")
except:
    model.fit(training, output, n_epoch=10000, batch_size=8, show_metric=True)
    model.save("Dashboard/model/model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    # converting the sentences into words and saving them into a variable called s_words
    # Then stemming the words to get a single and simplified word.
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    # Creating a loop to loop through the words and enumerate them, then
    # append 1 to the bag of words list if the word is present and 0 if not present.
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    # The return the list as a numpy array of matrix
    return np.array(bag)


#
def ChatMessage(inputMessage):
    global response

    dict_pickle = []

    # Running the First Model against the input text from the user to determine if the text is a Conversational
    # message or a Question asked by the user.
    results = model.predict([bag_of_words(inputMessage, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]

    # Saving the user input and the corresponding tag predicted by the first model .
    dict_pickle.append([tag, inputMessage])

    # if the tag is a question
    if tag == "question":
        # Getting the actual predicted tag from the # QUESTION: model
        questionModel = current_app.config["questionModel"]
        quest = questionModel.predict([inputMessage])[0]

        # If the question is a wiki pediat question
        if quest == 'wiki_question':
            responseData = wikipediaQustion(inputMessage)

            return responseData

        elif quest == "bank_details":
            responseData = """ These are your recent transactions\n
                    Txn: Credit
                    Acct: 2XX..76X Amt:NGN 6,000.00
                    Desc:MOB/UTU/3704572469/
                    Date: 10-Sep-2019 18: 45
                    Bal:NGN 195,733,000""";
            return responseData

        elif quest == "location":
            responseData = "you are located in this particular location"
            return responseData

    # 
    elif tag == 'conversation':
        # Getting the actual predicted conversation
        conversationModel = current_app.config["conversationModel"]
        convo = conversationModel.predict([inputMessage])[0]
        print(convo)

        # if the conversation is a conversation, execute the block
        # of code below
        if convo == "greeting":
            responseData = random.choice(response['greeting'])
            return responseData

        elif convo == 'bio_question':
            responseData = random.choice(response['bio_question'])
            return responseData

        elif convo == 'task':
            responseData = random.choice(response['task'])
            return responseData

        elif convo == 'age':
            responseData = random.choice(response['age'])
            return responseData

        elif convo == 'name':
            responseData = random.choice(response['name'])
            return responseData

        elif convo == 'good_reply':
            responseData = random.choice(response['good_reply'])
            return responseData
