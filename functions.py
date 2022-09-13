from uszipcode import SearchEngine
import pgeocode
import openai
import json
import re

greeting = "\nHi! I am moverbot, I'm in training so I still make a lot of mistakes, But I promiss to try my best! \n\nCan I help you get a moving estimate from big shoulders moving?"
ref_list= 'allowed list format: item_class{item_type}. allowed list: beds{single, twin, full, double, day bed, futon, queen, king, head board, foot board, box spring, mattress}, tables{vanity, end, sofa ,side, child, kitchen, dining, coffee, patio, changing, regular desk, large desk, entrance}, chairs{single, dining, kitchen, folding, high, arm, club, rocking, recliner, cushion, office, computer, child, wheel}, sofa{sofa, loveseat, 2 pcs sectional, ottoman}, appliances{stove, washer, dryer, tv under 60, tv over 60,  computer, stereo system, microwave, vacuum, dorm refrigerator, double door refrigerator, freezer}, storage{single dresser, double dresser, night stand, trunk, book case, book shelf, cube storage, plastic drawers, toy chest, wicker chest, regular chest, large chest, medium china cabinet, large china cabinet, curio cabinet, regular armoire, large armoire, kitchen island, 1 pc buffet, credenza, metal shelving unit}, other{rug, mirror, fan, lamp, medium picture, large picture, ladder, tool box, barbeque, garden tool, lawn mower push, generator, guitar, upright piano, baby grand piano, bicycle, other small appliance, other medium appliance, other large appliance, other small furniture, other medium furniture, other large furniture, other small item, other medium item }, boxes{small box, medium box, large box, wardrobe box, plastic bin, suitcase, bag}, forbidden{animals, plants, hazardous materials, guns, ammunition, cars, people, locations, vehicles, public property, public transport, unmovable object}. results example in json: {"results": [{"item_name": "item_name", "item_class": "item_class", "item_type": "item_type", "quantity": "item_quantity"}, {"item_name": "item_name", "item_class": "item_class", "item_type": "item_type", "quantity": "item_quantity"}, {"item_name": "item_name", "item_class": "item_class", "item_type": "item_type", "quantity": "item_quantity"}]} \\ finish results '
list_prompt= 'based on the allowed list and results example return results.json: '
pickup_prompt= 'about big shoulders moving company: Based in Wood Dale IL Big Shoulders Moving & Storage is your number one choice for a moving carrier. We are the actual carrier licensed and insured, using our trucks and experiend movers we do everything to provide the best moving service along side competative direct carrier rates. about moverbot: moverbot is a chatbot by big shoulders moving company, he can always help the client. required moverbot tasks: 1. always answer client questions.  2. always ask the client for the pick up zip code. 3. help the client with big shoulders moving services. moverbot reply format in json: {"results": [{"moverbot_reply_text": "mover bot reply", "zipcode_detected": "True | False", "zip_code": "unknown | zip_code"}]}. dialog: moverbot: Can I help you get a moving estimate from big shoulders moving?  client: '
delivery_prompt= 'about big shoulders moving company: Based in Wood Dale IL Big Shoulders Moving & Storage is your number one choice for a moving carrier. We are the actual carrier licensed and insured, using our trucks and experiend movers we do everything to provide the best moving service along side competative direct carrier rates. about moverbot: moverbot is a chatbot by big shoulders moving company, he can always help the client. required moverbot tasks: 1. always answer client questions. 2. always ask the client for the delivery zip code.  3. help the client with big shoulders moving services. moverbot reply format in json: {"results": [{"moverbot_reply_text": "mover bot reply", "zipcode_detected": "True | False", "zip_code": "unknown | zip_code"}]}. dialog: moverbot: Can I help you get a moving estimate from big shoulders moving?  client: '
error_text = "This is emberassing...looks like I'm stuck. Can you please rephrase your message?"

def open_ai_api(message):
    openai.api_key = "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"
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=message,
    temperature=0,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\"\"\""])
    ai_response = response['choices'][0]['text']
#    print(reply_text)
    return ai_response

