from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy
from sqlalchemy import exists
from datetime import datetime


# app = Flask(_name_)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tester.db'


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tester.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///tester.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()


db.metadata.clear()

subs = db.Table('subs',
	db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
	db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id'))
)

class User(db.Model):
	user_id =  db.Column(db.Integer, primary_key = True)
	name =  db.Column(db.String(20))
	subscriptions = db.relationship('Channel', secondary = subs, backref = db.backref('subscribers', lazy = 'dynamic'))

class Channel(db.Model):
	channel_id = db.Column(db.Integer, primary_key = True)
	channel_name =  db.Column(db.String(20))

print ("hello")


user1 = User(name='Anthony')
user2 = User(name='Stacy')
user3 = User(name='George')
user4 = User(name='Amber')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)

channel1 = Channel(channel_name='Pretty Printed')
channel2 = Channel(channel_name='Cat Videos')

db.session.add(channel1)
db.session.add(channel2)

channel1.subscribers.append(user1)
channel1.subscribers.append(user3)
channel1.subscribers.append(user4)

channel2.subscribers.append(user2)
channel1.subscribers.append(user4)

print ("hello")

db.session.commit()

# checking set backreferences
# for user in channel1.subscribers:
# 	print (user.name)

# print (type(channel1.subscribers))
# print (type(Users.name))









