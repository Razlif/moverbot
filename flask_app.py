from functions import *
from flask import Flask, render_template, request, session

app = Flask(__name__)
#app.static_folder = 'static'
app.secret_key = "SecretsOfMoverBot"

@app.route("/moverbot")
def moverbotapp():
    return render_template("moverbot.html")

@app.route("/")
def home():
    return render_template("moverbot.html")

@app.route("/get")
def get_bot_response():
    user_text = str(request.args.get('msg'))
    if "stage" not in session:
        session["stage"] = "1"
        session["conv_history"] = ""
        session["pickup_zip"] = "None"
        session["delivery_zip"] = "None"
        session["pickup_state"] = "None"
        session["delivery_state"] = "None"
        session["inventory"] = []
        session["move_type"] = ""
        session["milegae_fee"] = 0
        session["last_message"] = "moverbot reply"
        session["stage"], reply_text, session["conv_history"], user_text, session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"], session["inventory"], session["move_type"], session["milegae_fee"] =  main(session["stage"], session["conv_history"], user_text, session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"], session["inventory"], session["move_type"], session["milegae_fee"], session["last_message"])
    else:
        if "start over" in user_text or "Start over" in user_text:
            session.pop('stage', None)
            reply_text = "\nHi! I am moverbot, I'm in training so I still make a lot of mistakes, But I promiss to try my best! \n\nCan I help you get a moving estimate from big shoulders moving?"
        else:
            session["stage"], reply_text, session["conv_history"], user_text, session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"], session["inventory"], session["move_type"], session["milegae_fee"] =  main(session["stage"], session["conv_history"], user_text, session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"], session["inventory"], session["move_type"], session["milegae_fee"], session["last_message"])
            session["last_message"] = reply_text
            session["conv_history"] += "client: " + user_text + " moverbot: " + reply_text
    return reply_text



if __name__ == "__main__":
    app.run()