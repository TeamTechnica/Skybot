from databaseChanges import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy
#==================
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tester.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///tester.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()

usr = User(uni= "ksp2127", max_passengers=2, phone_number="123")
usr1 = User(uni ="ksp222", max_passengers=2, phone_number="321")

mat1 = Match(airport='JFK', ride_date="080911", ride_departureTime="120000")

flt1 = Flight( airport='JFK', flight_date="080911", departure_time="120000", passenger=usr1, ride=mat1)
flt2 = Flight( airport='JFK', flight_date="080901", departure_time="140000", passenger=usr, ride=mat1)
flt3 = Flight(airport='JFK', flight_date="080911", departure_time="160000", passenger=usr1, ride=mat1)


session.add_all([usr, usr1, mat1, flt1, flt2, flt3])
session.commit()

someFlight=Flight.query.filter_by(flight_date="080911").first()
print ((someFlight.passenger).uni)

print (usr1.flights)

print ((someFlight.ride).id)

print (mat1.riders)

for riderss in mat1.riders:
    print (riderss.passenger.uni)



#==========MATCHING ALGO=============

