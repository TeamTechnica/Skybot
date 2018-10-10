from flask import Flask, request
from pymessenger.bot import Bot
import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")


def verify_fb_token(token_sent):
    """ token_sent: sent by facebook 
    	description: 
    	verifies if it matches the verify token, or returns error """
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


if __name__ == '__main__':
	app.run()