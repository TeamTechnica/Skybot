import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# import sys
# sys.path.append('Skybot/')
from database import *
from match import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///match.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///match.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()


# Creates test data

test_user1 = User(uni='test100', max_passengers=2, phone_number="100000001", verification_code=123,verified="isVerified")
test_user2 = User(uni='test101', max_passengers=1,phone_number="100000002", verification_code=456, verified="isVerified")
test_user3 = User(uni='test102', max_passengers=2, phone_number="100000003", verification_code=789, verified="isVerified")
test_user4 = User(uni='test103', max_passengers=2, phone_number="100000004", verification_code=101, verified="isVerified")
test_user5 = User(uni='test105', max_passengers=2, phone_number="100000005", verification_code=129,verified="isVerified")
db.session.add(test_user1)
db.session.add(test_user2)
db.session.add(test_user3)
db.session.add(test_user4)
db.session.add(test_user5)
db.session.commit()

test_flight1 = Flight(airport='JFK', flight_date=10312018, departure_time=1028, passenger_id = test_user1.id)
test_flight2 = Flight(airport='JFK', flight_date=10312018, departure_time=1230, passenger_id = test_user2.id)
test_flight3 = Flight(airport='LGA', flight_date=12252018, departure_time=1245, passenger_id = test_user3.id)
test_flight4 = Flight(airport='LGA', flight_date=12252018, departure_time= 900, passenger_id = test_user4.id)
test_flight5 = Flight(airport='LGA', flight_date=12252018, departure_time=1100, passenger_id = test_user1.id)
test_flight6 = Flight(airport='JFK', flight_date=10312018, departure_time= 928, passenger_id = test_user5.id)

db.session.add(test_flight1)
db.session.add(test_flight2)
db.session.add(test_flight3)
db.session.add(test_flight4)
db.session.add(test_flight5)
db.session.add(test_flight6)
db.session.commit()

test_match1 = Match(airport='JFK', ride_date=10312018, ride_departureTime=102800, available_seats = 1)
db.session.add(test_match1)
db.session.commit()

test_flight1.match_id = test_match1.id
test_flight6.match_id = test_match1.id

new_user = User( uni='jna2123', max_passengers=2, phone_number="6092517239", verification_code=999, verified="isVerified")
new_user2 = User( uni='ksp1234', max_passengers=2, phone_number="1234569999", verification_code=111, verified="isVerified")
new_user3 = User( uni='ksp1235', max_passengers=2, phone_number="1234569989", verification_code=121, verified="isVerified")

db.session.add(new_user)
db.session.add(new_user2)
db.session.add(new_user3)
db.session.commit()




class TestMatch(unittest.TestCase):

    # Testing for schema

    def test_MatchExistingMatch(self):

        flt = 'JFK'
        date=10312018
        time=828
        maxx = 2
        results = matchFound(new_user, date, time, flt, maxx)
        self.assertEqual(results, ['test105', 'test101', 'jna2123', 628, 'JFK'] )

    def test_NonMatch(self):
        
        flt = 'JFK'
        date=10312018
        time=1528
        maxx = 2

        results = matchFound(new_user2, date, time, flt, maxx)
 
        self.assertEqual(results, ['ksp1234', 'ksp1235', 1328, 'JFK'])

    def test_MatchingWithNonMatch(self):

        flt = 'JFK'
        date=10312018
        time=1628
        maxx = 2

        results = matchFound(new_user3, date, time, flt, maxx)

        self.assertEqual(results, [])
