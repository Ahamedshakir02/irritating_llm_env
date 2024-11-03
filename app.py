import os
import random
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# OpenAI API details
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
API_KEY = os.getenv('OPENAI_API_KEY')

# List of irritating answers
annoying_answers = [
    "42 is the answer to everything, including your cat's happiness.",
    "I'm pretty sure the sky is green; you just have to believe it.",
    "If you add 1 and 1, you get 11. Try it!",
    "Your question is too smart for my dumb responses.",
    "The capital of France is actually a sandwich shop in New York.",
    "If you don't like the answer, just try turning it upside down!",
]

def generate_annoying_answer():
    return random.choice(annoying_answers)

def get_openai_response(user_question):
    messages = [{"role": "user", "content": user_question}]
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
        'max_tokens': 50,
        'temperature': 1.0
    }
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(OPENAI_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('choices')[0].get('message', {}).get('content', "I couldn't come up with an answer.")
    else:
        return f"Error {response.status_code}: {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    annoying_answer = ""
    openai_answer = ""
    
    if request.method == 'POST':
        user_input = request.form['question']
        annoying_answer = generate_annoying_answer()
        openai_answer = get_openai_response(user_input)

    return render_template('index.html', annoying_answer=annoying_answer, openai_answer=openai_answer)

if __name__ == '__main__':
    app.run(debug=True)
