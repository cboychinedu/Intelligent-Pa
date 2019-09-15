#!/usr/bin/env python

# Description:
# Author:
# Company:
# Date Created:
#

# Importing the necessary packages.
import nltk
import tflearn
import random
import json
import string
import pickle
import numpy as np
import tensorflow as tf
import wikipedia as wiki
from time import sleep
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk import PorterStemmer as Stemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from spellchecker import SpellChecker


# Creating a Dictionary for  the individual responses
response = {}
response['age'] = ["I am 18 years old!", "Well, Aipa is just only 18 years old", "Well, Aipa is just 18 years old.", "well, since you asked, i am 18 years old, and My name is Aipa."]
response['greeting'] = ['Hey there', 'Hello, how are you', 'Hello, How are you doing?']
response['task'] = ["""Good., So i guess you know that I can perform credit scoring, web analysis and Data analysis.\nBut just tell me what you need and i'll give you the accurate results.."""]
response['bio_question'] = ['fine fine, Its Really nice of you to ask tho..', "Fine okay,  What about you?", 'i Am Doing Good, Thanks for asking...']
response['name'] = ['My name is Aipa, and i am a Personal Assistant for analytics intelligence', 'My Name is Aipa, and i can help you out with Credit scoring, Web analytics and Data Analytics']
response['good_reply'] = ['Ok Perfect...', 'Perfect...', 'Ok Nice..', 'Alright...']

# Creating a Dictionary for the responses given back to the user if the question asked is going to be passed into wikipedia
d = {}
d['wiki_question'] = ['Your answers would be extracted from wikipedia, are you okay with this?']
d['age'] = ['My name is Aipa, and i am a Personal Assistant at Analytics Intelligence, and i am also 18 years old.', 'My is Aipa, I am a Personal Assistant for Analytics Intelligence, and i am 18years young.']
stop_words = stopwords.words('english')

# Assigning a variable called spell to check and correct the spelling of the input word
# or sentences passed into the system.
spell = SpellChecker()

# Loading in the  json dataset for classification between a Question and a Conversation.
with open("model/model_1.json") as file:
    data = json.load(file)


# Cleaning the text by creating a function to stem the words and convert the
# Alphabets into lower case letters so that the model prediction would be effective.
def process(text):
    # Turn the text into lowercase
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


# Passing the process function into the Vectorizer that would take in the filtered
# words from the input sentences and produce a word count for the individual words in
# the function and then save them into a variable called tfidfv variable.
tfidfv = TfidfVectorizer(analyzer=process)

# Building the model using Naive Bayes from sklearn Module.
model_2 = Pipeline([
    ('vectorizer', TfidfVectorizer(analyzer=process)),
    ('classifier', MultinomialNB())
])


# creating a function to take in questions and pass it into the wikipedia application programming
# Interface for the Required results and then return it back to the user.
def wikipedia_question(message):
    _correct = []
    result = 'wiki_question'
    if result == 'wiki_question':
        val = random.choice(d['wiki_question'])
        print(val)
        msg = input('You: ')
        if msg.lower().replace(' ', '') == 'yes':
            # import the question script and pass the input question into the function.
            for i in message.split():
                if i not in stop_words:
                    corrected_word = spell.correction(i)
                    _correct.append(corrected_word)

        # N/B TRY AND EXCEPT METHOD WOULD BE IMPLEMENTED HERE LATER FOR ANSWERING
        # QUESTIONS FROM THE DEFAULT DATASET FIRSTLY, BEFORE EXCEPTION WHICH WOULD BE
        # IT SENDS THE MESSAGE INTO WIKIPEDIA FOR THE OTHER RESULT.

            try:
                # Passing in the corrected word and joining them into a single sentence,
                # Then extract the nouns and pronouns present in the function and them pass them into
                # Wikipedia api for the required results.
                new_val = " ".join(_correct)
                corrected_message = extract_noun(new_val)
                wikipedia_message = wiki.summary(corrected_message, sentences=5)
                print(wikipedia_message)

            except:
                print('Please Rephrase, Currently unable to get your result...')

        else:
            print('Please Rephrase your question, Currently unable to Get your Answers...')
            pass


# Initializing the stemming function to stem the words passed into the system.
stemmer = LancasterStemmer()

# Setting a try and exception method to load the pickle file into memory or
# Create a new one if it is present.
try:
    with open("data.pickle", "rb") as f:
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
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# Building the model by adding 8 neurons for 3 layers and Resetting the Tensorflow graph.
tf.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# Loading the model into memory and saving it as model for predictions.
try:
    model.load("model/model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model/model.tflearn")


# Creating a function for taking in words and stemming them into simpler words, then
# saving its representative index number into a variable called bag.
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


# Creating a function to Start the program and run the models on the input messages.
def chat():
    dict_pickle = []
    while True:
        inp = input("You: ")
        if inp.lower().replace(' ', '') == "quit":
            break

        # Running the First Model against the input text from the user to determine if the text is a Conversational
        # message or a Question asked by the user.
        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        # Saving the user input and the corresponding tag predicted by the first model .
        dict_pickle.append([tag, inp])

        # Setting an if statement to check if the predicted tag was a question and if it was
        # it should pass the input question into the question_classifier script to find out the type of question it is.
        # After prediction on the actual question, then a function for that particular predicted question is called.
        if tag == 'question':
            # Getting The Actual Predicted tag from the Question model and saving it into the variable called quest
            from question.question import question_classifier
            quest = question_classifier(inp)
            print(quest)

            # if the predicted Question is a Wikipedia based question, then pass the question into wikipedia api to
            # Get the answers for the question.
            if quest == 'wiki_question':
                wikipedia_question(inp)

        # Setting an else if statement to check if the predicted tag was a Conversation, and if it was, it
        # Should pass the input Question into the conversation classifier to actually find out what type of conversation
        # it is and perform actions based on it .
        elif tag == 'conversation':
            # Getting the Actual Predicted Tag from the Conversation model and saving it into the variable called convo
            from conversation.conversation_script import conversation_classifier
            convo = conversation_classifier(inp)

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

        # Saving the user input and predicted tags into a new csv dataset file called 'inputdata.csv'
        # for furthermore training.
        for i in dict_pickle:
            with open('inputdata.csv', 'a+') as f:
                f.write('{}\n'.format(i))

# Defining a function for the interactive mode in the System.
def interaction(value, interactive_message):
    if value == 'question':
        message = interactive_message.lower()
        # Run it along a new model that classifies on inputs and responses.
        # or start an interactive breakdown on how the question is passed.
    elif value == 'conversation':
        pass
        # Start an interactive conversation on how the first question was asked.


chat()