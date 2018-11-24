import sys
sys.path.append('Skybot/')
from database_changes import *
#from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tester2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///tester2.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()

# Creates test database instances

test_user1 = User(uni='test100', max_passengers = 2, phone_number = "100000001")
test_user2 = User(uni='test101', max_passengers = 1, phone_number = "100000002")
test_user3 = User(uni='test102', max_passengers = 2, phone_number = "100000003")
test_user4 = User(uni='test103', max_passengers = 2, phone_number = "100000004")

test_flight1 = Flight(airport = 'JFK', flight_date = 10312018, departure_time = 123000)
test_flight2 = Flight(airport = 'JFK', flight_date = 10312018, departure_time = 123000)
test_flight3 = Flight(airport = 'LGA', flight_date = 12252018, departure_time = 124500)
test_flight4 = Flight(airport = 'LGA', flight_date = 12252018, departure_time = 100000)
test_flight5 = Flight(airport = 'LGA', flight_date = 12252018, departure_time = 100000)


# class TestDatabase(unittest.TestCase):

#     # Testing for schema
    
#     def test_UserSchema(self):    
#         result = str(User)
#         self.assertEqual(result, "<class 'database_changes.User'>")

#     def test_FlightSchema(self):    
#         result = str(Flight)
#         self.assertEqual(result, "<class 'database_changes.Flight'>")

#     def test_MatchSchema(self):    
#         result = str(Match)
#         self.assertEqual(result, "<class 'database_changes.Match'>")

#      #Test querying data
    
#     def test_AddingUsers(self):
#         session.add(test_user1)
#         session.add(test_user2)
#         session.add(test_user3)
#         session.add(test_user4)
#         session.commit()
    
#         result = str(User.query.all())
#         self.assertEqual(result, "[<User 1>, <User 2>, <User 3>, <User 4>]")

#     def test_AddingFlight(self):
#         session.add(test_flight1)
#         session.add(test_flight2)
#         session.add(test_flight3)
#         session.add(test_flight4)
#         session.add(test_flight5)
#         session.commit()

#         result = str(Flight.query.all())
#         self.assertEqual(result, "[<Flight 1>, <Flight 2>, <Flight 3>, <Flight 4>, <Flight 5>]")

#     # Checks whether an given existing user's phone number can be found in the database
#     def test_UserQuery(self):

#         pnumber = '100000001'
#         check_num = session.query(User).filter(User.phone_number == pnumber)
#         result = session.query(check_num.exists()).scalar()
#         self.assertEqual(result, True)
    
#     # Query a user's max passengers and phone number based on uni
#     def test_ReturnUserInfo(self):
#         test_uni = 'test101'
#         user = session.query(User).filter(User.uni == test_uni).first()
#         phone = user.phone_number
#         maxpass = user.max_passengers
#         result = (phone, maxpass)
#         self.assertEqual(result, ('100000002',1))

# # Query flight times and airports based on date

#     def test_ReturnFlightInfo(self):
#         test_date = '10312018'
#         matching_flights = session.query(Flight).filter(Flight.flight_date == test_date).all()

#         flight_info = []

#         for i in range (0,len(matching_flights)):
#             flight_info.append((matching_flights[i].airport, matching_flights[i].departure_time ))
       
#         result = flight_info
#         self.assertEqual(result, [('JFK', 123000), ('JFK', 123000)])


# # Deletes test cases from database
#     def test_Delete(self):
#         Flight.query.filter_by(id=test_flight3.id).delete()
#         results = str(Flight.query.all())
#         self.assertEqual(results, "[<Flight 1>, <Flight 2>, <Flight 4>, <Flight 5>]")

#     def test_RepeatedUni(self):
#         error = "false"
#         try:
#             print ("commit successful")
#             test_user6 = User(uni='test100', max_passengers = 2, phone_number = "100000001")
#             session.add(test_user6)
#             session.commit()
#         except:
#             session.rollback()
#             error = "User is already in database"
#         self.assertEqual(error, "User is already in database")





