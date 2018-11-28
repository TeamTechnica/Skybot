from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy
from sqlalchemy import exists
from datetime import datetime


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tester.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///tester.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()

# Creates test database instances

test_user1 = User(id=1, uni='test100', max_passengers=2,
                  phone_number="100000001", verification_code=123,
                  verified="isVerified")
test_user2 = User(id=2, uni='test101', max_passengers=1,
                  phone_number="100000002", verification_code=456,
                  verified="isVerified")
test_user3 = User(id=3, uni='test102', max_passengers=2,
                  phone_number="100000003", verification_code=789,
                  verified = "isVerified")
test_user4 = User(id=4, uni='test103', max_passengers=2,
                  phone_number="100000004", verification_code=101,
                  verified="isVerified")

test_flight1 = Flight(airport='JFK', flight_date=10312018,
                      departure_time=122800)
test_flight2 = Flight(airport='JFK', flight_date=10312018,
                      departure_time=123000)
test_flight3 = Flight(airport='LGA', flight_date=12252018,
                      departure_time=124500)
test_flight4 = Flight(airport='LGA', flight_date=12252018,
                      departure_time=100000)
test_flight5 = Flight(airport='LGA', flight_date=12252018,
                      departure_time=100000)

session.add(test_user1)
session.add(test_user2)
session.add(test_user3)
session.add(test_user4)
session.add(test_flight1)
session.add(test_flight2)
session.add(test_flight3)
session.add(test_flight4)
session.add(test_flight5)

session.commit()


# Write your code here

# Checking that a match is found based on an exact time  (NOT WORKING)
test_time = 124500
if session.query(Flight).filter(Flight.departure_time == test_time).count():
    pass
    # print ("There is a flight matching the time: " + str(test_time))


# Returning a list of all the flights that match an depature date
test_date = 10312018
matchingFlights = session.query(Flight).filter(Flight.flight_date == test_date)
if (session.query(matchingFlights.exists()).scalar()):
    pass
    # print ("the following fligts match your depature date: ")
    for row in matchingFlights:
        pass
        # print(row)

# match flights on time and airport
test_airport = 'JFK'
DateAirportFlights = []
matchingDateAirport = session.query(Flight).filter(Flight.flight_date == test_date)
if (session.query(matchingDateAirport.exists()).scalar()):
    pass
    # print ("I am in if statement")
    for row in matchingDateAirport:
        if row.airport == test_airport:
            # print(row)
            DateAirportFlights.append(row)

# print("List of Flights who have the same testDate and testAirport")
for match in matchingDateAirport:
        pass
        # print(match)

# another method to check for flights that match time and airport
test_date2 = 12252018
test_airport2 = 'LGA'
matches = session.query(Flight).filter(Flight.flight_date == test_date2,
                                       Flight.airport == test_airport2)
if (session.query(matches.exists()).scalar()):
    pass
    # print("The following flights match the second testDate & testAirport: ")
    for hit in matches:
        pass
        # print(hit)

# this case replicates what would happen when a new flight of a user is added
# and finding a flight match within a suitable time window
new_flight = Flight(airport='LGA', flight_date=12252018,
                    departure_time=80000)
session.commit()
query_matches = session.query(Flight).filter(Flight.flight_date == test_date2,
                                             Flight.airport == test_airport2)
timeMatches = []

if (session.query(matches.exists()).scalar()):
    for same in query_matches:
        # flight must be at least one hour before and existing
        # flight but less than four hours earlier
        if (-40000 < (int(new_flight.departure_time) - int(same.departure_time)) < -10000):
            timeMatches.append(same)

# print ("Here are the timeMatches: ")
for tm in timeMatches:
    print(tm)

# connect the users (uni) whose flight's match requirements (max passengers)


# testing the backref relationship between User and Flights
new_test_flight1 = Flight(id=7, airport='JFK', flight_date=10312018,
                          departure_time=122800, user_id=2)
new_test_flight2 = Flight(id=8, airport='JFK', flight_date=10312018,
                          departure_time=122800, user_id=4)
some_user = User.query.filter_by(id=7).first()

session.commit()


# will continue with test to access the flights linked to a user.
