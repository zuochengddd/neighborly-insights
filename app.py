import os
import openai
from flask import Flask, redirect, render_template, request, url_for,jsonify

from general_prompt import build_general_insights_prompt, get_insights_json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        input = request.form["user_ask"]
        prompt = "Concise but explicit. " + input
        # instead of providng raw data to open ai, we will call our internal services to build filtered analysis data
        json_data = get_insights_json()

        init_prompt = build_general_insights_prompt(json_data)

        messages = [
            {"role": "assistant", "content": "I am a helpful chatbot for Doordash"},
            {"role": "system", "content": init_prompt},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route('/question', methods=['POST'])
def process_questions():
    questions = request.json.get('questions')
    response = {
        'message': 'Received questions successfully',
        'questions': questions
    }
    return jsonify(response), 200
