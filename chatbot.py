import json
import nltk
import random
import pickle
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Load the intents data
with open('static/intents/data.json') as file:
    data = json.load(file)

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Initialize empty lists for documents and classes
documents = []
classes = []
text = []
intents = []

# Preprocess the data
for intent in data['intents']:
    for pattern in intent['patterns']:
        words = word_tokenize(pattern)
        words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalnum()]
        text.append(" ".join(words))
        intents.append(intent['tag'])
    if intent['tag'] not in classes:
        classes.append(intent['tag'])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(text)

y = [classes.index(intent) for intent in intents]

classifier = LinearSVC()
classifier.fit(X, y)

pickle.dump(vectorizer, open('static/models/vectorizer.pkl', 'wb'))
pickle.dump(classifier, open('static/models/classifier.pkl', 'wb'))

print("Model training completed.")