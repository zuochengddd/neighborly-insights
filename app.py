import os
import openai
from flask import Flask, redirect, render_template, request, url_for,jsonify, g
from flask_cors import CORS

from general_prompt import build_general_insights_prompt, get_insights_json

app = Flask(__name__)
CORS(app)
def initialize_map():
    g.messages = [
        {"role": "assistant", "content": "I am a helpful chatbot for Doordash"}
    ]
    g.initial_prompt = None

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.before_request
def before_request():
    initialize_map()

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        input = request.form["user_ask"]

        return redirect(url_for("index", result=generate_reply(input)))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route('/question', methods=['POST'])
def process_questions():

    new_questions = request.json.get('questions')
    print("quesiton is:" + new_questions)
    response = {
        'message': 'Received questions successfully',
        'reply': generate_reply(new_questions)
    }
    return jsonify(response), 200

def generate_reply(input):
    if g.initial_prompt is None:
        json_data = get_insights_json()
        g.initial_prompt = build_general_insights_prompt(json_data)
        g.messages.append(
            {"role": "system", "content": g.initial_prompt}
        )

    decorated_user_question = input + ". Try inspiring me with actions to take and prompt my next question"
    g.messages.append(
        {"role": "user", "content": decorated_user_question }
    )

    # instead of providing raw data to open ai, we will call our internal services to build filtered analysis data
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=g.messages
    )

    result = response.choices[0].message.content

    g.messages.append(
        {"role": "assistant", "content": result}
    )
    return result
