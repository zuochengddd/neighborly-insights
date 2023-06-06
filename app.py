import os

import openai
import json
from flask import Flask, redirect, render_template, request, url_for,jsonify


general_prompt_tempalte ="""
Here is the general information of our store:
Our store name is {name} and located at {location}. And our sales data collected from Doordash like : {sales}. And our review summary collected by Doordash like : {review}
"""

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        input = request.form["user_ask"]

        json_data = get_insights_json()

        init_prompt = build_general_insights_prompt(json_data)

        messages = [
            {"role": "assistant", "content": "I am a helpful chatbot for Doordash"},
            {"role": "user", "content": init_prompt},
            {"role": "user", "content": input}
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

def build_general_insights_prompt(json_data):
    location = json_data["storeDetails"]["location"]
    name = json_data["storeDetails"]["name"]
    sales_data = json_data["generalCompsAnalysis"]["sales"]
    review_data = json_data["generalCompsAnalysis"]["reviewComparison"]

    return general_prompt_tempalte.format(name = name, location = location, sales = sales_data, review =review_data)

def get_insights_json():
    # dummy response from upstream dependencies
    file_path = "utils/sampleUpstreamResponse.json" 
    with open(file_path) as file:
        data = json.load(file)
        return data
