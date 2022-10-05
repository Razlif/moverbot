
error_text = "This is embarrassing...<br>Can you please rephrase your message?"

error_text_2 = "Looks like I am having a problem"

ask_for_pickup_zipcode = "<br>To continue please enter your pickup zip code"

ask_for_delivery_zipcode = "<br>To continue please enter your delivery zip code"

ask_for_email = "<br>To continue please enter a good email address so we can send you the estimate"

ask_for_phone = "<br>To continue please enter a good phone number to reach you at"

ask_for_name = "<br>Please enter the name you want written on the estimate"

ask_for_item_list = "<br>Next please enter your item list for the move. Try to add each item in a new line.<br>You can delete your last entry by pressing 'delete'.<br>When you're finished just write 'done'."

general_prompt = "Is there anything else I can help you with?"

out_of_service_area = "I am afraid that is out of our service area."

general_task_raw_text = ' task( based on the CLIENT message complete BOT response and remember to always ask for: {{ ASK_FOR }} ) CLIENT: '

inventory_task = ' task: based on the list of cubic feet per item and the client item list complete results in the following format: {"results": [{"name": "item name", "quantity": "item quantity", "CF": "cubic feet per unit"}, {"name": "item name", "quantity": "item quantity", "CF": "cubic feet per unit"}]} results json: {"results":'

greeting_raw_text = "Hi!<br>I am {{BOT_NAME}}.<br>To get started please enter your pick up zip code or ask me a question."

conversation_starter_raw_text = 'company information( bot name: {{BOT_NAME}} | company name: {{COMPANY_NAME}} | company address: {{COMPANY_ADDRESS}} | company phone: {{COMPANY_PHONE}} | company email: {{COMPANY_EMAIL}} | years in business: {{YEARS_IN_OPERATION}} | company license: {{COMPANY_LICENSE}} | company type: {{COMPANY_TYPE}} ). example questions( '

price_reply_raw_text = '<br><br>Based on your list I estimate your move at {{ CUBIC_FT }} Cubic Feet which should take a truck and crew {{ WORKING_HOURS }}-{{ WORKING_HOURS_PLUS }} hours at ${{ PRICE_PER_HOUR }} an hour.<br>With mileage fee the estimate for your move is ${{ PRICE }}<br>'

problem_items_raw_text = "<br>I am afraid there are a few items I couldn't locate {{ problem_items }}.<br>This doesn't necessarily mean we can't take them but I will need a human colleague to review them first"

price_reply_raw_text_ld = "<br><br>Based on your list I estimate your move at {{ CUBIC_FT }} Cubic Feet Which we can do door to door to {{ DELIVERY_STATE }} for exactly ${{ PRICE }} all included.<br><br>The price is for a full service move including:<br>1.Dissasembley and reassembly of the furniture<br>2.Loading unloading and all of the labor<br>3.All of the taxes, tools, gas, labor and basic coverage are included<br>4.We will wrap all of the furniture with quilted blankets and moving pads<br>5.The estimate also includes 30 days of free optional storage<br>"
