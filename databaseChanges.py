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

if __name__ == '__database__':
    app.run(Debug=True)
