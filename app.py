from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random

app = Flask(__name__)


def get_flight_info():
	return "" 

def send_verify_email():
	# change verify state to email_sent 
	return "" 

def exist_user(phone_number):
	# if verify state is NONE, call send email function
	return ""

def new_user(phone_number):
	# insert into db -- verify state is set to NONE
	# CODE HERE
	resp = MessagingResponse()
	resp.message("Welcome to Skybot! What's your UNI?")
	return str(resp)

def check_verification(phone_number):

	return ""

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	# gets phone number of user
	body = request.values.get('From', None)
	
	# checks db for existing user
	# CODE HERE

	# depending on result, call exist or new user function

	resp = MessagingResponse()
	
	resp.message("Welcome to Skybot")
	
	return str(resp)


if __name__ == "__main__":
	app.run(debug=True)