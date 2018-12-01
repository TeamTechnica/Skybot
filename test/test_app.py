import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import unittest
import requests
import random
from app import *
from database import *
import xml.etree.ElementTree as ET
from twilio.rest import Client

verfi_num1 = str(random.randint(100000, 111111))
verfi_num2 = str(random.randint(100000, 111111))

phone_num1 = '+' + str(random.randint(10000000000, 11111111111))
phone_num2 = '+' + str(random.randint(10000000000, 11111111111))


class AppTests(unittest.TestCase):

    def test_new_user1(self):
        req = requests.post(
            'https://cuskybot.herokuapp.com/sms',
            data={
                'To': '+16674014282',
                'From': phone_num1, 'Body': 'Hello There!',
            },
        )
        root = ET.fromstring(str(req.text))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, "Welcome to Skybot! What's your UNI?")

    def test_new_user1(self):
        req = requests.post(
            'https://cuskybot.herokuapp.com/sms',
            data={
                'To': '+16674014282',
                'From': phone_num2, 'Body': 'Hello There!',
            },
        )
        root = ET.fromstring(str(req.text))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, "Welcome to Skybot! What's your UNI?")

    def test_user1_wrong_uni(self):
        req = requests.post(
            'https://cuskybot.herokuapp.com/sms',
            data={
                'To': '+16674014282',
                'From': phone_num1, 'Body': 'mj345',
            },
        )

        root = ET.fromstring(str(req.text))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Error: Invalid uni!""")

        # send correct uni now
        req = requests.post(
            'https://cuskybot.herokuapp.com/sms',
            data={
                'To': '+16674014282',
                'From': phone_num1, 'Body': 'mj3456',
            },
        )

        root = ET.fromstring(str(req.text))
        for child in root:
            message = child.text
            break

        self.assertEqual(
            message, """Check your email for a verification email
            and text us the code""",
        )

    def test_new_user1(self):
        req = requests.post(
            'https://cuskybot.herokuapp.com/sms',
            data={
                'To': '+16674014282',
                'From': phone_num2, 'Body': 'mj6789',
            },
        )
        root = ET.fromstring(str(req.text))
        for child in root:
            message = child.text
            break

        self.assertEqual(
            message, """Check your email for a verification email
            and text us the code""",
        )

    '''
    def test_uni_login(self):
        req = requests.post('https://cuskybot.herokuapp.com/sms',
                            data = {'To': '+16674014282',
                            'From': rand_num, 'Body': 'mj2729'})
        root = ET.fromstring(str(req.text))
        for child in root;
            message = child.text
            break

        self.assertEqual(message, "Check your email for a verification email
            and text us the code")

    def test_verfication(self)
        user = session.query(Users).filter(User.uni == mj2729).first()
        user_verification = user.verification_code

        req = requests.post('https://cuskybot.herokuapp.com/sms',
                            data = {'To': '+16674014282',
                            'From': rand_num, 'Body': user_verification})

        root = ET.fromstring(str(req.text))
        for child in root;
            message = child.text
            break

        self.assertEqual(message, str(Thanks for verifying! Let's start
        flight information. Please answer the following, separated by commas:
        1. JFK/LGA/EWR
        2. Date (MM/DD/YYYY)
        3. Flight Time (XX:XX AM/PM)
        4. Maximum Number of Additional Passengers))
    '''

    user1 = User.query.filter_by(phone_number=phone_num1).first()
    if user1 is not None:
        db.session.delete(user1)
        db.session.commit()

    user2 = User.query.filter_by(phone_number=phone_num2).first()
    if user1 is not None:
        db.session.delete(user1)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
