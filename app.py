import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        input = request.form["user_ask"]
        # print(input)
        # prompt = generate_insights_prompt(input)
        # print(prompt)
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=prompt,
        #     temperature=0.6,
        #     max_tokens=2000
        # )
        #print(response)
        #response = build_optimzied_response()
        response = build_chat_response()
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

def generate_insights_prompt(input):
    return """
    My store: Monthly Sales : $1000, average item price inflation rate: 1.2, and order rate 78/day.
    Store 1: Monthly sales: $2000, average item price inflation rate: 1.0, order rate 200/day.
    Store 2: Monthly sales: $3000, avereage item price inflation rate: 1.5 order rate  15/day

    Question: {}, make sure it includes all the data attributes. """.format(input)



# example respons: Your store keep me up to date by sending short sms about the product. You gain my trust because you make sure I'm buying the right product. However, you can improve by sending me vouchers discount to boost sales
def build_optimzied_response():
    return openai.Edit.create(
        model="text-davinci-edit-001",
        input="Your store did a good job but there are few more area can improve to boost sales",
        instruction="Make it friendly and clear"
    )


def build_chat_response():
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