def get_state(zip_code):
    engine = SearchEngine()
    zipcode = engine.by_zipcode(zip_code)
#    print(zipcode.state)
    state = zipcode.state
    return state

def get_distance(zip1, zip2):
    dist = pgeocode.GeoDistance('us')
    print(dist.query_postal_code(zip1, zip2))
    distance = dist.query_postal_code(zip1, zip2)
    return distance


def load_ai_response_to_json(ai_response):
    try:
        data_json = json.loads(ai_response)
    except:
        x = ai_response.split('}]', 1)
        mover_bot =  x[0] + '}]}'
        try:
            data_json = json.loads(mover_bot)
        except:
            mover_bot ='{"results":' + mover_bot
            data_json = json.loads(mover_bot)
    return data_json

def get_state_from_user_text(user_input):
    try:
        zip_code = re.findall(r'\d+', str(user_input))
#        print("zipcode: " + str(zip_code[0]))
        state = get_state(str(zip_code[0]))
#        print("state: " + state)
    except:
        state = "None"
#        print("state: " + state)
    return str(state)

def get_move_type(pickup_zip, delivery_zip, pickup_state, delivery_state):
    dispatch_zip = "60191"
    if pickup_state == delivery_state:
        disptch_to_pickup = get_distance(str(dispatch_zip), str(pickup_zip))
        pickup_to_delivery = get_distance(str(pickup_zip), str(delivery_zip))
        delivery_to_dispatch = get_distance(str(delivery_zip), str(dispatch_zip))
        move_type = "Local Move"
#        print("Local Move")
        try:
            mileage_fee = (int(disptch_to_pickup) + int(pickup_to_delivery) + int(delivery_to_dispatch)) * 2
        except:
            mileage_fee = 0
#        print("Mileage Fee: " + str(mileage_fee))
    else:
        move_type = "Long Distance Move"
#        print("Long Distance Move")
        mileage_fee = 0
    return move_type, mileage_fee

def get_reply_text_from_json(data_json):
    try:
        reply_text = data_json[0]['moverbot_reply_text']
    except:
        try:
            reply_text = data_json['moverbot_reply_text']
        except:
            reply_text = data_json['results'][0]['moverbot_reply_text']
    return reply_text

def stage_one(user_input, data_json):
    if "None" in str(get_state_from_user_text(user_input)):
        pickup_state = "None"
        stage = "1"
        reply_text = get_reply_text_from_json(data_json)
    else:
        pickup_state = str(get_state_from_user_text(user_input))
#        print(pickup_state)
        stage = "2"
        reply_text = "Pick up from: " + pickup_state + " Detected. \nGreat, thanks. Now please enter your delivery zip code."
    return stage ,reply_text, pickup_state

def stage_two(user_input, data_json):
    if "None" in str(get_state_from_user_text(user_input)):
        delivery_state = "None"
        stage = "2"
        reply_text = get_reply_text_from_json(data_json)
    else:
        delivery_state = str(get_state_from_user_text(user_input))
        stage = "3"
        reply_text = "Delivery to: " + delivery_state + " Detected.\n"
    return stage ,reply_text, delivery_state


def stage_three(pickup_zip, delivery_zip, pickup_state, delivery_state):
    move_type, mileage_fee = get_move_type(pickup_zip, delivery_zip, pickup_state, delivery_state)
    stage = "4"
    return stage, move_type, mileage_fee

def stage_four(user_input, inventory):
    if "done" in user_input or "Done" in user_input:
        stage = "5"
        reply_text = "\nItem list\n" + str(inventory) + "\n\nOne moment please I am calculating your results...\n"
        print(reply_text)
    elif "delete" in user_input or "Delete" in user_input:
        del(inventory[-1])
        stage = "4"
        reply_text = "Deleted last entry"
    else:
        stage = "4"
        reply_text = "Got it"
        inventory.append(user_input)
    return stage, inventory, reply_text

def stage_five(inventory):
    item_list_final, stage, all_items_cf = calc_cf(inventory)
    return item_list_final, stage, all_items_cf

