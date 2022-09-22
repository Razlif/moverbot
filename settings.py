### IMPORT PACKAGES
from os import environ, path
from dotenv import load_dotenv

### SET UP OPENAI KEY
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
#openai_key = environ.get('SECRET_KEY')
model_name = "text-davinci-002"
openai_key = "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"

### GET QUESTIONS FROM quesions.txt
que = open("/home/jujiberry/moverbot/questions.txt")
questions = que.read()
questions += ")"
que.close()

### GET INVENTORY FROM inventory.txt
inv = open('/home/jujiberry/moverbot/inventory.txt')
inventory_list = 'list of cubic feet per item: [{'
contents = inv.readlines()
for line in contents:
    inventory_list += line + ","
inventory_list += " abstract concepts : 0, people : 0, vehicles : 0, locations : 0, animals : 0, plants : 0, guns : 0, dangerous materials : 0}] "
inv.close()

#### user settings - edit all settings below this line - add your value inside the quotation marks "your value"
dispatch_zipcode = "60109"
company_name = "MOVERS INC"
bot_name = "Moverbot"
company_address = "111 somewhere st"
company_phone = "(999)999-9999"
company_email = "sales@moversinc.com"
allowed_service_locations = ['IL', 'NY', 'TX', 'CA']
mileage_fee = 2
minimum_cf_per_job = 300
price_per_hour = 250
years_in_operation = "15"
company_license = "us dot - 9999999"
company_type = "local moving carrier"
minimum_hours_per_job = 3

