import os
import openai
from flask import Flask, redirect, render_template, request, url_for,jsonify
from flask_cors import CORS

from general_prompt import build_general_insights_prompt, get_insights_json

app = Flask(__name__)

cache = {}
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

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

    response = {
        'message': 'Received questions successfully',
        'reply': generate_reply(new_questions)
    }

    return jsonify(response), 200

def generate_reply(input):
    if 'initial_prompt' not in cache:
        json_data = get_insights_json()
        cache['initial_prompt'] = build_general_insights_prompt(json_data)
        cache['messages'] = []
        cache['messages'].append(
            {"role": "assistant", "content": "I am a helpful chatbot for Doordash"}
        )
        cache['messages'].append(
            {"role": "assistant", "content": cache['initial_prompt']}
        )

    decorated_user_question = input + """
    Try inspiring me with actions to take and prompt my next question.
    When you mention the store names, always decorate it as a HTML <a> link with the inner text as the store name, and href as the store's link.
    The whole response should be html markup which is ready to be inserted into a web page.
    Avoid mentioning detailed score, just compare.
    """

    cache['messages'].append(
        {"role": "user", "content": decorated_user_question}
    )
    messages = []
    messages.append(
        {"role": "assistant", "content": "I am a helpful chatbot for Doordash"}
    )
    messages.append(
        {"role": "assistant", "content": cache['initial_prompt']}
    )
    messages.append(
        {"role": "user", "content": decorated_user_question}
    )

    # instead of providing raw data to open ai, we will call our internal services to build filtered analysis data
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    result = response.choices[0].message.content
    cache['messages'].append(
        {"role": "assistant", "content": result}
    )
    return result
