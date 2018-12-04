import unittest
from datetime import datetime

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
'''
from app import *


engine = create_engine(
    'postgres://ehepwtnqjcfntn:04461d661ce43b16602000fb490e32ece1f3558bddac8f4c6059886544f7c7cd@ec2-107-21-125-209.compute-1.amazonaws.com:5432/d6uqqsindhtp99',
)
Session = sessionmaker(autoflush=True, autocommit=False, bind=engine)
conn = engine.connect()
session = Session(bind=conn)
'''

def matchFound(cur_user, cur_fltDate, cur_fltTime, cur_airport, cur_maxPass):

    # Stores the user, their flight time, date, airport,
    # and prefered max number of additional passengers
    current_user = cur_user
    current_fltDate = cur_fltDate
    current_fltTime = cur_fltTime
    current_airport = cur_airport
    current_maxPass = cur_maxPass

    # If their max  passengers is 1, it queries fligths that are 1
    # hours within the flight depature that that were not matched.
    if current_maxPass == 1:
        matched_flight = (Flight.query.filter(
            Flight.flight_date == current_fltDate, Flight.departure_time.between(
                (current_fltTime - 100), (current_fltTime + 100),
            ), Flight.airport == current_airport, (Flight.match_id == None),
        ).first())  # getting all flights with the same departure date

    # If their max  passengers is 2, it queries fligths that are 1
    # hours within the flight depature that that were not matched

    if current_maxPass == 2:

        matched_flight = (Flight.query.filter(
            Flight.flight_date == current_fltDate, Flight.departure_time.between(
                (current_fltTime-100), (current_fltTime + 100),
            ), Flight.airport == current_airport, (Flight.match_id == None),
        ).first())

        # If there were no rides, that fit that criteria then
        # it queries flights that were matched but have space
        # that have the same flight depature or up to one hour later

        if matched_flight == None:

            available_rides = []

            previously_matched_flights = Flight.query.filter(
                Flight.flight_date == current_fltDate, Flight.departure_time.between(
                    (current_fltTime), (current_fltTime + 100),
                ), Flight.airport == current_airport, (Flight.match_id != None),
            )

            for x in previously_matched_flights:

                match_instance = Match.query.filter(
                    Match.id == x.match_id,
                ).first()

                if (match_instance.available_seats == 1):
                    matched_flight = x
                    break

    # If there were no matches, the user's flight is
    # added to the db and an empty list is returned

    if matched_flight == None:
        user_flight_data = Flight(
            airport=current_airport, flight_date=current_fltDate,
            departure_time=current_fltTime, passenger_id=current_user.id,
            match_id=None,
        )
        db.session.add(user_flight_data)
        db.session.commit()

        return []

    # Otherwise
    else:

        # First user flight data is added to DB
        user_flight_data = Flight(
            airport=current_airport, flight_date=current_fltDate,
            departure_time=current_fltTime, passenger_id=current_user.id,
            match_id=None,
        )
        db.session.add(user_flight_data)
        db.session.commit()

        # If the user was matched to a flight that was not previously matched
        if matched_flight.match_id == None:

            match_airport = current_airport
            match_date = current_fltDate

            matched_passenger_id = matched_flight.passenger_id

            # Calculates whether there will be an available seats
            # based on the preferences of the two users
            matched_user = User.query.filter(
                User.id == matched_passenger_id,
            ).first()
            match_availableSeats = (
                min(int(current_maxPass), int(matched_user.max_passengers))
            ) - 1

            # Finds the rider with the earliest departure time and subtracts two hours
            match_departTime = (min(
                int(current_fltTime), int(
                    matched_flight.departure_time,
                ),
            )) - 200

            # Creates new match instance and adds to DB
            new_match = Match(
                airport=match_airport, ride_date=match_date,
                ride_departureTime=match_departTime, available_seats=match_availableSeats,
                riders=[],
            )
            db.session.add(new_match)
            db.session.commit()

            # Updates the match ID for the user and matching flight
            user_flight_data.ride = new_match
            matched_flight.ride = new_match

            # Creates a list of the riders' UNIs
            match_list = []

            for riderss in new_match.riders:
                match_list.append(str(riderss.passenger.uni))

            # At the end of the array, it appends the ride depature time
            match_list.append(match_departTime)
            match_list.append(match_airport)
            # returns list of UNIs in ride
            return match_list

        # If user was matched to a previously matched flight
        else:

            # Updates the users ride to be the matched flight's ride
            user_flight_data.ride = matched_flight.ride

            # Updates the number of available seats in the match
            shared_match_id = matched_flight.match_id
            shared_match = (Match.query.filter(
                Match.id == shared_match_id,
            )).first()
            shared_match.available_seats = (shared_match.available_seats - 1)

            # Creates a list of the riders' UNIs
            match_list = []

            for riderss in shared_match.riders:
                match_list.append(str(riderss.passenger.uni))

            # Query the flights with the match ID
            earliest_flight = (Flight.query.filter(
                Match.id == shared_match_id,
            ).order_by(Flight.departure_time)).first()
            ride_departure = earliest_flight.departure_time - 200

            match_list.append(ride_departure)
            match_list.append(user_flight_data.airport)

            # returns list of UNIs in ride
            return match_list


# Notes for app.py:
# What is returned:
    # Either an empty list, meaning that the User was not matched to anyone
    # OR, an array with the list of UNIs in the match, their depature time, and the airport
    # For ride cost calculations, find the length of the array minus 2
    # (which accounts for the 2 spaces in the array taken by the departure time and airport)
