from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


def exist_user(phone_number):
	# DB call here
	return ""

def new_user(phone_number):
	# insert into db 
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