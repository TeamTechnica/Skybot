from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random
from database import * 
import sendgrid

import os
from sendgrid.helpers.mail import *

app = Flask(__name__)
db.create_all()

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

	sg = sendgrid.SendGrid("SENDGRID_APIKEY") 
	
	from_email = Email(CUSkyBot@gmail.com)
	to_email = Email(email)
	subject = "Verfify Email with SkyBot"

	random_num = random.randint(1, 100,000,000)
	content = Content("text/plain", "Your verifcation code is " + str(random_num))
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())

	if str(response.status_code) != 201:
		resp = MessagingResponse()
		resp.message("Please give me your email again, error in sending verfication code")
		return str(resp)

	return "" 

def exist_user(phone_number, uni):
	curr_user = db.session.query(User).filter_by(phone_number=phone_number).first()
	
	# if verify state is NONE, call send email function
	if curr_user.verified == 'NONE':
		send_verify_email(uni + "columbia.edu")
	return ""

def new_user(phone_number):
	# create & insert new user into database
	new_user = User(phone_number=phone_number)
	db.session.add(new_user)

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
	check_num = User.query.filter_by(phone_number='4106248627')
	"""
	if db.session.query(q.exists()).scalar() == 1:
		exist_user(pnumber)
	else:
		uni = request.values.get('Body', None)
		new_user(pnumber, uni)
	"""
	resp = MessagingResponse()
	resp.message("We queried the database")
	return str(resp)


if __name__ == "__main__":
	app.run(debug=True)
