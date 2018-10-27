from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security  import generate_password_hash, check_password_hash
import sqlite3
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(50))
    uni = db.Column(db.String(7), unique = True)
    max_passengers = db.Column(db.Integer)
    phone_number = db.Column(db.String(50), unique = True)
    verification_code = db.Column(db.Integer)
    verified = db.Column(db.Boolean, default=False)
    flights = db.relationship('Flight', backref='flyer')

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    airport = db.Column(db.String(3))
    flight_date =  db.Column(db.String(10))
    departure_time = db.String(10)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airport = db.Column(db.String(3))
    depature_time = db.Column(db.String(3))
    flight_date = db.Column(db.String(10))
    flights = db.relationship('Flight', backref='riders')


if __name__ == '__database__':
    app.run(Debug=True)
