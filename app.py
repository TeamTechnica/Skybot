from flask import Flask, request
from pymessenger.bot import Bot
import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
	return "Hello World"

if __name__ == '__main__':
	app.run()
