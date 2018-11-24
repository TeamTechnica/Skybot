from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security  import generate_password_hash
import sqlite3
import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import sys


sys.path.append('Skybot/')
from database import *
from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    quantity = db.Column(db.Integer)

class User(db.Model):
    """ SQLAlchemy Users Model """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uni = db.Column(db.String(80), nullable=False, unique=True)
    max_passengers = db.Column(db.Integer)
    phone_number = db.Column(db.String(50), unique = True)
    verification_code = db.Column(db.Integer)
    verified = db.Column(db.String(10), default='NONE')

    stock = db.relationship('Match', backref='product',
                         primaryjoin=id == Match.user_id)

    # def __init__(self, uni, max_passengers, phone_number):
    #     self.uni = uni
    #     self.max_passengers = max_passengers
    #     self.phone_number = phone_number

    # def __repr__(self):
    #     return '<User {}>'.format(self.uni)

class Flight(db.Model):
    """ SQLAlchemy Flights Model """
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_num = db.Column(db.String(80), nullable=False) #added this field
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    airport = db.Column(db.String(3))
    flight_date =  db.Column(db.Integer)
    departure_time = db.Column(db.Integer)


    stock = relationship('Match', backref='flight',
                         primaryjoin=id == Match.flight_id)

    # def __init__(self, airport, flight_date, departure_time):
    #     self.airport = airport
    #     self.flight_date = flight_date
    #     self.departure_time = departure_time

    # def __repr__(self):
    #     return '<Category {}>'.format(self.flight_num)


if __name__ == '__database__':
    app.run(Debug=True)
