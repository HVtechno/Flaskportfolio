import json
from nltk.chat.util import Chat, reflections
from fuzzywuzzy import fuzz
import re

def load_intents(file_path):
    with open(file_path, 'r') as file:
        intents_data = json.load(file)
    return intents_data["intents"]

def find_matching_pattern(user_input, patterns):
    best_pattern = None
    for pattern in patterns:
        if isinstance(pattern, str):
            if user_input.lower() == pattern.lower():
                best_pattern = pattern
                break
            normalized_pattern = re.sub(r'[^\w\s]', '', pattern).lower()
            normalized_input = re.sub(r'[^\w\s]', '', user_input).lower()
            if normalized_pattern in normalized_input:
                best_pattern = pattern
                break
        elif isinstance(pattern, re.Pattern):
            match = pattern.search(user_input)
            if match:
                best_pattern = pattern.pattern
                break
    return best_pattern

def create_chatbot(intents):
    pairs = []
    for intent in intents:
        patterns = intent["patterns"]
        responses = intent["responses"]
        for pattern in patterns:
            if isinstance(pattern, str):
                pairs.append((pattern, responses))
            else:
                pairs.append((str(pattern), responses))
    return Chat(pairs, reflections)

def chat_response(user_input, chatbot):
    best_pattern = find_matching_pattern(user_input, [pair[0] for pair in chatbot._pairs])
    if best_pattern:
        response = chatbot.respond(best_pattern)
        return response if response else "I apologize, my capabilities are limited to patterns I've been trained on. Could you please rephrase your sentence for me"
    else:
        return "I apologize, my capabilities are limited to patterns I've been trained on. Could you please rephrase your sentence for me"


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