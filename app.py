import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('static/models/model.h5')
import json
import random
from flask import Flask, render_template, request, jsonify
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

intents = json.loads(open('static/intents/data.json').read())
words = pickle.load(open('static/models/texts.pkl','rb'))
classes = pickle.load(open('static/models/labels.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

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
    app.run(debug=True)