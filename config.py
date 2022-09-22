### FLASK CONFIG - DO NOT ALTER THIS PAGE

### IMPORT PACKAGES
from os import environ, path
from dotenv import load_dotenv
import settings
import jinja2

### SET UP OPENAI KEY
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
OPENAI_KEY = environ.get('SECRET_KEY')

### SET UP JINJA ENVIROMENT
environment = jinja2.Environment()

### GENERAL FLASK SETTINGS
TESTING = True
DEBUG = True
FLASK_ENV = 'development'
secret_key = "SecretsOfMoverBot"

### GET QUESTIONS FROM quesions.txt
with open('questions.txt') as que:
    QUESTIONS = que.read()

### GET INVENTORY FROM inventory.txt
with open('inventory.txt') as inv:
    INVENTORY = '{"results": [{'
    contents = inv.readlines()
    for line in contents:
        INVENTORY += line + ","
    INVENTORY += "}]}"

### GET COMPANY SETTINGS FROM settings.py
COMPANY_NAME = settings.COMPANY_NAME

BOT_NAME = settings.BOT_NAME

COMPANY_ADDRESS = settings.COMPANY_ADDRESS

COMPANY_PHONE = settings.COMPANY_PHONE

COMPANY_EMAIL = settings.COMPANY_EMAIL

ALLOWED_PICKUP_LOCATIONS = settings.ALLOWED_PICKUP_LOCATIONS

ALLOWED_DELIVERY_LOCATIONS = settings.ALLOWED_DELIVERY_LOCATIONS

MILEAGE_FEE = settings.MILEAGE_FEE

MINIMUM_CF_PER_JOB = settings.MINIMUM_CF_PER_JOB

PRICE_PER_HOUR = settings.PRICE_PER_HOUR

YEARS_IN_OPERATION = settings.YEARS_IN_OPERATION

COMPANY_LICENSE = settings.COMPANY_LICENSE

DELIVERY_TIME_FRAME = settings.DELIVERY_TIME_FRAME

COMPANY_TYPE = settings.COMPANY_TYPE

### SET UP ADDITIONAL VARIABLES
ERROR_TEXT = "This is emberassing...looks like I'm stuck. Can you please rephrase your message?"

GENERAL_TASK = 'Complete BOT response:'

INVENTORY_TASK = 'based on the inventory and the client item list return results in the following format: {"results": [{"name": "item_name", "quantity": "item_quantity", "CF": "cubic_ft"}, {"name": "item_name", "quantity": "item_quantity", "CF": "cubic_ft"}]}'

PROMPT_AFTER_QUESTIONS="CLIENT: What now? BOT: Now in order to get a moving estimate please enter your pick up zip code. CLIENT:"

GREETING_TEMPLATE = environment.from_string('Hi!<br>I am {BOT_NAME}.<br>To get started please enter your pick up zip code or ask me a question.')

GREETING = GREETING_TEMPLATE.render(BOT_NAME=BOT_NAME)

CONV_START_TEMPLATE = environment.from_string("BOT: Hi! I am {{BOT_NAME}}. How can I help you today? CLIENT: I need a movers. BOT: Great, we will be more than happy to help. Please provide me with your pick up zip code to get started. CLIENT: Where are you located? BOT: We are located in {{COMPANY_ADDRESS}}. CLIENT: What is your contact information. BOT: We are always available at {{COMPANY_PHONE}} and {{COMPANY_EMAIL}}. CLIENT: How long have you beed in buisness? BOT: We have been in buisness for {{YEARS_IN_OPERATION}} years. CLIENT: Are you a carrier or a broker? BOT: We are a licensed and insured {{COMPANY_TYPE}}. Our license number is {{COMPANY_LICENSE}} CLIENT: How long does it to take to move? BOT: Our delivery time frame is {{DELIVERY_TIME_FRAME}}")

CONV_START = CONV_START_TEMPLATE.render(BOT_NAME=BOT_NAME, COMPANY_ADDRESS=COMPANY_ADDRESS, COMPANY_EMAIL=COMPANY_EMAIL, COMPANY_PHONE=COMPANY_PHONE, COMPANY_TYPE=COMPANY_TYPE, COMPANY_LICENSE=COMPANY_LICENSE, YEARS_IN_OPERATION=YEARS_IN_OPERATION, DELIVERY_TIME_FRAME=DELIVERY_TIME_FRAME)