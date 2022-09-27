##########################
#     Import packages    #
##########################

from uszipcode import SearchEngine
import pgeocode
import openai
import json
import re
import phonenumbers
import settings
import jinja2
import prompts

###############################
#    render jinja elements    #
###############################

environment = jinja2.Environment()

conversation_starter_template = environment.from_string(prompts.conversation_starter_raw_text)

conversation_starter = conversation_starter_template.render(BOT_NAME=settings.bot_name, COMPANY_NAME=settings.company_name,
                                                            COMPANY_ADDRESS=settings.company_address, COMPANY_EMAIL=settings.company_email,
                                                            COMPANY_PHONE=settings.company_phone, COMPANY_TYPE=settings.company_type,
                                                            COMPANY_LICENSE=settings.company_license, YEARS_IN_OPERATION=settings.years_in_operation,
                                                            PRICE_PER_HOUR=settings.price_per_hour
                                                            )

greeting_template = environment.from_string(prompts.greeting_raw_text)

greeting = greeting_template.render(BOT_NAME=settings.bot_name)

general_task_template = environment.from_string(prompts.general_task_raw_text)

problem_items_template = environment.from_string(prompts.problem_items_raw_text)

price_reply_template = environment.from_string(prompts.price_reply_raw_text)


#######################
#    def functions    #
#######################

##### check for phone in user last entry
def check_phone(user_text):
    num = "+1" + user_text
    my_number = phonenumbers.parse(num)
    if (phonenumbers.is_valid_number(my_number)) is True:
        phone = user_text
    else:
        phone = "None"
    return phone

##### check for email in user last entry
def check_email(user_text):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, user_text)):
        email = user_text
    else:
        email = "None"
    return email

##### send message to openai api
def open_ai_api(message):
    openai.api_key = settings.openai_key
    response = openai.Completion.create(
    model=settings.model_name,
    prompt=message,
    temperature=0,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\"\"\""])
    ai_response = response['choices'][0]['text']
    return ai_response

##### check user last entry for location information
def check_user_text_for_location(user_text, stage):
    try:
        user_text_parsed = re.findall(r'\d+', user_text)
        if len(user_text_parsed[0])==5:
            engine = SearchEngine()
            location_data = engine.by_zipcode(user_text_parsed[0])
            state = location_data.state
            zipcode = location_data.zipcode
            stage += 1
        else:
            state = "None"
            zipcode = "None"
    except:
        state = "None"
        zipcode = "None"
    return state, zipcode, stage

##### calculate distance between 2 zipcodes
def get_distance(zip1, zip2):
    dist = pgeocode.GeoDistance('us')
    distance = dist.query_postal_code(zip1, zip2)
    return distance

##### load openai inventory calculation to json object
def load_item_list_to_json(ai_response):
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

##### add or delete item from user last entry onto his item list
def collect_items(user_text, inventory, stage):
    if "done" in user_text or "Done" in user_text:
        stage += 1
        reply_text = ""
    elif "delete" in user_text or "Delete" in user_text:
        del(inventory[-1])
        reply_text = "Deleted last entry"
    else:
        reply_text = "Added item"
        inventory.append(user_text)
    return stage, inventory, reply_text

##### calculate cubic ft based on item list
def calc_cf(ai_response):
    problem_items = []
    item_list_display = "YOUR ITEM LIST:<br>"
    all_items_cf = 0
    data = load_item_list_to_json(ai_response)
    try:
        data_results = data['results']
    except:
        data_results = data[0]
    for i in data_results:
        try:
            item_cf = i['CF']
            if item_cf > 0:
                if i['quantity'] == "a" or i['quantity'] == "an":
                    item_quantity = "1"
                else:
                    item_quantity = i['quantity']
                total_item_cf = int(item_cf)*int(item_quantity)
                item_list_display += i['name'] + " x " + str(item_quantity) + " | " + str(total_item_cf) + " CF <br>"
                all_items_cf += total_item_cf
            else:
                problem_items.append(i['name'])
        except:
            problem_items.append(i['name'])
    if problem_items != []:
        item_list_display += problem_items_template.render(problem_items=problem_items)
    return item_list_display, all_items_cf