def stage_six(user_input):
    task = " based on the dialog return moverbot reply. results.json:"
    prompt ='about big shoulders moving company: Based in Wood Dale IL Big Shoulders Moving & Storage is your number one choice for a moving carrier. We are the actual carrier licensed and insured, using our trucks and experiend movers we do everything to provide the best moving service along side competative direct carrier rates. about moverbot: moverbot is a chatbot by big shoulders moving company, he can always help the client. required moverbot tasks: 1. always answer client questions.  2. help the client with big shoulders moving services. moverbot reply format in json: {"results": [{"moverbot_reply_text": "mover bot reply"}]}. dialog: moverbot: How can I help you today?  client: '
    message = prompt + user_input + " moverbot: " + task
    ai_response = open_ai_api(message)
    data_json = load_ai_response_to_json(ai_response)
    reply_text = get_reply_text_from_json(data_json)
    stage = "6"
    return stage, reply_text

def check_message_for_errors(stage, reply_text, last_message, error_text, conv_history, user_text):
    if last_message in reply_text or "moverbot reply" in reply_text or "mover bot reply" in reply_text or reply_text == user_text:
        print("bad reply: " + reply_text)
        if error_text in conv_history and stage=="1":
            reply_text = "Looks like I am still having a problem. To continue getting your estimate please enter a pick up zip code."
        elif error_text in conv_history and stage=="2":
            reply_text = "Looks like I am still having a problem. To continue please enter your delivery zip code or 'start over' to restart the chat."
        elif error_text in conv_history and stage=="6":
            reply_text = "Looks like I am still having a problem. Try typing 'start over' to restart the chat"
        else:
            reply_text = error_text
    return reply_text

def main(stage, conv_history, user_text, pickup_zip, delivery_zip, pickup_state, delivery_state, inventory, move_type, mileage_fee, last_message):
    if stage == "1":
        task = " based on the dialog return moverbot reply. results.json:"
        prompt = pickup_prompt + conv_history + user_text + task
        ai_response = open_ai_api(prompt)
        data_json = load_ai_response_to_json(ai_response)
        stage ,reply_text, pickup_state  = stage_one(user_text, data_json)
        reply_text = check_message_for_errors(stage, reply_text, last_message, error_text, conv_history, user_text)
    elif stage == "2":
        task = " based on the dialog return moverbot reply. results.json:"
        prompt = delivery_prompt + conv_history + task
        ai_response = open_ai_api(prompt)
        data_json = load_ai_response_to_json(ai_response)
        stage ,reply_text, delivery_state = stage_two(user_text, data_json)
        if stage == "3":
            stage, move_type, mileage_fee = stage_three(pickup_zip, delivery_zip, pickup_state, delivery_state)
            reply_text += "\nMove type: " + move_type + "\nGreat, thanks. Now please enter your item list, try to enter each item in a new line, you can enter 'delete' to remove the last item or 'done' when you are finished."
        else:
            reply_text = check_message_for_errors(stage, reply_text, last_message, error_text, conv_history, user_text)
    elif stage == "4":
        stage, inventory, reply_text = stage_four(user_text, inventory)
        if stage == "5":
            item_list_final, stage, all_items_cf = stage_five(inventory)
            price_reply = calculate_rate(int(all_items_cf), pickup_state, delivery_state, move_type)
            reply_text = item_list_final + price_reply
    else:
        stage ,reply_text = stage_six(user_text)
        reply_text = check_message_for_errors(stage, reply_text, last_message, error_text, conv_history, user_text)
    return stage, reply_text, conv_history, user_text, pickup_zip, delivery_zip, pickup_state, delivery_state, inventory, move_type, mileage_fee


