# Introduction

This project is intended to create a simple chatbot app for a moving company using an untrained openai model.

The bot is designed to understand and answer questions in natural language, collect user information and calculate the price based on working hours.

* To run the bot you will need to have an openai account and your openai api key.


# Installation

First clone the project
```
git clone https://github.com/Razlif/moverbot.git
```
Next install the required packages
```
pip install --user -r requirements.txt
```

# Openai Credentials

To use the program you will need your openai api key.

To get it, follow these steps:

Go to [openai](https://beta.openai.com/)

1. On the top right corner click on "settings"
2. In the drop down click on "view API keys"
3. Click on "create new secret key"
4. Copy and then paste the api key into the .env file in the project folder and save

.env:
```
SECRET_KEY = "Your openai api key"
```

# Updating the company information and settings

For the bot to run properly you will need to update 4 project files.

1. Update the company information on the settings.py file

>update only the user settings section

settings.py:
```
dispatch_zipcode = "10001"  # dispatch zip code for milage fee calculation
company_name = "Example Movers Inc"
bot_name = "Moverbot"
company_address = "1 West Street, NY, NY 10001"
company_phone = "(999) 999-9999"
company_email = "sales@examplemovers.com"
allowed_pickup_locations = ['NY', '10001'] # add states or zip codes
allowed_delivery_locations = ['NY', '10001'] # add states or zip codes
mileage_fee = 1  # price per mile for mileage fee calculation
minimum_cf_per_job = 300
price_per_hour = 200
years_in_operation = "3"
company_license = "license #999999"
company_type = "company type"
minimum_hours_per_job = 3
discount = 5 # discount in % added to final price
gas_charge = 15 # gas charge in % added to final price for long distance moves
```

2. Update the questions.txt file

>This will be a reference for the bot - you can add and remove questions as needed

questions.txt
```
CLIENT: Hi
BOT: Hi! Can I help you get a movng estimate from Example Movers Inc?
CLIENT: Do you offer insurance for my items?
BOT: yes we provide basic coverage at the amount $0.6 per lbs for all of your items already included in the estimate.
CLIENT: what items can you move?
BOT: all household items including pianos and anything that will fit in a moving truck.
CLIENT: what items can't you move?
BOT: Example Movers can not move animals, live plants, people, dangerous materials, guns etc.
...
```

3. Update the cubic feet for the items in the inventory.txt file

>You can add or remove items as needed

inventory.text
```
mattress:45
king bed:90
queen bed:75
full bed:60
...
```
4. Update your price sheet in the price_list.csv

>IMPROTANT
Your price_list.csv file must appear in the following format:

1. The A1 cell should be empty
2. All of the states should appear on the A column staring at A2
3. All of the cubic ft headrs should appear on the first line starting at B2
4. The cubic ft headrs should start with your mimum CF per job and increase by 100 CF each for each column

A price_list.csv example file is included in the project folder.
![price list](~/moverbot/static/pricelist.JPG)


# Price calculation

The price for local moves is based on hourly work.
The calculation is:
```
local move price = ((working hours x price per hour ) + mileage fee) x discount
```

The price for long distance moves is based on Cubic Feet.
```
long distance move price = Cubic Feet x rate per CF x gas charge x discount
```

# The conversation flow

The bot is designed to work in conversation stages:
1. Get and validate the client's pick up zip code
2. Get and validate the client's delivery zip code
3. collect the client's item list
4. calculate and present the client with the price.
5. collect client info: email, name, phone.
6. answer any additional questions

# Running the chatbot

Once all of the files are updated with the necessary information.
Run the flask app on your local machine and start fine tuning the bot by altering the questions.txt and inventory.txt as needed.
When you are ready, update the HTML + CSS with your design and deploy your app to the web.

# Train your openai model

The bot has the power of an openai model behind it so it is quite intelligent.
But some fine tuning is likely to be required.
This might mean editing the quesions.txt file or the inventory.txt file until you get exactly what you want.

You can however get much better results by training the openai model, this is done one time and after that the questions.txt file will no longer be necessary.
You can train your model on an infinite number of complex questions quickly and easily.
Go here to read more about [training your openai model](https://beta.openai.com/docs/guides/fine-tuning)
>Once your model is trained, update the "model name" in the settings.py file and remove the questions.txt file from the prompt variable in the functions.py file.

# Have Fun!