# from databaseChanges import *
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import unittest
# import sqlalchemy
# #==================
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tester.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# engine = create_engine('sqlite:///tester.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# db.drop_all()
# db.create_all()

# # usr = User(uni= "ksp2127", max_passengers=2, phone_number="123")
# # usr1 = User(uni ="ksp222", max_passengers=2, phone_number="321")

# # flt1 = Flight( airport='JFK', flight_date="080911", departure_time="120000")
# # flt2 = Flight( airport='JFK', flight_date="080901", departure_time="140000")
# # flt3 = Flight(airport='JFK', flight_date="080911", departure_time="160000")

# # cp1 = Match(id=1, flight_id=flt1.id, user_id=usr.id, quantity=2)
# # usr.rideshare.append(cp1)
# # flt1.rideshare.append(cp1)

# # cp2 = Match(id=2, flight_id=flt3.id, user_id=usr.id, quantity=1)
# # usr.rideshare.append(cp2)
# # flt3.rideshare.append(cp2)

# # cp3 = Match(id=3, flight_id=flt1.id, user_id=usr1.id, quantity=0)
# # usr1.rideshare.append(cp3)
# # flt1.rideshare.append(cp3)

# # session.add_all([usr, usr1, flt1, flt2, flt3])
# # session.commit()


# ##======
# #let's assume that we have a date and time, let's find other ppl going to the airport
# ##======
# # print ("Get all flights a user belongs to")
# # for p in session.query(User).all():
# #     print (p.uni)
# #     for a in p.rideshare:
# #         print (session.query(Flight).filter_by(id=a.flight_id).all())

# # print ("Get all users that belong to a flight")
# # for c in session.query(Flight).all():
# #     print ("I am a flight: " + str(c.departure_time))
# #     for a in c.rideshare:
# #         #print ( "I am a user in this flight: ")
# #         print (session.query(User).filter_by(id=a.user_id).all())

# test = Flight( airport='JFK', flight_date="80901", departure_time="140000")



# allFlights =[]
# print ("Get all users that belong to a flight")
# for c in session.query(Flight).all():
# 	# print (c.flight_date)
# 	# print (test.flight_date)
# 	print (c)
# 	print ("user/flight/match object if they are on the same flight" + str(c.rideshare))


# 	# for a in c.rideshare:
# 	# 	#print ("I am in rideshare and this is my user id: ")
# 	# 	#print (session.query(User).filter_by(id=a.user_id).all())
# 	# 	if(int(c.flight_date) == int(test.flight_date)):
# 	# 		print ("I am c.rideshare in for " + str(c.rideshare))
# 	# if(int(c.flight_date) == int(test.flight_date)):
# 	# 	#print ("flight date is equal to the testdate")
# 	# 	#print ("I am a flight: " + str(c.departure_time))
# 	# 	print ("I am c.rideshare in if " + str(c.rideshare))
# 	# 	# if(int(c.departure_time) == int(test.departure_time)): 
# 	# 	# 	print("I have the same departure_time")
# 	# 	# 	print ("I am c.rideshare" + str(c.rideshare))
# 	# 		# for a in c.rideshare:
# 	# 		# 	print ("I am in rideshare")
# 	# 		# 	print (session.query(User).filter_by(id=a.user_id).all())
