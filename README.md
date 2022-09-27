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
pip3 install --user -r requirements.txt
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

For the bot to run properly you will need to update 3 project files.

1. Update the company information on the settings.py file

> update only the user settings section

user settings:
```
dispatch_zipcode = "90210" # used to calculate mileage fee
company_name = "your company name"
bot_name = "the bot name"
company_address = "your company address"
company_phone = "your company phone"
company_email = "your company email"
allowed_service_locations = ['CA', 'TX', ...] # you can enter states or zip codes seperated by a comma
mileage_fee = 1 # setting for $ per mile on mileage fee calculation
price_per_hour = 200 # company price per working hour
years_in_operation = "15"
company_license = "your license"
company_type = "carrier/broker/other"
minimum_hours_per_job = 3
```
2. Update the questions.txt file

> This will be a referance for the bot - you can add and remove questions as needed.

questions.txt
```
CLIENT: What is he price for? how much will it cost?
BOT: all local movers are required to charge by the hour. we charge $__ per hour for the truck and crew with a minimum of __ hours per job.
CLIENT: do you offer insurance for my items?
BOT:
CLIENT:
BOT:
CLIENT:
BOT:
CLIENT:
BOT:
```

3. Update the cubic feet for the items in the inventory.txt file

> You can add or remove items as needed

inventory.text
```
king bed : 10
queen bed : 10
single bed : 10
night stand : 10
dresser : 10
large mirror : 10
chest : 10
tv : 10
```

# The conversation flow

The bot is designed to work in conversation stages:
1. Get and validate the client's pick up zip code
2. Get and validate the client's delivery zip code
3. collect the client's item list
4. calculate and present client with the price.
5. collect client info: email, name, phone.
6. answer any additional questions

# Running the chatbot

Once all of the files are updated with the necessary information.
Run the flask app on your local machine and start fine tuning the bot by altering the questions.txt and inventoy.txt as needed.

Once all of the files are updated with the necessary information.
Run the flask app on your local machine and start fine tuning the bot by altering the questions.txt and inventoy.txt as needed.

# Notes

The bot has the power of an openai model behind it so it is quite intelegant.
But some fine tuning is likely to be required.
This might mean editing the quesions.txt file or the inventory.txt file until you get the exactly what you want.

You can however get much better results by training the openai model, this is done one time and after that the questions.txt file will no longer be necessary.
You can train your model on an infinite number of complex questions quickly and easily.
Go here to read more about [training your openai model](https://beta.openai.com/docs/guides/fine-tuning)
>Once your model is trained update the "model name" in the settings.py file and remove the questions.txt file from the prompt variable in the functions.py file.

# Have Fun!