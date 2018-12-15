import datetime
import os
import random
import re
import unittest
from datetime import datetime

import sendgrid
import sqlalchemy
from flask import Flask
from flask import redirect
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sendgrid.helpers.mail import *
from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from cost import *


app = Flask(__name__)
app.config.from_object(['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ehepwtnqjcfntn:04461d661ce43b16602000fb490e32ece1f3558bddac8f4c6059886544f7c7cd@ec2-107-21-125-209.compute-1.amazonaws.com:5432/d6uqqsindhtp99'

db = SQLAlchemy(app)

from database import *

# variable for uni integrity checking
airports = ["JFK", "LGA", "EWR"]


def notify_user(phone_number, unis):
    client = Client(os.getenv('TWILIO_KEY'), os.getenv('TWILIO_TOKEN'))
    message = client.messages.create(
        to=phone_number,
        from_=os.getenv('SKYBOT_TWILIO_NUM'),
        body="your matches are " + unis + ". Have a great day!",
    )


def send_matches(match_unis, match_nums):
    """Handles returning matching unis to user

    Returns: TwiML to send to user
    """
    resp = MessagingResponse()
    unis = ""

    if len(match_unis) == 0:
        resp.message(
            """No matches for you right now, but we'll send you an update if there's a match!""",
        )
    else:
        for x in range(0, len(match_unis)-2):
            unis = unis + str(match_unis[x]) + " "

        for num in match_nums:
            notify_user(num, unis)

        reply = "Your matches are " + unis + ". Have a great day!"
        resp.message(reply)

    return resp


def parse_date(date_entry):
    """
    Handles checking valid date entry

    Returns: Boolean if valid and date string for matching
    if valid
    """
    cur_date = datetime.datetime.now()
    flt_date = str(date_entry)

    if re.match(r"[0-9]*-[0-9]*-[0-9]*", flt_date) is not None:
        date_str = flt_date.replace('-', '')
    else:
        return False, ""

    entry_date = datetime.datetime(
        int(date_str[4:8]), int(date_str[0:2]), int(date_str[2:4]),
    )
    if (
        len(date_str) > 8 or len(date_str) < 1 or
        int(date_str[0:2].lstrip("0")) < 0 or
        int(date_str[0:2].lstrip("0")) > 12 or
        int(date_str[2:4].lstrip("0")) < 1 or
        int(date_str[2:4].lstrip("0")) > 31 or
        entry_date < cur_date
    ):
        return False, ""
    else:
        return True, date_str


def parse_time(body):
    """
    Handles checking valid date entry

    Returns: Boolean if valid and date string for matching
    if valid
    """
    print("Body: " + str(body))
    time_ent = body
    if re.search('[a-zA-Z]', time_ent) is not None:
        return False, ""
    elif(
        len(time_ent) != 6 or
        int(time_ent[0:2].lstrip("0")) > 24 or int(time_ent[0:2].lstrip("0")) < 1 or
        int(time_ent[2:4].lstrip("0")) < 1 or int(time_ent[2:4].lstrip("0")) > 60 or 
        int(time_ent[4:6].lstrip("0")) < 1 or
        int(time_ent[4:6].lstrip("0")) > 60
    ):
        return False, ""
    else:
        return True, time_ent


def parse_max(body):
    """
    Handles checking valid time entry

    Returns: Boolean if valid and time string for matching
    if valid
    """
    max_entry = body

    if re.search('[a-zA-Z]', max_entry) is not None:
        return False, ""
    elif int(max_entry) > 2 or int(max_entry) < 1:
        return False, ""
    else:
        return True, int(max_entry)


def verify(pnumber, body):
    """ Handles initial info collection for flight

    Returns: TwiML to send to user
    """

    # triggered when they send the correct verification code
    resp = MessagingResponse()

    row = db.session.query(User).filter(User.phone_number == pnumber).first()

    if str(row.verified) == "VERIFIED":
        resp.message("""Thanks for verifying! Let's get started with your
        flight information. Please enter the Airport
        (1)JFK (2)LGA (3)EQR""")

        row.verified = "AIRPORT_IN"
        db.session.commit()
    elif str(row.verified) == "AIRPORT_IN":
        if re.search('[a-zA-Z]', body) is not None:
            resp.message("""No letters. Please enter 1 for JFK, 2 for
                LGA or 3 for EWR""")
        elif int(body) < 1 or int(body) > 3:
            resp.message("""Incorrect Format. Please enter 1 for JFK, 2 for
                LGA or 3 for EWR""")
        else:
            resp.message("""Please enter Date of Flight Departure in
                following format MM-DD-YYYY""")
            cur_airport = str(airports[int(body) - 1])
            new_flight(cur_airport, row.id)
            row.verified = "DATE_INFO"
            db.session.commit()
            flight = db.session.query(Flight).order_by(Flight.id.desc()).filter(Flight.passenger_id == row.id).first()
            flight.airport = cur_airport
            db.session.commit()
    elif str(row.verified) == "DATE_INFO":
        valid, str_date = parse_date(body)
        if valid is True:
            cur_fltDate = int(str_date)
            
            resp.message("""Please enter flight time in following Military
                time format HHMMSS""")
            row.verified = "FLIGHT_TIM"
            db.session.commit()
            flight = db.session.query(Flight).order_by(Flight.id.desc()).filter(Flight.passenger_id == row.id).first()
            flight.flight_date = int(cur_fltDate)
            db.session.commit()
        else:
            resp.message("""Incorrect Format. Please enter in following format
                MM-DD-YYYY""")
    elif str(row.verified) == "FLIGHT_TIM":
        valid, str_time = parse_time(body)
        if valid is True:
            resp.message("""Last thing, please enter the max number of
            passengers you're willing to ride with as a number. Ex. 2""")
            
            cur_fltTime = int(str_time)
            
            row.verified = "FINISHED"
            db.session.commit()
            flight = db.session.query(Flight).order_by(Flight.id.desc()).filter(Flight.passenger_id == row.id).first()
            flight.departure_time = int(cur_fltTime)
            db.session.commit()
        else:
            resp.message(
                """Incorrect Format. Please enter in milliary format HHMMSS""",
            )
    elif str(row.verified) == "FINISHED":
        valid, int_max = parse_max(body) 

        flight = db.session.query(Flight).order_by(Flight.id.desc()).filter(Flight.passenger_id == row.id).first()

        if valid is True:
            cur_max = int_max
            matches, match_nums = matchFound(row, flight, cur_max)
            resp = send_matches(matches, match_nums)
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
    if check_uni(uni) is True:
        pass
    else:
        return str(error("Invalid uni: Send it again."))

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
    resp.message(
        """Check your email for a verification email and text us the code""",
    )

    # update email verified
    row.verified = "EMAIL_SENT"
    db.session.commit()

    return str(resp)


def reverify_uni():
    """
    Handles the case when wrong verification_code given

    Returns: TwiML to send to user
    """
    resp = MessagingResponse()
    resp.message(
        """Sorry the verification_code does not match. Please enter your uni again""",
    )
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

def check_valid_code(pnumber, body):
    """ Handles checking valid code

    Keyword arguments:
    phone_number -- user's phone number
    body -- user's input code

    Returns boolean
    """
    curr_user = db.session.query(User).filter_by(
        phone_number=pnumber,
    ).first()

    if re.search('[a-zA-Z]', body) is None:
        pass
    else:
        return False

    if int(body) == curr_user.verification_code is False:
        return False
    else:
        return True




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
        # email is not verified
        message = send_verify_email(body, body + "@columbia.edu", phone_number)
    elif curr_user.verified == "EMAIL_SENT" and check_valid_code(phone_number, body) == True:
        # update verified state to "VERIFIED"
        curr_user.verified = "VERIFIED"
        db.session.commit()

        message = verify(phone_number, body)
    elif curr_user.verified == "EMAIL_SENT" and check_valid_code(phone_number, body) == False:
        # update verified so new email is sent
        curr_user.verified = "NONE"
        db.session.commit()

        message = error("Sorry the code doesn't match. Please input uni again so we can send a new code")

    elif str(curr_user.verified) in ["VERIFIED", "AIRPORT_IN", "FLIGHT_TIM", "DATE_INFO", "FINISHED"]:
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
    # create & insert new user into database
    new_user = User(
        phone_number=phone_number,
        verified="NONE", verification_code=0,
        uni="NONE", max_passengers=0, flights=[],
    )
    db.session.add(new_user)
    db.session.commit()

    # send confirmation message & ask for UNI
    resp = MessagingResponse()
    resp.message("Welcome to Skybot! What's your UNI?")
    return str(resp)


def new_flight(current_airport, user_id):
    """ inserts a new flight

    Keyword arguments:
    current_airport -- user's airport
    user_id -- user's id
    """
    # create & insert new user into database
    new_flight = Flight(
        airport=current_airport, flight_date=-1,
        departure_time=-1, passenger_id=user_id,
        match_id=None,
    )
    db.session.add(new_flight)
    db.session.commit()


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


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """ Handles text communication with users

    Returns: TwiML to send to user
    """
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


def matchFound(cur_user, flight, cur_max):
    """ Matches users together to take a cab together

    Returns: 
        match_unis: UNIs for each matched user
        match_nums: phone numbers for each matched user
    """
    # If their max  passengers is 1, it queries fligths that are 1
    # hours within the flight depature that that were not matched.
    if cur_max == 1:
        matched_flight = db.session.query(Flight).filter(
            Flight.flight_date == flight.flight_date, Flight.passenger_id != cur_user.id, Flight.departure_time.between(
                (flight.departure_time - 100), (flight.departure_time + 100),
            ), Flight.airport == flight.airport, (Flight.match_id == None),
        ).first()  # getting all flights with the same departure date

    # If their max  passengers is 2, it queries fligths that are 1
    # hours within the flight depature that that were not matched

    if cur_max == 2:

        matched_flight = db.session.query(Flight).filter(
            Flight.flight_date == flight.flight_date, Flight.passenger_id != cur_user.id, Flight.departure_time.between(
                (flight.departure_time-100), (flight.departure_time + 100),
            ), Flight.airport == flight.airport, (Flight.match_id == None),
        ).first()

        # If there were no rides, that fit that criteria then
        # it queries flights that were matched but have space
        # that have the same flight depature or up to one hour later

        if matched_flight == None:

            available_rides = []

            previously_matched_flights = db.session.query(Flight).filter(
                Flight.flight_date == flight.flight_date, Flight.departure_time.between(
                    (flight.departure_time), (flight.departure_time + 100),
                ), Flight.airport == flight.airport, (Flight.match_id != None),
            )

            for x in previously_matched_flights:

                match_instance = db.session.query(Match).filter(
                    Match.id == x.match_id,
                ).first()

                if (match_instance.available_seats == 1):
                    matched_flight = x
                    break

    # If there were no matches, the user's flight is
    # added to the db and an empty list is returned

    if matched_flight == None:
        return [], []

    # Otherwise
    else:


        # If the user was matched to a flight that was not previously matched
        if matched_flight.match_id == None:

            match_airport = flight.airport
            match_date = flight.flight_date

            matched_passenger_id = matched_flight.passenger_id

            # Calculates whether there will be an available seats
            # based on the preferences of the two users
            matched_user = db.session.query(User).filter(
                User.id == matched_passenger_id,
            ).first()
            match_availableSeats = (
                min(int(cur_max), int(matched_user.max_passengers))
            ) - 1

            # Finds the rider with the earliest departure time and subtracts two hours
            match_departTime = (min(
                int(flight.departure_time), int(
                    matched_flight.departure_time,
                ),
            )) - 200

            # Creates new match instance and adds to DB
            new_match = Match(
                airport=match_airport,
                ride_date=match_date,
                ride_departureTime=match_departTime,
                available_seats=match_availableSeats,
                riders=[],
            )
            db.session.add(new_match)
            db.session.commit()

            # Updates the match ID for the user and matching flight
            flight.ride = new_match
            matched_flight.ride = new_match

            # Creates a list of the riders' UNIs
            match_unis = []
            match_nums = []

            for riderss in new_match.riders:
                match_unis.append(str(riderss.passenger.uni))
                match_nums.append(str(riderss.passenger.phone_number))

            # At the end of the array, it appends the ride depature time
            match_unis.append(match_departTime)
            match_unis.append(match_airport)
            # returns list of UNIs in ride
            return match_unis, match_nums

        # If user was matched to a previously matched flight
        else:

            # Updates the users ride to be the matched flight's ride
            flight.ride = matched_flight.ride

            # Updates the number of available seats in the match
            shared_match_id = matched_flight.match_id
            shared_match = db.session.query(Match).filter(
                Match.id == shared_match_id,
            ).first()
            shared_match.available_seats = (shared_match.available_seats - 1)

            # Creates a list of the riders' UNIs and phone numbers
            match_unis = []
            match_nums = []

            for riderss in shared_match.riders:
                match_unis.append(str(riderss.passenger.uni))
                match_nums.append(str(riderss.passenger.phone_number))

            # Query the flights with the match ID
            earliest_flight = db.session.query(Flight).filter(
                Match.id == shared_match_id,
            ).order_by(Flight.departure_time).first()
            ride_departure = earliest_flight.departure_time - 200

            match_unis.append(ride_departure)
            match_unis.append(flight.airport)

            # returns list of UNIs in ride
            return match_unis, match_nums


if __name__ == "__main__":
    app.run(debug=True)
