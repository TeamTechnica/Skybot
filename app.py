import os
import random

import sendgrid
from flask import Flask
from flask import redirect
from flask import request
from sendgrid.helpers.mail import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.twiml.messaging_response import MessagingResponse

from databaseChanges import *

engine = create_engine('sqlite:///site.db')
Session = sessionmaker(autoflush=True, autocommit=False, bind=engine)
conn = engine.connect()
session = Session(bind=conn)


def parse_flight_info(text_message):
    """ Parses incoming text for flight information """
    # new_flight = Flight()
    # db.session.add(new_user)
    # db.session.commit()
    # db.session.close()
    return ""


def receive_flight_info():
    """ Hanldes communication once all needed info is collected """

    # if verify state is VERIFIED
    resp = MessagingResponse()
    resp.message("""Thank you for the information!
        We'll notify you as soon as we have a match""")
    return str(resp)


def verify(pnumber):
    """ Handles initial info collection for flight """

    # triggered when they send the correct verification code
    resp = MessagingResponse()

    row = db.session.query(User).filter(User.phone_number == pnumber).first()

    if str(row.verified) == "VERIFIED":
        resp.message("""Thanks for verifying! Let's get started with your
        flight information. Please enter the Airport
        JFK/LGA/EQR""")

        row.verified = "AIRPORT_INFO"
        db.session.commit()
    elif str(row.verified) == "AIRPORT_INFO":
        resp.message("""Please enter Date of Flight Departure in following format
            MM/DD/YYYY""")

        row.verified = "DATE_INFO"
        db.session.commit()
    elif str(row.verified) == "DATE_INFO":
        resp.message("""Please enter flight time in following format
            (XX:XX AM/PM)""")

        row.verified = "FLIGHT_TIME"
        db.session.commit()
    elif str(row.verified) == "FLIGHT_TIME":
        resp.message("""Last thing, please enter the max number of passengers you're willing
            to ride with as a number. Ex. 2""")

        row.verified = "FINISHED"
        db.session.commit()
    elif str(row.verified) == "FINISHED":
        resp.message(
            """Thanks! Give me a moment while I find some matches !""",
        )

    return str(resp)


def send_verify_email(uni, email, pnumber):
    """ Sends user verification email

    Keyword arguments:
    email -- user's email address
    """

    sg = sendgrid.SendGridAPIClient(os.getenv('SENDGRID_TOKEN'))

    user_uni = uni

    from_email = Email("CUSkyBot@gmail.com")
    to_email = Email(str(email))
    subject = "Verify Email with SkyBot"

    random_num = random.randint(100000000000, 111111111111)

    row = db.session.query(User).filter(User.phone_number == pnumber).first()
    row.verification_code = random_num
    row.uni = user_uni
    db.session.commit()

    content = Content("text/plain", "Verifcation Code: " + str(random_num))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    resp = MessagingResponse()
    resp.message("""Check your email for a verification email
            and text us the code""")

    # update email verified
    row.verified = "EMAIL_SENT"
    db.session.commit()

    return str(resp)


def reverfiy_uni():
    """
    Handles the case when wrong verification_code given
    """
    resp = MessagingResponse()
    resp.message("""Sorry the verification_code does not match.
        Please enter your uni again""")
    return str(resp)


def error():
    """
    Error Handler
    """

    resp = MessagingResponse()
    resp.message("""Sorry an error has occured, please try again later
        """)
    return str(resp)


def exist_user(phone_number, body):
    """ Handles communication with existing Skybot users

    Keyword arguments:
    phone_number -- user's phone number
    body -- user's text message
    """
    curr_user = db.session.query(User).filter_by(
        phone_number=phone_number,
    ).first()

    # if verify state is NONE, call send email function
    if curr_user.verified == 'NONE':
        message = send_verify_email(body, body + "@columbia.edu", phone_number)
    elif curr_user.verified == "EMAIL_SENT" and int(body) == curr_user.verification_code:
        # update verified state to "VERIFIED"
        curr_user.verified = "VERIFIED"
        db.session.commit()

        message = verify(phone_number)
    elif curr_user.verified == "EMAIL_SENT" and int(body) != curr_user.verification_code:
        # update verified so new email is sent
        curr_user.verified = "NONE"
        db.session.commit()

        message = reverfiy_uni()
    elif str(curr_user.verified) in ["VERIFIED", "AIRPORT_INFO", "FLIGHT_TIME", "DATE_INFO", "FINISHED"]:
        message = verify(phone_number)
    else:
        message = error()
    return message


def new_user(phone_number):
    """ Handles communication with new Skybot users

    Keyword arguments:
    phone_number -- user's phone number
    """

    # create & insert new user into database
    new_user = User(
        phone_number=phone_number,
        verified="NONE", verification_code=0,
    )
    db.session.add(new_user)
    db.session.commit()

    # send confirmation message & ask for UNI
    resp = MessagingResponse()
    resp.message("Welcome to Skybot! What's your UNI?")
    return str(resp)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """ Handles text communication with users """

    # gets phone number of user
    pnumber = request.values.get('From', None)

    #result = db.session.query(User.verification_code).all()
    # print("*********************")
    # print(result)
    # print("*********************")

    #result = db.session.query(User.uni).all()
    # print("*********************")
    # print(result)
    # print("*********************")

    # checks db for existing user
    check_num = db.session.query(User).filter(User.phone_number == pnumber)
    if db.session.query(check_num.exists()).scalar() is False:
        out_message = new_user(pnumber)
    else:
        body = request.values.get('Body', None)
        out_message = exist_user(pnumber, body)

    return str(out_message)


# comment
if __name__ == "__main__":
    app.run(debug=True)
