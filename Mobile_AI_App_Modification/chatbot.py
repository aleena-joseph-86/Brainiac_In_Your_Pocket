import json
import nltk
import random
import pickle
import numpy as np  # Add this line to import NumPy
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer

# Initializing Lancaster Stemmer
stemmer = LancasterStemmer()

# Loading dataset
with open('dataset/dataset.json') as file:
    data = json.load(file)

with open('data.pickle', 'rb') as f:
    words, labels, train, output = pickle.load(f)

# Building network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, input_shape=(len(train[0]),), activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(len(output[0]), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Loading Model
model.load_weights('models/chatbot-model.keras')

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)

def chat(inputText):
    print('[INFO] Start talking...(type quit to exit)')
    while True:
        inp = inputText
        # Type quit to exit
        if inp.lower() == 'quit':
            break
        # Predicting input sentence tag
        predict = model.predict(np.array([bag_of_words(inp, words)]))
        predictions = np.argmax(predict)
        tag = labels[predictions]
        # Printing response
        for t in data['intents']:
            if t['tag'] == tag:
                responses = t['responses']
        outputText = random.choice(responses)
        return outputText
    
