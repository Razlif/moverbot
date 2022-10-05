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
        session["conversation_history"], session["last_message"] = [""] * 2
        session["client_inventory"] = []
        session["milegae_fee"] = 0
        [session["client_email"],
         session["pickup_zip"],
         session["delivery_zip"],
         session["pickup_state"],
         session["delivery_state"],
         session["move_type"],
         session["client_name"],
         session["client_phone"]] = ["None"] * 8
        [reply_text,
         session["stage"],
         session["pickup_zip"],
         session["delivery_zip"],
         session["pickup_state"],
         session["delivery_state"],
         session["milegae_fee"],
         session["client_inventory"],
         session["move_type"],
         session["client_name"],
         session["client_phone"],
         session["client_email"]] = functions.main_handler(session["stage"],
                                                           user_text,
                                                           session["conversation_history"],
                                                           session["pickup_zip"],
                                                           session["delivery_zip"],
                                                           session["pickup_state"],
                                                           session["delivery_state"],
                                                           session["milegae_fee"],
                                                           session["client_inventory"],
                                                           session["move_type"],
                                                           session["last_message"],
                                                           session["client_name"],
                                                           session["client_phone"],
                                                           session["client_email"])
    else:
        if "start over" in user_text or "Start over" in user_text:
            session.pop('stage', None)
            reply_text = functions.greeting
        else:
            [reply_text,
             session["stage"],
                session["pickup_zip"],
                session["delivery_zip"],
                session["pickup_state"],
                session["delivery_state"],
                session["milegae_fee"],
                session["client_inventory"],
                session["move_type"],
                session["client_name"],
                session["client_phone"],
                session["client_email"]] = functions.main_handler(session["stage"],
                                                                  user_text,
                                                                  session["conversation_history"],
                                                                  session["pickup_zip"],
                                                                  session["delivery_zip"],
                                                                  session["pickup_state"],
                                                                  session["delivery_state"],
                                                                  session["milegae_fee"],
                                                                  session["client_inventory"],
                                                                  session["move_type"],
                                                                  session["last_message"],
                                                                  session["client_name"],
                                                                  session["client_phone"],
                                                                  session["client_email"])
    session["last_message"] = reply_text
    session["conversation_history"] += "CLIENT: " + \
        user_text + " BOT: " + reply_text + " "
    return reply_text


if __name__ == "__main__":
    app.run()
