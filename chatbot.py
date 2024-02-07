import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import tensorflow as tf

# Initialize WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Read data from JSON file
data_file = open('static/intents/data.json').read()
intents = json.loads(data_file)

# Initialize lists
words = []
classes = []
documents = []
ignore_words = ['?', '!']

# Iterate through intents and patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Add documents to the corpus
        documents.append((w, intent['tag']))
        # Add intent tag to classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize, lowercase, and remove duplicates from words
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
# Sort classes
classes = sorted(list(set(classes)))

# Save words and classes to pickle files
pickle.dump(words, open('static/models/texts.pkl', 'wb'))
pickle.dump(classes, open('static/models/labels.pkl', 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)

# Iterate through documents
for doc in documents:
    bag = []
    pattern_words = doc[0]
    # Lemmatize each word
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # Create bag of words
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    # Create output row
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    # Append bag and output row to training data
    training.append([bag, output_row])

# Shuffle training data
random.shuffle(training)

# Separate bags of words and output rows
bags_of_words = [item[0] for item in training]
output_rows = [item[1] for item in training]

# Convert bags of words and output rows into numpy arrays
bags_of_words_np = np.array(bags_of_words)
output_rows_np = np.array(output_rows)

# Create model
model = Sequential()
model.add(Dense(128, input_shape=(len(bags_of_words_np[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(output_rows_np[0]), activation='softmax'))

# Compile model
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Fit model
hist = model.fit(bags_of_words_np, output_rows_np, epochs=200, batch_size=5, verbose=1)

# Save model
model.save('static/models/model.h5', hist)

print("Model created")