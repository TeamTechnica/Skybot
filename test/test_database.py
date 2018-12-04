#import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append('Skybot/')
from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy

engine = create_engine(
    'postgres://ehepwtnqjcfntn:04461d661ce43b16602000fb490e32ece1f3558bddac8f4c6059886544f7c7cd@ec2-107-21-125-209.compute-1.amazonaws.com:5432/d6uqqsindhtp99',
)
Session = sessionmaker(autoflush=True, autocommit=False, bind=engine)
conn = engine.connect()
session = Session(bind=conn)

db.drop_all()
db.create_all()


# Creates test database instances

test_user1 = User(
    uni='test100', max_passengers=2, phone_number="100000001",
    flights=[], verification_code=123, verified="isVerified",
)
test_user2 = User(
    uni='test101', max_passengers=1, phone_number="100000002",
    flights=[], verification_code=456, verified="isVerified",
)
test_user3 = User(
    uni='test102', max_passengers=2, phone_number="100000003",
    flights=[], verification_code=789, verified="isVerified",
)
test_user4 = User(
    uni='test103', max_passengers=2, phone_number="100000004",
    flights=[], verification_code=101, verified="isVerified",
)
test_user5 = User(
    uni='test105', max_passengers=2, phone_number="100000005",
    flights=[], verification_code=129, verified="isVerified",
)


test_flight1 = Flight(
    airport='JFK', flight_date=10312018,
    departure_time=1028, passenger_id=test_user1.id, match_id=None,
)
test_flight2 = Flight(
    airport='JFK', flight_date=10312018,
    departure_time=1230, passenger_id=test_user2.id, match_id=None,
)
test_flight3 = Flight(
    airport='LGA', flight_date=12252018,
    departure_time=1245, passenger_id=test_user3.id, match_id=None,
)
test_flight4 = Flight(
    airport='LGA', flight_date=12252018,
    departure_time=900, passenger_id=test_user4.id, match_id=None,
)
test_flight5 = Flight(
    airport='LGA', flight_date=12252018,
    departure_time=1100, passenger_id=test_user1.id, match_id=None,
)
test_flight6 = Flight(
    airport='JFK', flight_date=10312018,
    departure_time=928, passenger_id=test_user5.id, match_id=None,
)


# db.session.add_all([test_user1, test_user2, test_user3, test_user4, test_flight1, test_flight2, test_flight3, test_flight4, test_flight5])
# db.session.commit()

class TestDatabase(unittest.TestCase):

    # Testing for schema

    def test_UserSchema(self):
        result = str(User)
        self.assertEqual(result, "<class 'database.User'>")

    def test_FlightSchema(self):
        result = str(Flight)
        self.assertEqual(result, "<class 'database.Flight'>")

    def test_MatchSchema(self):
        result = str(Match)
        self.assertEqual(result, "<class 'database.Match'>")

    #  Test querying data

    def test_AddingUsers(self):
        db.session.add(test_user1)
        db.session.add(test_user2)
        db.session.add(test_user3)
        db.session.add(test_user4)
        db.session.commit()

        result = str(User.query.all())
        self.assertEqual(result, "[<id 1>, <id 2>, <id 3>, <id 4>]")

    def test_AddingFlight(self):
        db.session.add(test_flight1)
        db.session.add(test_flight2)
        db.session.add(test_flight3)
        db.session.add(test_flight4)
        db.session.add(test_flight5)
        db.session.commit()

        result = str(Flight.query.all())
        self.assertEqual(result, "[<id 1>, <id 2>, <id 3>, <id 4>, <id 5>]")

    def test_UserQuery(self):
        # Checks whether existing user's phone number can be found in the db

        pnumber = '100000001'
        check_num = db.session.query(User).filter(User.phone_number == pnumber)
        result = db.session.query(check_num.exists()).scalar()
        self.assertEqual(result, True)

    def test_ReturnUserInfo(self):
        # Query a user's max passengers and phone number based on uni

        test_uni = 'test101'
        user = db.session.query(User).filter(User.uni == test_uni).first()
        phone = user.phone_number
        maxpass = user.max_passengers
        result = (phone, maxpass)
        self.assertEqual(result, ('100000002', 1))

    def test_ReturnFlightInfo(self):
        # Query flight times and airports based on date

        test_date = 10312018
        matching_flights = db.session.query(Flight).filter(
            Flight.flight_date == test_date,
        ).all()

        flight_info = []

        for i in range(0, len(matching_flights)):
            flight_info.append(
                (
                    matching_flights[i].airport,
                    matching_flights[i].departure_time,
                ),
            )

        result = flight_info
        self.assertEqual(result, [('JFK', 1028), ('JFK', 1230)])

    def test_Delete(self):
        # Deletes test cases from database
        Flight.query.filter_by(id=test_flight3.id).delete()
        results = str(Flight.query.all())
        self.assertEqual(results, "[<id 1>, <id 2>, <id 4>, <id 5>]")

    def test_RepeatedUni(self):
        error = "false"
        try:
            test_user6 = User(
                uni='test100', max_passengers=2,
                phone_number="100000001",
            )
            db.session.add(test_user6)
            db.session.commit()
        except:
            db.session.rollback()
            error = "User is already in database"
        self.assertEqual(error, "User is already in database")
