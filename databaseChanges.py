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


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
engine = sqlalchemy.create_engine('sqlite:///:memory:')
Base = declarative_base()


class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    #user_id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey('flights.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    quantity = Column(Integer)

class User(Base):
    """ SQLAlchemy Users Base """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    uni = Column(String(80), nullable=False, unique=True)
    max_passengers = Column(Integer)
    phone_number = Column(String(50), unique = True)
    #verification_code = Column(Integer)
    #verified = Column(String(10), default='NONE')

    stock = relationship('Match', backref='user',
                         primaryjoin=id == Match.user_id)

class Flight(Base):
    """ SQLAlchemy Flights Base """
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    #creation_date = Column(datetime(timezone=True), default=datetime.datetime.utcnow)
    #flight_num = Column(String(6))
    airport = Column(String(3))
    flight_date =  Column(Integer)
    departure_time = Column(Integer)


    stock = relationship('Match', backref='flight',
                         primaryjoin=id == Match.flight_id)


# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()


# test_user1 = User(id=1, uni='test100', max_passengers = 2, phone_number = "100000001")
# test_user2 = User(id=2, uni='test101', max_passengers = 1, phone_number = "100000002")
# test_user3 = User(id=3, uni='test102', max_passengers = 2, phone_number = "100000003")
# test_user4 = User(id=4, uni='test103', max_passengers = 2, phone_number = "100000004")
# print ("hello")

# test_flight1 = Flight(id=0, airport = 'JFK', flight_date = 10312018, departure_time = 122800)
# test_flight2 = Flight(id= 1, airport = 'JFK', flight_date = 10312018, departure_time = 123000)
# test_flight3 = Flight(id=2, airport = 'LGA', flight_date = 12252018, departure_time = 124500)
# test_flight4 = Flight(id=3, airport = 'LGA', flight_date = 12252018, departure_time = 100000)
# test_flight5 = Flight(id=4, airport = 'LGA', flight_date = 12252018, departure_time = 100000)

# session.add(test_user1)
# session.add(test_user2)
# session.add(test_user3)
# session.add(test_user4)
# session.add(test_flight1)
# session.add(test_flight2)
# session.add(test_flight3)
# session.add(test_flight4)
# session.add(test_flight5)

# session.commit()
