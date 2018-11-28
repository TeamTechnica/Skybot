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


def send_verify_email(uni, email):
    """ Sends user verification email

    Keyword arguments:
    email -- user's email address
    """
    user_uni = uni

    from_email = Email("CUSkyBot@gmail.com")
    to_email = Email(str(email))
    subject = "Verify Email with SkyBot"

    random_num = random.randint(100000000000, 111111111111)

    row = db.session.query(User).filter(User.uni == user_uni).first()
    row.verification_code = random_num
    db.session.commit()

    content = Content("text/plain", "Verifcation Code: " + str(random_num))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    resp = MessagingResponse()
    resp.message("""Check your email for a verification email
            and text us the code""")

    # update email verified
    row = db.session.query(User).filter(User.uni == user_uni).first()
    row.verified = "EMAIL_SENT"
    db.session.commit()

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
        message = send_verify_email(body, body + "@columbia.edu")
    elif curr_user.verified == "EMAIL_SENT" and body == curr_user.verification_code:
        # update verified state to "VERIFIED"
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
    db.session.add(new_user)
    db.session.commit()
    db.session.close()

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
    check_num = db.session.query(User).filter(User.phone_number == pnumber)
    if db.session.query(check_num.exists()).scalar() is False:
        out_message = new_user(pnumber)
    else:
        body = request.values.get('Body', None)
        out_message = exist_user(pnumber, body)

    return str(out_message)

def matchFound(cur_user, cur_fltDate, cur_fltTime, cur_airport):
    current_user = cur_user
    current_fltDate = cur_fltDate
    current_fltTime = cur_fltTime
    current_airport = cur_airport

    # Queries for the first match based on flight date, time and aiport
    matched_flight = (Flight.query.filter(Flight.flight_date == current_fltDate, Flight.departure_time == current_fltTime, Flight.airport == current_airport)).first() #getting all flights with the same departure date
    print(matched_flight)

    if matched_flight == None:
        # Adds the users flight data to the database after querying (avoids matching with itself)
        user_flight_data = Flight( airport=current_airport, flight_date=current_fltDate, departure_time=current_fltTime, passenger=current_user)
        db.session.add(user_flight_data)
        db.session.commit()

        print ("There are currently no matches, but we will keep searching!")
    else:

        user_flight_data = Flight( airport=current_airport, flight_date=current_fltDate, departure_time=current_fltTime, passenger=current_user)
        db.session.add(user_flight_data)
        db.session.commit()

        match_airport = current_airport
        match_date = current_fltDate

        # Finds the rider with the earliest departure time and subtracts two hours
        match_departTime = str ((min(int(current_fltTime), int(matched_flight.departure_time)))  - 20000 )

        # Creates new match instance 
        new_match = Match(airport = match_airport, ride_date = match_date, ride_departureTime = match_departTime)
        db.session.add(new_match)
        db.session.commit()

        # Add match to the flight 
        user_flight_data.ride = new_match
        matched_flight.ride = new_match

        # Message are sent to users 
        print ("this is the uni of your rideshare match: " )

        for riderss in new_match.riders:
            print (riderss.passenger.uni)



# comment
if __name__ == "__main__":
    app.run(debug=True)
