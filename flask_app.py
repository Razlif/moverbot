import functions
from flask import Flask, render_template, request, session

app = Flask(__name__)
#app.static_folder = 'static'
app.secret_key = "SecretsOfMoverBot"


@app.route("/")
def home():
    return render_template("moverbot.html")

@app.route("/get")
def get_bot_response():
    user_text = str(request.args.get('msg'))
    if "stage" not in session:
        session["stage"] = 1
        session["conversation_history"] = ""
        session["pickup_zip"] = "None"
        session["delivery_zip"] = "None"
        session["pickup_state"] = "None"
        session["delivery_state"] = "None"
        session["client_inventory"] = []
        session["move_type"] = ""
        session["milegae_fee"] = 0
        session["last_message"] = ""
        session["client_name"] = "None"
        session["client_phone"] = "None"
        session["client_email"] = "None"
        prompt, reply_text, session["stage"], session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"], session["milegae_fee"], session["client_inventory"], session["client_name"], session["client_phone"], session["client_email"] = functions.main_handler(session["stage"], user_text, session["conversation_history"] , session["pickup_zip"] ,session["delivery_zip"], session["pickup_state"] ,session["delivery_state"] ,session["milegae_fee"] ,session["client_inventory"] ,session["last_message"] , session["client_name"], session["client_phone"], session["client_email"])
    else:
        if "start over" in user_text or "Start over" in user_text:
            session.pop('stage', None)
            reply_text = functions.greeting
            prompt = ""
        else:
            prompt, reply_text, session["stage"], session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"], session["milegae_fee"], session["client_inventory"], session["client_name"], session["client_phone"], session["client_email"] = functions.main_handler(session["stage"], user_text, session["conversation_history"] , session["pickup_zip"] ,session["delivery_zip"], session["pickup_state"] ,session["delivery_state"] ,session["milegae_fee"] ,session["client_inventory"] ,session["last_message"] , session["client_name"], session["client_phone"], session["client_email"])
    session["last_message"] = reply_text
    session["conversation_history"] += "CLIENT: " + user_text + " BOT: " + reply_text + " "
    prompt += reply_text
    return reply_text



if __name__ == "__main__":
    app.run()