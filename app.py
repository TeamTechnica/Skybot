from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random
from database import * 
import sendgrid

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
	# change verify state to email_sent 
	client = sendgrid.SendGridClient("SENDGRID_APIKEY") #how to generate key?
	message = sendgrid.Mail()

	message.add_to(email)
	message.sent_from("skybot@gmail.com") #neeed to make an email for skybot
	message.set_subject("Verify with Skybot")
	message.set_html("Hi please verfiy you email!") #need to send code

	client.send(message)
	return "" 

def exist_user(phone_number):
	# if verify state is NONE, call send email function
	return ""

def new_user(phone_number):
	# create & insert new user into database
	new_user = User(phone_number=pnumber)
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
	check_num = db.session.query(User).filter(User.phone_number == pnumber)

	if db.session.query(q.exists()).scalar() == 1:
		exist_user(pnumber)
	else:
		new_user(pnumber)

	resp = MessagingResponse()
	resp.message("Welcome to Skybot")
	
	return str(resp)


if __name__ == "__main__":
	app.run(debug=True)