def calc_cf(inventory):
    problem_items = "<br>I am afraid there are a few items I couldn't locate: "
    item_list_display = ""
    inventory = "client item list: " + str(inventory)
    prompt= 'based on the allowed list and results example return results.json: '
    ref_list= 'allowed list format: item_class{item_type}. allowed list: beds{single, twin, full, double, day bed, futon, queen, king, head board, foot board, box spring, mattress}, tables{vanity, end, sofa ,side, child, kitchen, dining, coffee, patio, changing, regular desk, large desk, entrance}, chairs{single, dining, kitchen, folding, high, arm, club, rocking, recliner, cushion, office, computer, child, wheel}, sofa{sofa, loveseat, 2 pcs sectional, ottoman}, appliances{stove, washer, dryer, tv under 60, tv over 60,  computer, stereo system, microwave, vacuum, dorm refrigerator, double door refrigerator, freezer}, storage{single dresser, double dresser, night stand, trunk, book case, book shelf, cube storage, plastic drawers, toy chest, wicker chest, regular chest, large chest, medium china cabinet, large china cabinet, curio cabinet, regular armoire, large armoire, kitchen island, 1 pc buffet, credenza, metal shelving unit}, other{rug, mirror, fan, lamp, medium picture, large picture, ladder, tool box, barbeque, garden tool, lawn mower push, generator, guitar, upright piano, baby grand piano, bicycle, other small appliance, other medium appliance, other large appliance, other small furniture, other medium furniture, other large furniture, other small item, other medium item }, boxes{small box, medium box, large box, wardrobe box, plastic bin, suitcase, bag}, forbidden{animals, plants, hazardous materials, guns, ammunition, cars, people, locations, vehicles, public property, public transport, unmovable object}. results example in json: {"results": [{"item_name": "item_name", "item_class": "item_class", "item_type": "item_type", "quantity": "item_quantity"}, {"item_name": "item_name", "item_class": "item_class", "item_type": "item_type", "quantity": "item_quantity"}, {"item_name": "item_name", "item_class": "item_class", "item_type": "item_type", "quantity": "item_quantity"}]} \\ finish results '
    item_request = ref_list + " " + inventory + " " + prompt
    ai_response = open_ai_api(item_request)
    data = load_ai_response_to_json(ai_response)
    try:
        data_results = data['results']
    except:
        data_results = data[0]
    item_list_final = ""
    all_items_cf = 0
    for i in data_results:
        item_quantity = ""
        try:
            if i['quantity'] =="a":
                item_quantity = "1"
            else:
                item_quantity = i['quantity']
            total_cf = 0
            item_cf = ""
            if "bed" in i['item_class']:
                if "single" in i['item_type']:
                    item_cf = "50"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "twin" in i['item_type']:
                    item_cf = "50"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "full" in i['item_type']:
                    item_cf = "50"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "double" in i['item_type']:
                    item_cf = "50"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "day" in i['item_type']:
                    item_cf = "50"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "queen" in i['item_type']:
                    item_cf = "75"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "king" in i['item_type']:
                    item_cf = "95"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "head board" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "foot board" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "box spring" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "mattress" in i['item_type']:
                    item_cf = "40"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "night stand" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                else:
                    item_cf = "50"
                    total_cf = int(item_cf)*int(item_quantity)
            if "table" in i['item_class']:
                if "night stand" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "vanity" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "end" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "sofa" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "side" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "child" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "kitchen" in i['item_type']:
                    item_cf = "30"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "dining" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "coffee" in i['item_type']:
                    item_cf = "20"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "patio" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "changing" in i['item_type']:
                    item_cf = "20"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "regular desk" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large desk" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "entrance" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                else:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
            if "chair" in i['item_class']:
                if "single" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "dining" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "kitchen" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "folding" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "high" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "arm" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "club" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "rocking" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "recliner" in i['item_type']:
                    item_cf = "20"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "cushion" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "office" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "computer" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "child" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "wheel" in i['item_type']:
                    item_cf = "35"
                    total_cf = int(item_cf)*int(item_quantity)
                else:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
            if "storage" in i['item_class']:
                if " single dresser" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "double dresser" in i['item_type']:
                    item_cf = "40"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "night stand" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "trunk" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "book case" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "book shelf" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "cube storage" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "plastic" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "toy" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "wicker" in i['item_type']:
                    item_cf = "20"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "regular chest" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large chest" in i['item_type']:
                    item_cf = "40"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "medium china cabinet" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large china cabinet" in i['item_type']:
                    item_cf = "65"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "curio" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "regular armoire" in i['item_type']:
                    item_cf = "40"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large armoire" in i['item_type']:
                    item_cf = "55"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "kitchen island" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "buffet" in i['item_type']:
                    item_cf = "35"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "credenza" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "metal shelving unit" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "other small furniture" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "other medium furniture" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "other large furniture" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                else:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
            if "appliance" in i['item_class']:
                if "stove" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "washer" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "dryer" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "tv under 60" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "tv over 60" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "computer" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "stereo" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "microwave" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "vacuum" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "dorm refrigerator" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "double door refrigerator" in i['item_type'] :
                    item_cf = "60"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "freezer" in i['item_type']:
                    item_cf = "40"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "small appliance" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "medium appliance" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large appliance" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                else:
                    item_cf = "20"
                    total_cf = int(item_cf)*int(item_quantity)
            if "sofa" in i['item_class']:
                if "sofa" in i['item_type']:
                    item_cf = "60"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "loveseat" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "sectional" in i['item_type']:
                    item_cf = "90"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "ottoman" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
            if "box" in i['item_class']:
                if "small box" in i['item_type']:
                    item_cf = "2"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "medium box" in i['item_type']:
                    item_cf = "3"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large box" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "wardrobe box" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "plastic bin" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "suitcase" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "bag" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                else:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
            if "other" in i['item_class']:
                if "rug" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "mirror" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "fan" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "lamp" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "medium picture" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large picture" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "ladder" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "tool" in i['item_type']:
                    item_cf = "20"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "barbeque" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "garden tool" in i['item_type']:
                    item_cf = "5"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "lawn mower" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "generator" in i['item_type']:
                    item_cf = "15"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "guitar" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "baby grand piano" in i['item_type']:
                    item_cf = "120"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "bicycle" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "small appliance" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "medium appliance" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large appliance" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "small furniture" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "medium furniture" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "large furniture" in i['item_type']:
                    item_cf = "45"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "small item" in i['item_type']:
                    item_cf = "10"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "medium item" in i['item_type']:
                    item_cf = "25"
                    total_cf = int(item_cf)*int(item_quantity)
            if "forbidden" in i['item_class']:
                if "animal" in i['item_type']:
                    item_cf = "0"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "plants" in i['item_type']:
                    item_cf = "0"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "hazardous" in i['item_type']:
                    item_cf = "0"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "gun" in i['item_type']:
                    item_cf = "0"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "ammunition" in i['item_type']:
                    item_cf = "0"
                    total_cf = int(item_cf)*int(item_quantity)
                elif "car" in i['item_type']:
                    item_cf = "0"
                    item_quantity = i['quantity']
                    total_cf = int(item_cf)*int(item_quantity)
                elif "people" in i['item_type']:
                    item_cf = "0"
                    total_cf = int(item_cf)*int(item_quantity)
                else:
                    item_cf = "0"
                    total_cf = int(item_cf)*int(item_quantity)
