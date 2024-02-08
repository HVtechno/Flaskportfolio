import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
import json
import random
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SERVER = os.getenv('SMTP_SERVER')
PORT = os.getenv('SMTP_PORT')
USER = os.getenv('SMTP_USER')
PASSWORD = os.getenv('SMTP_PASSWORD')
RECEIVER = os.getenv('SMTP_RECEIVER')

app = Flask(__name__)
CORS(app)

# Load resources
with open('static/intents/data.json') as file:
    intents = json.load(file)

with open('static/models/texts.pkl', 'rb') as file:
    words = pickle.load(file)

with open('static/models/labels.pkl', 'rb') as file:
    classes = pickle.load(file)

# Load the model
model = load_model('static/models/model.h5')

def clean_up_sentence(sentence):
    return [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(sentence)]

def bow(sentence, words):
    return np.array([1 if word in sentence else 0 for word in words])

def predict_class(sentences):
    # Clean up sentences
    cleaned_sentences = [clean_up_sentence(sentence) for sentence in sentences]
    
    # Convert sentences to bags of words
    bows = [bow(sentence, words) for sentence in cleaned_sentences]
    
    # Predict classes for all sentences
    predictions = model.predict(np.array(bows))
    
    # Process predictions for each sentence
    return [process_prediction(prediction) for prediction in predictions]

def process_prediction(prediction):
    # Filter out predictions below threshold
    indexes = np.where(prediction > 0.25)[0]
    return [(i, prediction[i]) for i in indexes]

def getResponse(ints, intents_json):
    tag = classes[ints[0][0]]
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

def chatbot_response(msg):
    ints = predict_class([msg])[0]
    return getResponse(ints, intents)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    print('Received user input:', user_input)
    bot_response = chatbot_response(user_input)
    return jsonify({'bot_response': bot_response})

@app.route('/send_message', methods=['POST'])
def send_message():
    user_data = {
        'user_name': request.form.get('full_name'),
        'user_email': request.form.get('email_address'),
        'user_mobile': request.form.get('mobile_number'),
        'email_subject': request.form.get('email_subject'),
        'user_message': request.form.get('your_message')
    }

    send_confirmation_email(user_data)

    return '', 204

def send_confirmation_email(user_data):
    subject = "🎉 Someone Looking For You! 🕵️‍♂️"
    
    html_content = render_template('thankyou.html', **user_data)

    sender_email = user_data['user_email']
    receiver_email = RECEIVER

    message = MIMEMultipart()
    message["From"] = f"HariDigiCV <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(html_content, "html"))

    smtp_server = SERVER
    smtp_port = PORT
    smtp_username = USER
    smtp_password = PASSWORD

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    options = {
        'request_timeout': 120  # Set the timeout to 120 seconds
    }
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000, **options)