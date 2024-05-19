import json
import nltk
import random
import pickle
import numpy as np 
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer

# Initializing Lancaster Stemmer
stemmer = LancasterStemmer()

# Loading dataset
with open('dataset/dataset.json') as f:
    data = json.load(f)

try:
    with open('data.pickle', 'rb') as file:
        words, labels, train,  output = pickle.load(file)
except FileNotFoundError:
    words = []
    x_docs = []  # Patterns - Sentences
    y_docs = []  # Tags for patterns
    labels = []

    # Looping over all data in json file as dictionaries
    for intent in data['intents']:
        # Looping over the patterns - input sentences
        for pattern in intent['patterns']:
            # Tokenizing each word in each pattern sentences
            tokenizedWords = nltk.word_tokenize(pattern)
            # Extending words list with lists of tokens
            words.extend(tokenizedWords)
            # Appending docs lists with sentence and respective tag
            x_docs.append(tokenizedWords)
            y_docs.append(intent['tag'])
            # Appending labels list with tags
            if intent['tag'] not in labels:
                labels.append(intent['tag'])

    # Sorting labels
    labels = sorted(labels)

    # Stemming words and sorting - Stemming refers to finding the root of every word
    words = [stemmer.stem(w.lower()) for w in words if w not in '?']
    words = sorted(list(set(words)))

    train = []
    output = []

    # Creating a Bag of Words - One Hot Encoding
    out_empty = [0 for _ in range(len(labels))]
    for x, doc in enumerate(x_docs):
        bag = []
        stemmedWords = [stemmer.stem(w) for w in doc]

        # Marking word index as 1
        for w in words:
            if w in stemmedWords:
                bag.append(1)
            else:
                bag.append(0)

        outputRow = out_empty[:]
        outputRow[labels.index(y_docs[x])] = 1

        train.append(bag)
        output.append(outputRow)

    # Converting data into numpy array
    train = np.array(train)
    output = np.array(output)

    # Saving data
    with open('data.pickle', 'wb') as f:
        pickle.dump((words, labels, train, output), f)

# Building network
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(len(train[0]),)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(len(output[0]), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print('[INFO] Training Model...')

# Training model
model.fit(train, output, epochs=400, batch_size=8)

# Saving model weights
model.save('models/chatbot-model.keras')

print('[INFO] Model successfully trained')
