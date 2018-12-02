import os
import random
import sys
import unittest
import xml.etree.ElementTree as ET

import requests
from twilio.rest import Client

from app import *
from database import *

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

verfi_num1 = str(random.randint(100000, 111111))
verfi_num2 = str(random.randint(100000, 111111))

phone_num1 = '+' + str(random.randint(10000000000, 11111111111))
phone_num2 = '+' + str(random.randint(10000000000, 11111111111))


class Test(unittest.TestCase):
    def test_new_user1(self):
        self.test_app = app.test_client()

        response = self.test_app.post(
            '/sms', data={
                'To': '+16674014282',
                'From': phone_num1, 'Body': 'Hello There!',
            },
        )

        root = ET.fromstring(str(response.data))
        for child in root:
            message = child.text
            break

        self.assertEqual(message, "Welcome to Skybot! What's your UNI?")

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
