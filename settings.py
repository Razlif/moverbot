### IMPORT PACKAGES
from os import environ, path
from dotenv import load_dotenv

### SET UP OPENAI KEY
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
openai_key = environ.get('SECRET_KEY')
model_name = "text-davinci-002"

### GET QUESTIONS FROM quesions.txt
que = open("~/moverbot/questions.txt")
questions = que.read()
questions += ")"
que.close()

### GET INVENTORY FROM inventory.txt
inv = open('~/moverbot/inventory.txt')
inventory_list = 'list of cubic feet per item: [{'
contents = inv.readlines()
for line in contents:
    inventory_list += line + ","
inventory_list += " abstract concepts : 0, people : 0, vehicles : 0, locations : 0, animals : 0, plants : 0, guns : 0, dangerous materials : 0}] "
inv.close()

### user settings - edit all settings below this line - add your value inside the quotation marks "your value"
dispatch_zipcode = ""
company_name = ""
bot_name = ""
company_address = ""
company_phone = ""
company_email = ""
allowed_service_locations = ['CA']
mileage_fee = 1
price_per_hour = 200
years_in_operation = ""
company_license = ""
company_type = ""
minimum_hours_per_job = 3

