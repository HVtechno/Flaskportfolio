import json
from nltk.chat.util import Chat, reflections

def load_intents(file_path):
    with open(file_path, 'r') as file:
        intents_data = json.load(file)
    return intents_data["intents"]

def create_chatbot(intents):
    pairs = []
    for intent in intents:
        patterns = intent["patterns"]
        responses = intent["responses"]
        pairs.append([f"({'|'.join(patterns).lower()})", responses])
    return Chat(pairs, reflections)

def chat_response(user_input, chatbot):
    response = chatbot.respond(user_input)
    return response if response else "I'm sorry, I didn't understand that. Can you please rephrase?"

if __name__ == "__main__":
    intents_file_path = "static/intents/intents.json"
    intents = load_intents(intents_file_path)
    chatbot = create_chatbot(intents)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = chat_response(user_input, chatbot)
        print("ChatGPT:", response)