#            print("item name: " + i['item_name'] + " | item class: " + i['item_class'] + " | item type: " + i['item_type'] + " | cf: " + str(item_cf) + " | quantity: " + str(item_quantity) + " | total per item: " + str(total_cf) + "\n")
            all_items_cf += total_cf
            item_list_final += "item name: " + i['item_name'] + " | item class: " + i['item_class'] + " | item type: " + i['item_type'] + " | cf: " + str(item_cf) + " | quantity: " + str(item_quantity) + " | total per item: " + str(total_cf) + "\n"
            if "forbidden" in str(i) or str(item_cf) == "0":
                problem_items += i['item_name'] + ", "
            else:
                item_list_display += i['item_name'] + " x " + str(item_quantity) + " | " + str(total_cf) + " CF <br>"
        except:
            print("could not get item: " +i['item_name'] )
            problem_items += i['item_name'] + ", "
    item_list_final += "\nTotal Volume: " + str(all_items_cf)
    give_cf = "<br>Thank you for waiting, based on your item list I estimate your move will take " + str(all_items_cf) + " Cubic Feet"
    if problem_items == "<br>I am afraid there are a few items I couldn't locate: ":
        final_message = "ITEM LIST:<br>" + item_list_display + give_cf
    else:
        final_message = "Thank you for waiting<br><br>ITEM LIST:<br>" + item_list_display + problem_items + " This doesn't mean we can't take them but I will need a human collegue to review them first."+ give_cf
    stage = "6"
    return final_message, stage, all_items_cf

