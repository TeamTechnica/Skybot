from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random
from database import *
import sendgrid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sendgrid.helpers.mail import *

engine = create_engine('sqlite:///site.db')
Session = sessionmaker(autoflush=True, autocommit=False, bind=engine)
conn = engine.connect()
session = Session(bind=conn)

app = Flask(__name__)


def parse_flight_info(text_message):
    """ Parses incoming text for flight information """
    # new_flight = Flight()
    # session.add(new_user)
    # session.commit()
    # session.close()
    return ""


def receive_flight_info():
    """ Hanldes communication once all needed info is collected """

    # if verify state is VERIFIED
    resp = MessagingResponse()
    resp.message("""Thank you for the information!
        We'll notify you as soon as we have a match""")
    return str(resp)


def verify():
    """ Handles initial info collection for flight """

    # triggered when they send the correct verification code
    resp = MessagingResponse()
    resp.message("""Thanks for verifying! Let's get started with your
        flight information. Please answer the following, separated by commas:
        1. JFK/LGA/EWR
        2. Date (MM/DD/YYYY)
        3. Flight Time (XX:XX AM/PM)
        4. Maximum Number of Additional Passengers""")
    return str(resp)


def send_verify_email(email, phone_number):
    """ Sends user verification email

    Keyword arguments:
    email -- user's email address
    """
    sg = sendgrid.SendGridAPIClient(os.getenv('SENDGRID_TOKEN'))

    from_email = Email("CUSkyBot@gmail.com")
    to_email = Email(str(email))
    subject = "Verify Email with SkyBot"

    random_num = random.randint(1, 100000000)
    
    # commit the random number to user's data for comparison
    # session.query().filter(User.phone_number == phone_number).update({"verification_code": random_num})

    content = Content("text/plain", "Verifcation Code: " + str(random_num))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    if str(response.status_code) != 201:
        resp = MessagingResponse()
        resp.message("""Please send your email again,
            error in sending verfication code""")
        return str(resp)
    else:
        resp = MessagingResponse()
        resp.message("""Check your email for a verification email
            and text us the code""")
        # change verified state to EMAIL_SENT
        # session.query().filter(User.phone_number == pnumber).update({"verified": "EMAIL_SENT"})
        return str(resp)


def exist_user(phone_number, body):
    """ Handles communication with existing Skybot users

    Keyword arguments:
    phone_number -- user's phone number
    body -- user's text message
    """
    curr_user = session.query(User).filter_by(
        phone_number=phone_number).first()

    # if verify state is NONE, call send email function
    if curr_user.verified == 'NONE':
        message = send_verify_email(body + "@columbia.edu", phone_number)
    elif curr_user.verified == "EMAIL_SENT" and body == curr_user.verification_code:
        message = verify()
    else:
        message = verify()
    return message


def new_user(phone_number):
    """ Handles communication with new Skybot users

    Keyword arguments:
    phone_number -- user's phone number
    """

    # create & insert new user into database
    new_user = User(phone_number=phone_number, verified="NONE")
    session.add(new_user)
    session.commit()
    session.close()

    # send confirmation message & ask for UNI
    resp = MessagingResponse()
    resp.message("Welcome to Skybot! What's your UNI?")
    return str(resp)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """ Handles text communication with users """

    # gets phone number of user
    pnumber = request.values.get('From', None)

    # checks db for existing user
    check_num = session.query(User).filter(User.phone_number == pnumber)
    if session.query(check_num.exists()).scalar() is False:
        out_message = new_user(pnumber)
    else:
        body = request.values.get('Body', None)
        out_message = exist_user(pnumber, body)

    return str(out_message)


if __name__ == "__main__":
    app.run(debug=True)
