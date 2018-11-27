from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security  import generate_password_hash
import sqlite3
import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
import sys
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine('sqlite:///tester.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()

# class Match(db.Model):
#     __tablename__ = 'match'
#     id = db.Column(db.Integer, primary_key=True)
#     #user_id = db.Column(db.Integer, primary_key=True)
#     flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#     quantity = db.Column(db.Integer)

class User(db.Model):
    """ SQLAlchemy Users Model """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uni = db.Column(db.String(80))
    max_passengers = db.Column(db.Integer)
    phone_number = db.Column(db.String(50), unique = True)
    flights = relationship("Flight", backref="passenger")

    #verification_code = db.Column(db.Integer)
    #verified = db.Column(db.String(10), default='NONE')

    # rideshare = db.relationship('Match', backref='user',
    #                      primaryjoin=id == Match.user_id)

class Flight(db.Model):
    """ SQLAlchemy Flights Model """
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    #creation_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    #flight_num = db.Column(db.String(6))
    airport = db.Column(db.String(3))
    flight_date =  db.Column(db.Integer)
    departure_time = db.Column(db.Integer)
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))

    # rideshare = relationship('Match', backref='flight',
    #                      primaryjoin=id == Match.flight_id)

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    airport = db.Column(db.String(3))
    ride_date =  db.Column(db.Integer)
    ride_departureTime = db.Column(db.Integer)
    #riderslist
    riders = relationship("Flight", backref="ride")



if __name__ == '__databaseChanges__':
    app.run(Debug=True)


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

#=============matching algorithm=================




#each match can go to multiple users