##### calculate price based on cubic ft and mileage fee
def calculate_price(pickup_zip, delivery_zip, cubic_ft):
    disptch_to_pickup = get_distance(settings.dispatch_zipcode, pickup_zip)
    pickup_to_delivery = get_distance(pickup_zip, delivery_zip)
    delivery_to_dispatch = get_distance(delivery_zip, settings.dispatch_zipcode)
    mileage_fee = (int(disptch_to_pickup) + int(pickup_to_delivery) + int(delivery_to_dispatch)) * int(settings.mileage_fee)
    add_hours = int(cubic_ft) - int(settings.minimum_cf_per_job)
    if add_hours < 1:
        working_hours = int(settings.minimum_hours_per_job)
        working_hours_plus = working_hours+2
        price = int(working_hours*int(settings.price_per_hour))+int(mileage_fee)
        price_reply = price_reply_template .render( CUBIC_FT = cubic_ft, WORKING_HOURS = working_hours, WORKING_HOURS_PLUS = working_hours_plus,
                                                    PRICE_PER_HOUR = settings.price_per_hour, PRICE = price
                                                    )
    else:
        add_hours = int(add_hours/200)
        working_hours = float(settings.minimum_hours_per_job) + add_hours
        working_hours_plus = working_hours+2
        price = int(working_hours*float(settings.price_per_hour))+float(mileage_fee)
        price_reply = price_reply_template .render( CUBIC_FT = cubic_ft, WORKING_HOURS = int(working_hours), WORKING_HOURS_PLUS = int(working_hours_plus),
                                                    PRICE_PER_HOUR = settings.price_per_hour, PRICE = int(price)
                                                    )
    return price_reply

##### check openai response for mirror answers and answer loops
def check_message_for_errors(stage, reply_text, last_message, conversation_history, user_text):
    if reply_text in last_message or reply_text == user_text:
        if prompts.error_text in conversation_history:
            if stage == 1:
                reply_text = prompts.error_text_2 + prompts.ask_for_pickup_zipcode
            elif  stage == 2:
                reply_text = prompts.error_text_2 + prompts.ask_for_delivery_zipcode
            elif  stage == 5:
                reply_text = prompts.error_text_2 + prompts.ask_for_email
            elif  stage == 7:
                reply_text = prompts.error_text_2 + prompts.ask_for_phone
            elif  stage > 7:
                reply_text = prompts.error_text_2 + prompts.general_prompt
        else:
            reply_text = prompts.error_text
    return reply_text


####################################
#     main conversation handler    #
####################################


def main_handler(stage, user_text, conversation_history, pickup_zipcode, delivery_zipcode, pickup_state, delivery_state,mileage_fee, client_inventory ,last_message, client_name, client_phone, client_email):
    if stage == 1:
        pickup_state, pickup_zipcode, stage = check_user_text_for_location(user_text, stage)
        if pickup_state == "None":
            general_task = general_task_template.render(ASK_FOR="pickup zip code")
            prompt = conversation_starter + settings.questions + general_task + user_text + " BOT:"
            ai_response = open_ai_api(prompt)
            reply_text = check_message_for_errors(stage, ai_response, last_message, conversation_history, user_text)
        else:
            if pickup_state in settings.allowed_service_locations or pickup_zipcode in settings.allowed_service_locations:
                reply_text = "Great thanks" + prompts.ask_for_delivery_zipcode
            else:
                reply_text = prompts.out_of_service_area
                stage = 1
    elif stage == 2:
        delivery_state, delivery_zipcode, stage = check_user_text_for_location(user_text, stage)
        if delivery_state == "None":
            general_task = general_task_template.render(ASK_FOR="delivery zip code")
            prompt = conversation_starter + settings.questions + general_task + user_text + " BOT:"
            ai_response = open_ai_api(prompt)
            reply_text = check_message_for_errors(stage, ai_response, last_message, conversation_history, user_text)
        else:
            if delivery_state in settings.allowed_service_locations or delivery_zipcode in settings.allowed_service_locations:
                reply_text = "Great thanks" + prompts.ask_for_item_list
            else:
                reply_text = prompts.out_of_service_area
                stage = 2
    elif stage == 3:
        stage, client_inventory, reply_text = collect_items(user_text, client_inventory, stage)
        if stage == 4:
            prompt = settings.inventory_list + " client item list: " +str(client_inventory) + " " + prompts.inventory_task
            ai_response = open_ai_api(prompt)
            item_list_display, all_items_cf = calc_cf(ai_response)
            price_reply = calculate_price(pickup_zipcode, delivery_zipcode, int(all_items_cf))
            reply_text = item_list_display + price_reply + prompts.ask_for_email
            stage += 1
    elif stage == 5:
        if user_text in str(check_email(user_text)):
            client_email = user_text
            stage += 1
            reply_text = "Great thanks" + prompts.ask_for_name
        else:
            reply_text = prompts.ask_for_email
    elif stage == 6:
        client_name = user_text
        stage += 1
        reply_text = "Great thanks" + prompts.ask_for_phone
    elif stage == 7:
        if user_text in check_phone(user_text):
            client_phone = user_text
            stage += 1
            reply_text = "Great, your estimate is on it's way!<br>" + prompts.general_prompt
        else:
            reply_text = prompts.ask_for_phone
    else:
        general_task = general_task_template.render(ASK_FOR="any additional questions")
        prompt = conversation_starter + settings.questions + general_task + user_text + " BOT:"
        ai_response = open_ai_api(prompt)
        reply_text = check_message_for_errors(stage, ai_response, last_message, conversation_history, user_text)
    reply_text += "<br>"
    return reply_text, stage, pickup_zipcode, delivery_zipcode, pickup_state, delivery_state, mileage_fee, client_inventory, client_name, client_phone, client_email