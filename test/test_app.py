import unittest
import requests
import random
import app
import xml.etree.ElementTree as ET
from twilio.rest import Client



class AppTests(unittest.TestCase):

	rand_num = str(random.randint(100000000000, 111111111111))

	def test_new_user(self):           
		req = requests.post('https://cuskybot.herokuapp.com/sms', data = {'To': '+16674014282', 'From': rand_num, 'Body': 'me'})
		root = ET.fromstring(str(req.text))
		for child in root:
			message = child.text
			break
		
		self.assertEqual(message, "Welcome to Skybot! What's your UNI?")

	'''
	def test_uni_login(self):
		req = requests.post('https://cuskybot.herokuapp.com/sms', data = {'To': '+16674014282', 'From': rand_num, 'Body': 'mj2729'})
		root = ET.fromstring(str(req.text))
		for child in root;
			message = child.text
			break

		self.assertEqual(message, "Check your email for a verification email
            and text us the code")

	def test_verfication(self)
		user = session.query(Users).filter(User.uni == mj2729).first()
		user_verification = user.verification_code
		
		req = requests.post('https://cuskybot.herokuapp.com/sms', data = {'To': '+16674014282', 'From': rand_num, 'Body': user_verification})
		
		root = ET.fromstring(str(req.text))
		for child in root;
			message = child.text
			break

		self.assertEqual(message, str(Thanks for verifying! Let's get started with your
        flight information. Please answer the following, separated by commas:
        1. JFK/LGA/EWR
        2. Date (MM/DD/YYYY)
        3. Flight Time (XX:XX AM/PM)
        4. Maximum Number of Additional Passengers))
	'''



if __name__ == '__main__':
	unittest.main()

