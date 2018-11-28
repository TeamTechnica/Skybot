from databaseChanges import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy
# ==================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tester.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///tester.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()

usr = User(uni="ksp2127", max_passengers=2, phone_number="123")
usr1 = User(uni="ksp222", max_passengers=2, phone_number="321")


mat1 = Match(airport='JFK', ride_date="080911", ride_departureTime="120000")

flt1 = Flight(airport='JFK', flight_date="080911",
              departure_time="120000", passenger=usr)
flt2 = Flight(airport='JFK', flight_date="080901",
              departure_time="140000", passenger=usr)
flt3 = Flight(airport='JFK', flight_date="080911",
              departure_time="160000", passenger=usr1)


db.session.add_all([usr, usr1, mat1, flt1, flt2, flt3])
db.session.commit()

# ==========MATCHING ALGO=============

current_user = usr1
current_fltDate = "080911"
current_fltTime = "120000"
current_airport = 'JFK'

# Queries for the first match based on flight date, time and aiport

# getting all flights with the same departure date
matched_flight = (Flight.query.filter(Flight.flight_date == current_fltDate,
                  Flight.departure_time == current_fltTime,
                  Flight.airport == current_airport)).first()
print(matched_flight)

if matched_flight is None:
    # Adds users flight data to db after querying - avoids matching with self
    user_flight_data = Flight(airport=current_airport,
                              flight_date=current_fltDate,
                              departure_time=current_fltTime,
                              passenger=current_user)
    db.session.add(user_flight_data)
    db.session.commit()

    print("There are currently no matches, but we will keep searching!")
else:
    user_flight_data = Flight(airport=current_airport,
                              flight_date=current_fltDate,
                              departure_time=current_fltTime,
                              passenger=current_user)
    db.session.add(user_flight_data)
    db.session.commit()

    match_airport = current_airport
    match_date = current_fltDate

    # Finds the rider with the earliest departure time and subtracts two hours
    match_departTime = str((min(int(current_fltTime),
                            int(matched_flight.departure_time))) - 20000)

    # Creates new match instance
    new_match = Match(airport=match_airport, ride_date=match_date,
                      ride_departureTime=match_departTime)
    db.session.add(new_match)
    db.session.commit()

    # Add match to the flight
    user_flight_data.ride = new_match
    matched_flight.ride = new_match

    # Message are sent to users
    print("these is the matched flight")
    # print ((new_match.riders).uni)

    for riderss in new_match.riders:
        print(riderss.passenger.uni)