def calculate_rate(cubic_ft, pick_up, delivery, move_type):
    ask_for_email = "<br>I will need some information in order to send you the quote.<br>Please enter a good email address where I can send you the estimate: "
    service_includes = "<br><br>The price is for full door to door service including:<br> -- Loading and unloading<br> -- Dissasembley and reassembley of the furniture<br> -- All of the labor, taxes, tolls, gas and basic coverage are included<br> -- Free use of blakets and moving pads to - we will wrap all of your belongings<br>We are of course the actual carrier, licensed and insured<br>"
    if move_type == "Local Move":
        if float(cubic_ft) < 350:
            working_hours = "3"
        elif float(cubic_ft) < 650:
            working_hours = "3-6"
        elif float(cubic_ft) < 1050:
            working_hours = "5-8"
        elif float(cubic_ft) < 1550:
            working_hours = "6-9"
        else:
            working_hours = "9-12"
        give_price = "<br>Our hourly rate for the moving team and truck is $250.<br>Based on the volume your move will take " + working_hours + " hours. "
        full_price_reply = give_price + service_includes + ask_for_email
    else:
        if pick_up == "IL" or pick_up == "IN" or pick_up == "WI" or pick_up == "MI":
            if delivery == "IL" or delivery == "IN" or delivery == "WI" or delivery == "MI":
                if float(cubic_ft) > 1799:
                    base_rate = 3.27
                elif float(cubic_ft) < 1800 and float(cubic_ft) > 1399:
                    base_rate = 3.27
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 3.55
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 499:
                    base_rate = 4.11
                elif float(cubic_ft) < 500 and float(cubic_ft) > 399:
                    base_rate = 5.22
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 5.22
                else:
                    base_rate = 6.88
            elif delivery == "AL" or delivery == "AR" or delivery == "CT" or delivery == "DC" or delivery == "DE" or delivery == "IA" or delivery == "GA" or delivery == "KY" or delivery == "MA" or delivery == "MD" or delivery == "MN" or delivery == "MO" or delivery == "MS" or delivery == "NC" or delivery == "NJ" or delivery == "NY" or delivery == "OH" or delivery == "OK" or delivery == "PA" or delivery == "RI" or delivery == "SC" or delivery == "TN" or delivery == "TX" or delivery == "VA" or delivery == "WV":
                if float(cubic_ft) > 999:
                    base_rate = 4.6
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 599:
                    base_rate = 4.9
                elif float(cubic_ft) < 600 and float(cubic_ft) > 399:
                    base_rate = 5.5
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 6.10
                else:
                    base_rate = 6.4
            elif delivery == "FL" or delivery == "NH" or delivery == "VT":
                if float(cubic_ft) > 1399:
                    base_rate = 4.6
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 4.9
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 799:
                    base_rate = 5.2
                elif float(cubic_ft) < 800 and float(cubic_ft) > 599:
                    base_rate = 5.5
                elif float(cubic_ft) < 600 and float(cubic_ft) > 499:
                    base_rate = 5.8
                elif float(cubic_ft) < 500 and float(cubic_ft) > 299:
                    base_rate = 6.75
                else:
                    base_rate = 6.75
            elif delivery == "AZ" or delivery == "CO" or delivery == "KS" or delivery == "CA" or delivery == "NE" or delivery == "NM" or delivery == "NV" or delivery == "UT" or delivery == "WY":
                if float(cubic_ft) > 1399:
                    base_rate = 5.5
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 5.8
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 799:
                    base_rate = 5.95
                elif float(cubic_ft) < 800 and float(cubic_ft) > 399:
                    base_rate = 6.10
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 6.75
                else:
                    base_rate = 7.01
            elif delivery == "LA" or delivery == "ME" or delivery == "MT" or delivery == "ID" or delivery == "ND" or delivery == "OR" or delivery == "SD" or delivery == "WA":
                if float(cubic_ft) > 1399:
                    base_rate = 6.10
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 6.40
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 399:
                    base_rate = 6.75
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 7.35
                else:
                    base_rate = 7.35
            else:
                base_rate = 7.35
        elif pick_up == "MN" or pick_up == "IA":
            if delivery == "IL" or delivery == "IA" or delivery == "WI" :
                if float(cubic_ft) > 1799:
                    base_rate = 3.33
                elif float(cubic_ft) < 1800 and float(cubic_ft) > 1399:
                    base_rate = 3.33
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 3.61
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 499:
                    base_rate = 4.16
                elif float(cubic_ft) < 500 and float(cubic_ft) > 399:
                    base_rate = 5.27
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 5.27
                else:
                    base_rate = 6.94
            elif delivery == "AL" or delivery == "AR" or delivery == "CT" or delivery == "DC" or delivery == "DE" or delivery == "GA" or delivery == "IN" or delivery == "KY" or delivery == "MA" or delivery == "MD" or delivery == "MI" or delivery == "MO" or delivery == "MS" or delivery == "NC" or delivery == "NJ" or delivery == "NY" or delivery == "OH" or delivery == "OK" or delivery == "PA" or delivery == "RI" or delivery == "SC" or delivery == "TN" or delivery == "TX" or delivery == "VA" or delivery == "WV":
                if float(cubic_ft) > 999:
                    base_rate = 5.1
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 599:
                    base_rate = 5.4
                elif float(cubic_ft) < 600 and float(cubic_ft) > 399:
                    base_rate = 6.1
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                        base_rate = 6.75
                else:
                    base_rate = 7.1
            elif delivery == "FL" or delivery == "NH" or delivery == "VT":
                if float(cubic_ft) > 1399:
                    base_rate = 5.1
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 5.4
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 799:
                    base_rate = 5.7
                elif float(cubic_ft) < 800 and float(cubic_ft) > 599:
                    base_rate = 6.1
                elif float(cubic_ft) < 600 and float(cubic_ft) > 499:
                    base_rate = 6.4
                elif float(cubic_ft) < 500 and float(cubic_ft) > 399:
                    base_rate = 7.4
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 7.4
                else:
                    base_rate =7.4
            elif delivery == "AZ" or delivery == "CO" or delivery == "KS" or delivery == "CA" or delivery == "NE" or delivery == "NM" or delivery == "NV" or delivery == "UT" or delivery == "WY":
                if float(cubic_ft) > 1399:
                    base_rate = 6.1
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 6.4
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 799:
                    base_rate = 6.55
                elif float(cubic_ft) < 800 and float(cubic_ft) > 399:
                    base_rate = 6.75
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 7.4
                else:
                    base_rate = 7.75
            elif delivery == "LA" or delivery == "ME" or delivery == "MT" or delivery == "ID" or delivery == "ND" or delivery == "OR" or delivery == "SD" or delivery == "WA":
                if float(cubic_ft) > 1399:
                    base_rate = 6.75
                elif float(cubic_ft) < 1400 and float(cubic_ft) > 999:
                    base_rate = 7.1
                elif float(cubic_ft) < 1000 and float(cubic_ft) > 399:
                    base_rate = 7.4
                elif float(cubic_ft) < 400 and float(cubic_ft) > 299:
                    base_rate = 8.1
                else:
                    base_rate = 8.1
            else:
                base_rate = 8.1
        else:
            base_rate = 8.1
        final_price = ((float(cubic_ft) * float(base_rate)) * 1.07) * 0.9
        final_price_str = str(int(final_price))
        give_price = "<br>Which we can do for exactly $" + final_price_str
        full_price_reply = give_price + service_includes + ask_for_email
    return full_price_reply