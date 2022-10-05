# IMPORT PACKAGES
from os import environ, path
from dotenv import load_dotenv
import pandas as pd


# SET UP OPENAI KEY
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
openai_key = environ.get('SECRET_KEY')
model_name = "text-davinci-002"

# GET PRICE LIST FROM CSV
price_list = pd.read_csv('~/moverbot/price_list.csv')


# GET QUESTIONS FROM quesions.txt
que = open('~/moverbot/questions.txt')
questions = que.read()
questions += " )"
que.close()

# GET INVENTORY FROM inventory.txt
inv = open('~/moverbot/inventory.txt')
inventory_list = 'list of cubic feet per item: [{'
contents = inv.readlines()
for line in contents:
    inventory_list += line + ","
# add forbidden item types to inventory list variable with cubic ft value of '0'
inventory_list += " abstract concepts : 0, people : 0, vehicles : 0, locations : 0, animals : 0, plants : 0, guns : 0, dangerous materials : 0}] "
inv.close()


######################################################################
#                                                                    #
#                       USER SETTINGS                                #
#               edit all settings below this line                    #
#                                                                    #
######################################################################


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
gas_charge = 15 # gas charge in % added to final price
