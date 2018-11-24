import sys
sys.path.append('Skybot/')
from databaseChanges import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import sqlalchemy

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tester1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///tester1.db')
Session = sessionmaker(bind=engine)
session = Session()

db.drop_all()
db.create_all()

person = User(uni="Em231")
person1 = User(uni="Jo432")

flt1 = Flight(flight_num="Delta1")
flt2 = Flight(flight_num="Delta2")
flt3 = Flight(flight_num="Delta3")

mat1 = Match(id=1, flight_id=flt1.id, user_id=person.id, quantity=20)
person.stock.append(mat1)
flt1.stock.append(mat1)

mat2 = Match(id=2, flight_id=flt3.id, user_id=person.id, quantity=10)
person.stock.append(mat2)
flt3.stock.append(mat2)

mat3 = Match(id=3, flight_id=flt1.id, user_id=person1.id, quantity=40)
person1.stock.append(mat3)
flt1.stock.append(mat3)

session.add_all([person, person1, flt1, flt2, flt3])
session.commit()

# Get all flights a user belongs to
for p in session.query(User).all():
    print (p.uni)
    for a in p.stock:
        print (session.query(Flight).filter_by(id=a.flight_id).all())

# Get all users that belong to a flight
for c in session.query(Flight).all():
    print (c.flight_num)
    for a in c.stock:
        print (session.query(User).filter_by(id=a.user_id).all())
