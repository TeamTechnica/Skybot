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

    stock = db.relationship('Match', backref='user',
                         primaryjoin=id == Match.user_id)

class Flight(db.Model):
    """ SQLAlchemy Flights Model """
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    flight_num = db.Column(db.String(6))
    airport = db.Column(db.String(3))
    flight_date =  db.Column(db.Integer)
    departure_time = db.Column(db.Integer)


    stock = relationship('Match', backref='flight',
                         primaryjoin=id == Match.flight_id)

if __name__ == '__database__':
    app.run(Debug=True)
