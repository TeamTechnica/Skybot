import unittest
import requests
import random
import xml.etree.ElementTree as ET
from twilio.rest import Client


class AppTests(unittest.TestCase):
	def test_new_user(self):            
		req = requests.post('https://cuskybot.herokuapp.com/sms', data = {'To': '+16674014282', 'From': '+13476537652', 'Body': 'me'})
		root = ET.fromstring(str(req.text))
		for child in root:
			message = child.text
			break
		
		self.assertEqual(message, "Welcome to Skybot! What's your UNI?")


if __name__ == '__main__':
	unittest.main()

