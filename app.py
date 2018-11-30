import datetime
import os
import random
import re

import sendgrid
from flask import Flask
from flask import redirect
from flask import request
from sendgrid.helpers.mail import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.twiml.messaging_response import MessagingResponse

from database import *

engine = create_engine('sqlite:///site.db')
Session = sessionmaker(autoflush=True, autocommit=False, bind=engine)
conn = engine.connect()
session = Session(bind=conn)

# variables for matching
cur_fltDate = None
cur_fltTime = None
cur_airport = None

# variable for uni integrity checking
uni_entered = False

airports = ["JFK", "LGA", "EWR"]


def send_matches(match_list):
    """Handles returning matching unis to user

    Returns: TwiML to send to user
    """
    resp = MessagingResponse()
    unis = ""

    if len(match_list) == 0:
        resp.message("""Sorry I was not able to find any matches.
            I will keep looking though!""")
    else:
        for uni in match_list:
            unis = unis + uni + " "
        reply = "Your matches are" + unis + ". Have a great day!"
        resp.message(reply)

    return resp


def parse_date(date_entry):
    """
    Handles checking valid date entry

    Returns: Boolean if valid and date string for matching
    if valid
    """
    valid = True
    cur_date = datetime.datetime.now()
    flt_date = str(date_entry)

    if re.match(r"[0-9]*-[0-9]*-[0-9]*", flt_date) != None:
        date_str = flt_date.replace('-', '')
    else:
        valid = False
        return valid, ""

    entry_date = datetime.datetime(
        int(date_str[4:8]), int(date_str[0:2]), int(date_str[2:4]),
    )
    if (
        len(date_str) > 8 or len(date_str) < 1 or int(date_str[0:2]) < 0 or int(date_str[0:2]) > 12 or
        int(date_str[2:4]) < 1 or int(
            date_str[2:4],
        ) > 31 or entry_date < cur_date
    ):
        valid = False
        return valid, ""
    else:
        return valid, date_str


def parse_time(body):
    """
    Handles checking valid date entry

    Returns: Boolean if valid and date string for matching
    if valid
    """
    valid = True
    time_ent = body
    if (
        len(time_ent) < 6 or len(time_ent) > 6 or int(time_ent[0:2]) > 24 or int(time_ent[0:2]) < 1 or
        int(time_ent[2:4]) < 1 or int(time_ent[2:4]) > 60 or int(
            time_ent[4:6],
        ) < 1 or int(time_ent[4:6]) > 60
    ):
        valid = False
        return valid, ""
    else:
        return valid, time_ent


def parse_max(body):
    """
    Handles checking valid time entry

    Returns: Boolean if valid and time string for matching
    if valid
    """
    valid = True
    max_entry = body

    if int(max_entry) > 2 or int(max_entry) < 1:
        valid = False
        return valid, ""
    else:
        return valid, max_entry


def verify(pnumber, body):
    """ Handles initial info collection for flight

    Returns: TwiML to send to user
    """
    global cur_fltDate, cur_fltTime, cur_airport, airports
    # triggered when they send the correct verification code
    resp = MessagingResponse()

    row = db.session.query(User).filter(User.phone_number == pnumber).first()

    if str(row.verified) == "VERIFIED":
        resp.message("""Thanks for verifying! Let's get started with your
        flight information. Please enter the Airport
        (1)JFK (2)LGA (3)EQR""")

        row.verified = "AIRPORT_INFO"
        db.session.commit()
    elif str(row.verified) == "AIRPORT_INFO":
        if int(body) < 1 or int(body) > 3:
            resp.message("""Incorrect Format. Please enter 1 for JFK, 2 for
                LGA or 3 for EWR""")
        else:
            resp.message("""Please enter Date of Flight Departure in following format
                MM-DD-YYYY""")
            cur_airport = str(airports[int(body) - 1])
            row.verified = "DATE_INFO"
            db.session.commit()
    elif str(row.verified) == "DATE_INFO":
        valid, str_date = parse_date(body)
        if valid == True:
            cur_fltDate = int(str_date)
            resp.message("""Please enter flight time in following Military time format
                HHMMSS""")
            row.verified = "FLIGHT_TIME"
            db.session.commit()
        else:
            resp.message("""Incorrect Format. Please enter in following format
                MM-DD-YYYY""")
    elif str(row.verified) == "FLIGHT_TIME":
        valid, str_time = parse_time(body)
        if valid == True:
            resp.message("""Last thing, please enter the max number of passengers you're willing
            to ride with as a number. Ex. 2""")

            cur_fltTime = int(str_time)
            row.verified = "FINISHED"
            db.session.commit()
        else:
            resp.message(
                """Incorrect Format. Please enter in milliary format HHMMSS""",
            )
    elif str(row.verified) == "FINISHED":
        valid, str_max = parse_max(body)
        if valid == True:
            matches = matchFound(row, cur_fltDate, cur_fltTime, cur_airport)
            resp = send_matches(matches)
        else:
            resp.message(
                """Error, you can only enter between 1-2 passengers""",
            )

    return str(resp)


