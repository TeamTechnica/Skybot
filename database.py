import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from app import db


class User(db.Model):
    """ SQLAlchemy Users Model """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uni = db.Column(db.String(80))
    max_passengers = db.Column(db.Integer)
    phone_number = db.Column(db.String(50), unique=True)
    flights = relationship("Flight", backref="passenger")
    verification_code = Column(Integer)
    verified = Column(String(10), default='NONE')

    def __init__(self, uni, max_passengers, phone_number, flights, verification_code, verified):
        self.uni = uni
        self.max_passengers = max_passengers
        self.phone_number = phone_number
        self.flights = flights
        self.verification_code = verification_code
        self.verified = verified

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Flight(db.Model):
    """ SQLAlchemy Flights Model """
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    airport = db.Column(db.String(3))
    flight_date = db.Column(db.Integer)
    departure_time = db.Column(db.Integer)
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))

    def __init__(self, airport, flight_date, departure_time, passenger_id, match_id):
        self.airport = airport
        self.flight_date = flight_date
        self.departure_time = departure_time
        self.passenger_id = passenger_id
        self.match_id = match_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    airport = db.Column(db.String(3))
    ride_date = db.Column(db.Integer)
    ride_departureTime = db.Column(db.Integer)
    available_seats = db.Column(db.Integer)  # can be done by querying the match id
    riders = relationship("Flight", backref="ride")

    def __init__(self, airport, ride_date, ride_departureTime, available_seats, riders):
        self.airport = airport
        self.ride_date = ride_date
        self.ride_departureTime = ride_departureTime
        self.available_seats = available_seats
        self.riders = riders

    def __repr__(self):
        return '<id {}>'.format(self.id)
