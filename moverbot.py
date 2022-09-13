from functions import *

###### VARIABLES

pickup_zip = "None"
delivery_zip = "None"
pickup_state = "None"
delivery_state = "None"
inventory = []
conv_history = ""
move_type = ""
mileage_fee = 0
run = True
last_message = "mover bot reply"
stage = "1"

########## GREETING
print(greeting)


###### CONVERSATION LOOP

while run==True:
#    print("stage: " + stage)
    user_text = input("")
    if "start over" in user_text:
        pickup_zip = "None"
        delivery_zip = "None"
        pickup_state = "None"
        delivery_state = "None"
        inventory = []
        conv_history = "dialog: "
        move_type = ""
        mileage_fee = 0
        run = True
        last_message = "mover bot reply"
        stage = "1"
        print(greeting)
    if "exit chat" in user_text:
        run = False
    else:
        stage, reply_text, conv_history, user_text, pickup_zip, delivery_zip, pickup_state, delivery_state, inventory, move_type, mileage_fee =  main(stage, conv_history, user_text, pickup_zip, delivery_zip, pickup_state, delivery_state, inventory, move_type, mileage_fee, last_message)
        print(reply_text)
        last_message = reply_text
        conv_history += "client: " + user_text + " moverbot: " + reply_text