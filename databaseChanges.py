from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import sqlite3
import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
import sys
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


class Flight(db.Model):
    """ SQLAlchemy Flights Model """
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    airport = db.Column(db.String(3))
    flight_date = db.Column(db.Integer)
    departure_time = db.Column(db.Integer)
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), default='NONE')


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    airport = db.Column(db.String(3))
    ride_date = db.Column(db.Integer)
    ride_departureTime = db.Column(db.Integer)
    riders = relationship("Flight", backref="ride")
    ride_passengers = db.Column(db.Integer)


if __name__ == '__databaseChanges__':
    app.run(Debug=True)
