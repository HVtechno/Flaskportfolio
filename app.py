from flask import Flask, render_template, request, jsonify
from chatbot import chat_response, create_chatbot, load_intents
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

intents_file_path = "static/intents/intents.json"
intents = load_intents(intents_file_path)
chatbot = create_chatbot(intents)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    print('Received user input:', user_input)
    bot_response = chat_response(user_input, chatbot)
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)