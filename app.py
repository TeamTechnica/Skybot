from flask import Flask, request
from pymessenger.bot import Bot
import os

#ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
#VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

app = Flask(__name__)
bot = Bot (ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token", '')
		return verify_fb_token(token_sent)
	else:
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					recipient_id = message['sender']['id']
					if message['message'].get('text'):
						response_sent_text = get_message()
						send_message(recipient_id, response_sent_text)
					if message['message'].get('attachments'):
						response_sent_nontext = get_message()
						send_message(recipient_id, response_sent_nontext)
		return "Message Processed"


def verify_fb_token(token_sent):
	 """ token_sent: sent by facebook 
	 description: 
	 	verifies if it matches the verify token, or returns error """
	 if token_sent == VERIFY_TOKEN:
	 	return request.args.get("hub.challenge")
	 return 'Invalid verification token:' + str(token_sent) + str(VERIFY_TOKEN)

def get_message():
	sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
	return random.choice(sample_responses)

def send_message(recipient_id, response):
	bot.send_text_message(recipient_id, response)
	return "success"

if __name__ == '__main__':
	app.run()