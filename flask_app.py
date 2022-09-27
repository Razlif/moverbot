import functions
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "SecretsOfMoverBot"


@app.route("/")
def home():
    return render_template("moverbot.html")

@app.route("/get")
def get_bot_response():
    user_text = str(request.args.get('msg'))
    reply_text= ""
    if "stage" not in session:
        session["stage"] = 1
        session["conversation_history"], session["move_type"], session["last_message"]  = [""]*3
        session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"], session["client_name"], session["client_phone"], session["client_email"] = ["None"]*7
        session["client_inventory"] = []
        session["milegae_fee"] = 0
        output_vars = [
            reply_text, session["stage"], session["pickup_zip"], session["delivery_zip"], session["pickup_state"], session["delivery_state"],
            session["milegae_fee"], session["client_inventory"], session["client_name"], session["client_phone"], session["client_email"]
            ]
        input_vars = [
            session["stage"], user_text, session["conversation_history"] , session["pickup_zip"] ,session["delivery_zip"], session["pickup_state"], session["delivery_state"],
            session["milegae_fee"] ,session["client_inventory"] ,session["last_message"] , session["client_name"], session["client_phone"], session["client_email"]
            ]
        output_vars = functions.main_handler(*input_vars)
    else:
        if "start over" in user_text or "Start over" in user_text:
            session.pop('stage', None)
            output_vars[0] = functions.greeting
        else:
            output_vars = functions.main_handler(*input_vars)
    session["last_message"] = output_vars[0]
    session["conversation_history"] += "CLIENT: " + user_text + " BOT: " + output_vars[0] + " "
    return output_vars[0]


if __name__ == "__main__":
    app.run()