def send_verify_email(uni, email, pnumber):
    """ Sends user verification email

    Keyword arguments:
    email -- user's email address

    Returns: TwiML to send to user
    """

    sg = sendgrid.SendGridAPIClient(os.getenv('SENDGRID_TOKEN'))

    user_uni = uni

    from_email = Email("CUSkyBot@gmail.com")
    to_email = Email(str(email))
    subject = "Verify Email with SkyBot"

    random_num = random.randint(100000, 111111)

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

    Returns: TwiML to send to user
    """
    resp = MessagingResponse()
    resp.message("""Sorry the verification_code does not match.
        Please enter your uni again""")
    return str(resp)


def error(message):
    """
    Error Handler

    Returns: TwiML to send to user
    """

    resp = MessagingResponse()
    error_message = "Error: " + str(message)
    resp.message(error_message)
    return str(resp)


def exist_user(phone_number, body):
    """ Handles communication with existing Skybot users

    Keyword arguments:
    phone_number -- user's phone number
    body -- user's text message

    Returns: TwiML to send to user
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

        message = verify(phone_number, body)
    elif curr_user.verified == "EMAIL_SENT" and int(body) != curr_user.verification_code:
        # update verified so new email is sent
        curr_user.verified = "NONE"
        db.session.commit()

        message = reverfiy_uni()
    elif str(curr_user.verified) in ["VERIFIED", "AIRPORT_INFO", "FLIGHT_TIME", "DATE_INFO", "FINISHED"]:
        message = verify(phone_number, body)
    else:
        message = error("Something unexpected happened, please try later")
    return message


def new_user(phone_number):
    """ Handles communication with new Skybot users

    Keyword arguments:
    phone_number -- user's phone number

    Returns: TwiML to send to user
    """
    global uni_entered

    uni_entered = True
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


def check_uni(body):
    """
    Handles checking if uni is valid or not

    Returns: True or False depending on valid uni
    """
    valid_uni = True

    uni_chars = re.sub("[0-9]", '', body)
    if len(uni_chars) < 2 or len(uni_chars) > 3:
        valid_uni = False

    uni_int = re.sub("[a-zA-Z]", "", body)
    if len(uni_int) != 4:
        valid_uni = False

    return valid_uni


def remove_user(pnumber):
    """
    Handles removing a user from table

    Returns nothing, removes user from DB
    """
    user = User.query.filter_by(phone_number=str(pnumber)).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """ Handles text communication with users

    Returns: TwiML to send to user
    """
    global uni_entered
    # gets phone number of user
    pnumber = request.values.get('From', None)

    # checks db for existing user
    check_num = db.session.query(User).filter(User.phone_number == pnumber)
    if db.session.query(check_num.exists()).scalar() is False:
        out_message = new_user(pnumber)
    else:
        body = request.values.get('Body', None)
        if uni_entered == True:
            uni_entered = False
            valid = check_uni(body)
            if valid == False:
                remove_user(pnumber)
                return str(error("Invalid uni!"))

        out_message = exist_user(pnumber, body)

    return str(out_message)


def matchFound(cur_user, cur_fltDate, cur_fltTime, cur_airport):
    current_user = cur_user
    current_fltDate = cur_fltDate
    current_fltTime = cur_fltTime
    current_airport = cur_airport

    match_list = []

    # Queries for the first match based on flight date, time and aiport
    matched_flight = (Flight.query.filter(
        Flight.flight_date == current_fltDate, Flight.departure_time ==
        current_fltTime, Flight.airport == current_airport,
    )).first()  # getting all flights with the same departure date

    if matched_flight == None:
        # Adds the users flight data to the database after querying (avoids matching with itself)
        user_flight_data = Flight(
            airport=current_airport, flight_date=current_fltDate,
            departure_time=current_fltTime, passenger=current_user,
        )
        db.session.add(user_flight_data)
        db.session.commit()

    else:

        user_flight_data = Flight(
            airport=current_airport, flight_date=current_fltDate,
            departure_time=current_fltTime, passenger=current_user,
        )
        db.session.add(user_flight_data)
        db.session.commit()

        match_airport = current_airport
        match_date = current_fltDate

        # Finds the rider with the earliest departure time and subtracts two hours
        match_departTime = str(
            (min(int(current_fltTime), int(matched_flight.departure_time))) - 20000,
        )

        # Creates new match instance
        new_match = Match(
            airport=match_airport, ride_date=match_date,
            ride_departureTime=match_departTime,
        )
        db.session.add(new_match)
        db.session.commit()

        # Add match to the flight
        user_flight_data.ride = new_match
        matched_flight.ride = new_match

        for riderss in new_match.riders:
            match_list.append(str(riderss.passenger.uni))

    return match_list


if __name__ == "__main__":
    app.run(debug=True)
