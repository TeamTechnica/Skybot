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

if __name__ == '__main__':
	app.run()