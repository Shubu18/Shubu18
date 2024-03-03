from flask import Flask, render_template, request
import google.generativeai as genai

genai.configure(api_key="")

app = Flask(__name__)


def ai(text):
    generation_config = {
        "temperature": 0,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    prompt_parts = [text]

    response = model.generate_content(prompt_parts)
    return response.text


def add_response(re):
    with open("responses.txt", "a") as file:
        file.write(re + "\n")


def readresponses():
    with open("responses.txt", "r") as file:
        responses = file.readlines()
        # Clearing the file
    open("responses.txt", "w").close()
    return responses


@app.route('/')
def get_all_posts():
    return render_template("index.html", )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/ChatBot", methods=["POST", "GET"])
def chatbot():
    if request.method == "POST":
        data = request.form
        a = data["aa"]
        response = ai(a).replace("*", "")
        add_response(response)
        print(response)
        return render_template("chatbot.html", msg_sent=True, datas=readresponses())
    return render_template("chatbot.html", msg_sent=False)


@app.route("/Add_Quotes", methods=["POST", "GET"])
def add_quotes():
    if request.method == "POST":
        data = request.form
        a = data["naam"]
        b = data["quot"]
        with open("quotes.txt", "a") as file:
            file.write(f"\n{b}" f"\n{a}")
            return render_template('ad_quote.html')
    return render_template('ad_quote.html')


@app.route("/quotes")
def quotes():
    with open("quotes.txt", "r") as file:
        responses = file.readlines()
    return render_template('quote.html', datas=responses)


if __name__ == "__main__":
    app.run(debug=True)
