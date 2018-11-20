from app import *
from database import *
import sys
sys.path.append('Skybot/')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

engine = create_engine('sqlite:///site.db')
Session = sessionmaker(autoflush=True, autocommit=False, bind=engine)
conn = engine.connect()
session = Session(bind=conn)

sched = BlockingScheduler()

# This job will run every day at midnight
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0)
def clean_database():

    total_flights = 0

    # Gets the current date and time
    current_datetime = datetime.datetime.now()

    #Parses current time into day, month, year, hour, minute
    current_day = current_datetime.day
    current_month = current_datetime.month
    current_year = current_datetime.year
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute


    flights = Flight.query.all()

    # Iterates through array of Flight objects
    
    #for flight in flights: 
        
    #    date = flight.flight_date
    #    time = flight.departure_time

    #    month = int(date[0:2])
    #    day = int(date[2:4])
    #    year = int(date[4:8])

    #    hour = int(time[])
    #    minute = int(time[])

        # Check if the year has passed
    #    if ()
 
    print(total_flights + ' expired flights were removed from the database.')

sched.start()
