import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from databaseChanges import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy
from sqlalchemy import exists
from datetime import datetime


# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tmp/test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# engine = create_engine('sqlite:///tester.db')
#Session = sessionmaker(bind=engine)
#session = Session()

engine = sqlalchemy.create_engine('sqlite:////tmp/test.db')
Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
Base.metadata.drop_all(engine)

#db.drop_all()
#db.create_all()



# test_user1 = User(id=1, uni='test100', max_passengers = 2, phone_number = "100000001", verification_code = 0, verified = "isVerified")
# test_user2 = User(id=2, uni='test101', max_passengers = 1, phone_number = "100000002", verification_code = 0, verified = "isVerified")
# test_user3 = User(id=3, uni='test102', max_passengers = 2, phone_number = "100000003", verification_code = 0, verified = "isVerified")
# test_user4 = User(id=4, uni='test103', max_passengers = 2, phone_number = "100000004", verification_code = 0, verified = "isVerified")


test_user1 = User(id=1, uni='test100', max_passengers = 2, phone_number = "100000001")
test_user2 = User(id=2, uni='test101', max_passengers = 1, phone_number = "100000002")
test_user3 = User(id=3, uni='test102', max_passengers = 2, phone_number = "100000003")
test_user4 = User(id=4, uni='test103', max_passengers = 2, phone_number = "100000004")
print ("hello")

test_flight1 = Flight(airport = 'JFK', flight_date = 10312018, departure_time = 122800)
test_flight2 = Flight(id= 1, airport = 'JFK', flight_date = 10312018, departure_time = 123000)
test_flight3 = Flight(id=2, airport = 'LGA', flight_date = 12252018, departure_time = 124500)
test_flight4 = Flight(id=3, airport = 'LGA', flight_date = 12252018, departure_time = 100000)
test_flight5 = Flight(id=4, airport = 'LGA', flight_date = 12252018, departure_time = 100000)

session.add(test_user1)
session.add(test_user2)
session.add(test_user3)
session.add(test_user4)
# session.add(test_flight1)
# session.add(test_flight2)
# session.add(test_flight3)
# session.add(test_flight4)
# session.add(test_flight5)

session.commit()


# # Write your code here

# # Checking that a match is found based on an exact time  (NOT WORKING)
# test_time = 124500
# if session.query(Flight).filter(Flight.departure_time == test_time).count():
# 	print ("There is a flight matching the time: " + str(test_time))


# #=============================

# newUniMatches = 0 
# newUni = "uni123"
# maxPassPref = 2 
# newUniPhoneNum = "100000001"
# newUniAirport = "JFK"
# newUniDate = 10312018
# newUniTime = 122800


# newUni2 = "uni163"


# newStudent = User(id = 0, uni= newUni, max_passengers = 2, phone_number = "100000001")
# newStudentFlight = Flight(id = 101, airport = "JFK", flight_date = 10312018, departure_time = 123800) #changed to 38

# #Link the student's personal information and flight information
# newStudentInfo = Match(id= 1011, flight_id= newStudentFlight.id, user_id= newStudent.id, quantity= 0) 
# #session.commit()



# newStudent2 = User(id = 10, uni= newUni2, max_passengers = 2, phone_number = "100100001")
# newStudentFlight = Flight(id = 11, airport = "JFK", flight_date = 10312018, departure_time = 123800) #changed to 38


# #Link the student's personal information and flight information
# newStudent2Info = Match(id= 111, flight_id= newStudentFlight.id, user_id= newStudent.id, quantity= 0) 
# #session.commit()


# matchingFlights = session.query(Flight).filter(Flight.flight_date == 10312018, Flight.airport == "JFK")


# matchingFlightsTest = session.query(Flight).filter(Flight.airport == newUniAirport)

# for f in matchingFlights:
# 	print (f.flight_date)

# potentialMatches = []
# timeMatches = []


# if (session.query(matchingFlights.exists()).scalar()):
# 	#go through matches and users whose quantity is 
# 	print ("matching flights exist")
# 	#(this means they have not been matched)
# 	for flights in (session.query(Flight).filter(Flight.flight_date == 10312018, Flight.airport == "JFK")):
# 		potentialMatches.append(flights) # these are matches with the same date and airport
# 		print ("I finished making potentialMatches")
# 	for i in potentialMatches:
# 		print ("I am before the if")
# 		print (i.departure_time)
# 		print (newStudentFlight.departure_time)
# 		print ((int(newStudentFlight.departure_time) - int(i.departure_time)))
# 		if ( 0 <= (int(newStudentFlight.departure_time) - int(i.departure_time)) < 10000): #the students flight departs 0 to 60 minutes after
# 			timeMatches.append(i)
# 			print ("yay")

#=========================================
	# for c in session.query(Flight).all():
	# 	for x in c.stock:
	# 		print (session.query(User).filter_by(id=x.user_id).all())

#==================this=======================
# for c in session.query(Flight).all(): #check all flights
#     print (c.flight_num) #print out the flight number
#     print ("before second for loop")
#     for a in c.stock: #for each of the flights, access stock
#         print (session.query(User).filter_by(id=a.user_id).all())
#=========================================


	# for x in timeMatches:
	# 	print (session.query(User).filter_by(id=a.user_id).all())

		#for all the flights that match airport, date and time    (! #right now this is a direct match)
		# for a in flights.stock:
		# 	print (" I am in flights stock")
		# 	print (session.query(User).filter_by(id = a.user_id).all())  #if the student is not currently matched 

	# print ("you have been matched with"+ firstMatch.uni)
	# print ("An email has been sent to them. Please contact " + firstMatch.uni + "to schedule your rideshare")
	
	# #Update the match quanitity of the matched individuals to 1 

	# firstMatch_MatchObj = session.query(Match).filter_by(id=firstMatch.user_id).first()
	# firstMatch_MatchObj.quanitity = 1

	# newStudent_MatchObj = session.query(Match).filter_by(id=newStudent.user_id).first()
	# newStudent_MatchObj.quanitity = 1 
#==================this=======================
# else:
# 	print ("we are sorry, there are no matches at this time. We will contact you if we later find a match.")
#=========================================



#===============================


# #this case replicates what would happen when a new flight of a user is added
# #and finding a flight match within a suitable time window
# new_flight = Flight(airport = 'LGA', flight_date = 12252018, departure_time = 80000)
# session.commit()
# query_matches = session.query(Flight).filter(Flight.flight_date == test_date2, Flight.airport == test_airport2)
# timeMatches = []

# if (session.query(matches.exists()).scalar()):
# 	for same in query_matches:
# 		#if we are going to match people the new flight must be at least one hour before and existing
# 		#flight but less than four hours earlier 
# 		if ( -40000 < (int(new_flight.departure_time) - int(same.departure_time)) < -10000):
# 			timeMatches.append(same)

# #print ("Here are the timeMatches: ")
# for tm in timeMatches:
# 	print(tm)
	
session.commit()

