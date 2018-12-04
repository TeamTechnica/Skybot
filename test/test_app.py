import os
import random
import sys
import unittest
import xml.etree.ElementTree as ET

import requests
from twilio.rest import Client

from app import *

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

verfi_num1 = str(random.randint(100000, 111111))
verfi_num2 = str(random.randint(100000, 111111))

phone_num1 = '+' + str(random.randint(10000000000, 11111111111))
phone_num2 = '+' + str(random.randint(10000000000, 11111111111))


class Test(unittest.TestCase):
    '''
    def test_new_user1(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
            '/sms', data={
                'From': phone_num1, 'Body': 'Hello There!',
            },
        )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, "Welcome to Skybot! What's your UNI?")

    def test_new_user2(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
            '/sms', data={
                'From': phone_num2, 'Body': 'Hello There!',
            },
        )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, "Welcome to Skybot! What's your UNI?")

    def test_wrong_uni_user2(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
            '/sms', data={
                'From': phone_num2, 'Body': 'mj33',
            },
        )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, "Error: Invalid uni!")

        response = self.test_app.post(
            '/sms', data={
                'From': phone_num2, 'Body': 'mj2222',
            },
        )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(
            message, """Check your email for a verification email
            and text us the code""",
        )

    def test_input_uni(self):
        self.test_app = app.test_client()

        response = self.test_app.post('/sms', data={ 'From': phone_num1, 'Body': 'mj1111',},)

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Check your email for a verification email
        and text us the code""")

    def test_wrong_verif_code_user2(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
                '/sms', data={
                    'From': phone_num2, 'Body': '234',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Sorry the verification_code does not match.
        Please enter your uni again""")

        user2_code = User.query.filter_by(phone_number=phone_num2).first()

        response = self.test_app.post(
                '/sms', data={
                    'From': phone_num2, 'Body': str(user2_code.verification_code),
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Thanks for verifying! Let's get started with your
        flight information. Please enter the Airport (1)JFK (2)LGA (3)EQR""")

    def test_correct_verif_code_user1(self):
        self.test_app = app.test_client()

        user1_code = User.query.filter_by(phone_number=phone_num1).first()

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num1,
                'Body': str(user1_code.verification_code),
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Thanks for verifying! Let's get started with your
        flight information. Please enter the Airport (1)JFK (2)LGA (3)EQR""")

    def test_incorrect_airport_user2(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num2,
                'Body': '6',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Incorrect Format. Please enter 1 for JFK, 2 for
                LGA or 3 for EWR""")

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num2,
                'Body': '1',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Please enter Date of Flight Departure in
                following format MM-DD-YYYY""")


    def test_correct_airport_user1(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num1,
                'Body': '1',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Please enter Date of Flight Departure in
                following format MM-DD-YYYY""")

    def test_incorrect_date_user2(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num2,
                'Body': '07',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Incorrect Format. Please enter in following format
                MM-DD-YYYY""")

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num2,
                'Body': '12-30-2018',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Please enter flight time in following Military
        time format HHMMSS""")

    def test_correct_date_user1(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num1,
                'Body': '12-30-2018',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Please enter flight time in following Military
        time format HHMMSS""")

    def test_incorrect_pass_user2(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num2,
                'Body': 'la',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, """Incorrect Format. Please enter in milliary format HHMMSS""")

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num2,
                'Body': '103000',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        #what should this message be?
        self.assertEqual(message, """""")

    def test_correct_pass_user1(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
                '/sms', data={
                'From': phone_num1,
                'Body': '103000',
                },
            )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        #what should this message be?
        self.assertEqual(message, """""")


    def remove_users(self):
        self.test_app = app.test_client()

        user1 = User.query.filter_by(phone_number=phone_num1).first()
        if user1 is not None:
            db.session.delete(user1)
            db.session.commit()

        user2 = User.query.filter_by(phone_number=phone_num2).first()
        if user1 is not None:
            db.session.delete(user1)
            db.session.commit()
    '''


if __name__ == '__main__':
    unittest.main()
