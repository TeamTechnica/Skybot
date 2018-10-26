import pandas as pd
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	body = request.values.get('From', None)

	resp = MessagingResponse()
	
	resp.message("Welcome to Skybot")
	return str(resp)


if __name__ == "__main__":
	app.run(debug=True)
