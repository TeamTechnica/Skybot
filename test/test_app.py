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

if message != "Welcome to Skybot! What's your UNI?":
    raise ValueError('Unexpected Behavior. Bot give no intro')


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

if message != "Welcome to Skybot! What's your UNI?":
    raise ValueError('Unexpected Behavior. Bot give no intro')


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

if message != "Error: Invalid uni!":
    raise ValueError(
        'Unexpected Behavior. Bot does not check for invalid unis',
    )

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

if message != """Check your email for a verification email
    and text us the code""":
    print(message)
    raise ValueError(
        'Unexpected Behavior. Bot does not check for email verification',
    )


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

if message != """Check your email for a verification email
    and text us the code""":
    raise ValueError(
        'Unexpected Behavior. Bot does not check for email verification',
    )

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
