from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random
import sqlite3
import sendgrid
import os
from sendgrid.helpers.mail import *

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

def send_verify_email(email):
	sg = sendgrid.SendGrid("SENDGRID_APIKEY") #API Key goes here
	
	from_email = Email(CUSkyBot@gmail.com)
	to_email = Email(email)
	subject = "Verfify Email with SkyBot"

	random_num = random.randint(1, 100,000,000)
	content = Content("text/plain", "Your verifcation code is " + str(random_num))
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())

	if(str(response.status_code) != 201):
		resp = MessagingResponse()
		resp.message("Please give me your email again, error in sending verfication code")
		return str(resp)
	
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
