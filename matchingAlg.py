from databaseChanges import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy
from sqlalchemy import exists
from datetime import datetime


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tester.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///tester.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()

import uuid


#=============================

newUniMatches = 0 
newUni = "uni123"
maxPassPref = 2 
newUniPhoneNum = "100000001"
newUniAirport = "JFK"
newUniDate = 10312018
newUniTime = 122800


newUni2 = "uni163"


newStudent = User(id = uuid.uuid4(), uni= newUni, max_passengers = maxPassPref, phone_number = newUniPhoneNum)
newStudentFlight = Flight(id = uuid.uuid4(), airport = newUniAirport, flight_date = newUniDate, departure_time = newUniTime)

#Link the student's personal information and flight information
newStudentInfo = Match(id= uuid.uuid4(), flight_id= newStudentFlight.id, user_id= newStudent.id, quantity= maxPassPref) 
session.commit()



newStudent2 = User(id = uuid.uuid4(), uni= newUni2, max_passengers = maxPassPref, phone_number = newUniPhoneNum)
newStudentFlight = Flight(id = uuid.uuid4(), airport = newUniAirport, flight_date = newUniDate, departure_time = newUniTime)

#Link the student's personal information and flight information
newStudent2Info = Match(id= uuid.uuid4(), flight_id= newStudentFlight.id, user_id= newStudent.id, quantity= maxPassPref) 
session.commit()


matchingFlights = session.query(Flight).filter(Flight.flight_date == newUniDate, Flight.airport == newUniAirport)


matchingFlightsTest = session.query(Flight).filter(Flight.airport == newUniAirport)

for tm in matchingFlightsTest:
	print("hello")


potentialMatches = []

if (session.query(matchingFlights.exists()).scalar()):
	#go through matches and users whose quantity is 
	#(this means they have not been matched)
	for flights in matchingFlights:	
		print ("I am in matching flights")
		#for all the flights that match airport, date and time    (! #right now this is a direct match)
		for match in flights.stock:
			print("we have a match")
			firstMatch = session.query(User).filter_by(quantity = 0).first()  #if the student is not currently matched 

	print ("you have been matched with"+ firstMatch.uni)
	print ("An email has been sent to them. Please contact " + firstMatch.uni + "to schedule your rideshare")
	
	#Update the match quanitity of the matched individuals to 1 

	firstMatch_MatchObj = session.query(Match).filter_by(id=firstMatch.user_id).first()
	firstMatch_MatchObj.quanitity = 1

	newStudent_MatchObj = session.query(Match).filter_by(id=newStudent.user_id).first()
	newStudent_MatchObj.quanitity = 1 

else:
	print ("we are sorry, there are no matches at this time. We will contact you if we later find a match.")




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

