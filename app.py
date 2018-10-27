from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random
import sqlite3

app = Flask(__name__)
# conn = sqlite3.connect('example.db')

def receive_flight_info():
	# if verify state is VERIFIED
	resp = MessagingResponse()
	resp.message("""Thank you for the information! 
		We'll notify you as soon as we have a match""")
	return str(resp)

def verify():
	# triggered when they send the correct verification code
	resp = MessagingResponse()
	resp.message("""Thank you for verifying your identity! Let's get 
		started with your flight information. Please answer the following:
		1. JFK/LGA/EWR
		2. Date (MM/DD/YYYY)
		3. Flight Time (XX:XX AM/PM) 
		4. Maximum Number of Additional Passengers""")
	return str(resp)

def send_verify_email():
	# change verify state to email_sent 
	return "" 

def exist_user(phone_number):
	# if verify state is NONE, call send email function
	return ""

def new_user(phone_number):
	# insert into db -- verify state is set to NONE
	# conn.execute(""" INSERT INTO XXXX (phone, "NONE"")
	resp = MessagingResponse()
	resp.message("Welcome to Skybot! What's your UNI?")
	return str(resp)

def check_verification(phone_number):

	return ""

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	# gets phone number of user
	pnumber = request.values.get('From', None)
	
	# checks db for existing user
	# conn.execute(""" SELECT EXISTS( SELECT 1 FROM xxxx WHERE YYY = pnumber) """)

	# depending on result, call exist or new user function

	resp = MessagingResponse()
	
	resp.message("Welcome to Skybot")
	
	return str(resp)


if __name__ == "__main__":
	app.run(debug=True)