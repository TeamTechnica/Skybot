# SkyBot

Contributors: @joicodes, @lesley2958, @MJDev, @KlarizsaPadilla

## About SkyBot

SkyBot is an SMS chat bot that allows traveling Columbia students to share rides to the airport, matching them with other students going to the same airport at the same time. Currently, Columbia students have a designated Facebook Group called Columbia / Barnard Airport Cab Sharing, where they post their travel itineraries in hopes of connecting  with someone who has a similar flight departure time, in an effort to split a cab fare to save money. In New York City, cab fare to airports can be as high as $100 depending on the number of riders, transportation peak hours, and weather inclemation. SkyBot is a cost effective solution that addresses these pain points.

Using our matching algorithm, SkyBot accurately matches students with the closest travel itineraries and shared preferences! With API integrations, including Twilio, SendGrid, and Lyft students can easily:

- Estimate transportation cost
- Receive their matches'contact information via text message
- Receive a recommended departure time based on riders' flights

SkyBot aims to provide a simple user interface to connect people in order to make the process of getting to your desired destination less of a hassle.


## How to use SkyBot

With Skybot, it is easy to find your next rideshare to the airport. Just following the steps below:
1. Text Skybot "hello" or any other greeting of your choice at 667-401-4282
2. Skybot will then prompt you for your Columbia uni-- please respond with your Columbia uni.
3. Skybot then emails your uni email a verification code. Please respond with that verification code.
4. Upon having your uni verified, please provide the flight details Skybot requests, in the form she requests.
5. Lastly, if there are matches for your rideshare, Skybot will share the uni's of the passengers on your ride. Otherwise, Skybot will keep your information on file in case someone with similar flight details as you, is later looking for a flight.


## Structure

```bash
├── .gitignore                    # Ignore unneeded Python files
├── .pylintrc                     # Python lint configuration
├── .travis.yml                   # CI Configuration
├── .pre-commit-config.yaml       # Precommit File
├── .coveragerc                   # Coverage Information
├── CONTRIBUTING.md               # Guide to adding to SkyBot
├── Procfile                      # Used when deploying the bot to production
├── README.md                     # This file
├── app.py                        # The main bot code
├── config.py                     # Database Configurations
├── database.py                   # Contains database schemas
├── manage.py                     # Database Managemenet
├── match.py                      # Contains matching algorithm
├── requirements.txt              # Libraries used to build the bot
├── runtime.txt                   # Python configuration for Heroku
├── nose.cfg             		  # TO DO
├── test/                         # All supporting code used by app.py
    ├── test_app.py               # TO DO
    ├── test_databases.py         # TO DO
├── coverage_docs/				  # TO DO
├── migrations/		     		  # TO DO
├── submissions/				  # TO DO
```


## Technology Stack

- Development Framework: Python (Flask)
- Unit Testing Tool: PyUnit
- Static Analysis Tool: PyLint
- Build Tool: Travis CI
- Continuous Integration Tool: Travis CI
- Data Storage: PostgreSQL
- VersionControl: Github
- Cloud Platform: Heroku
- APIs: Twilio, SendGrid, Lyft Fare Estimator


## Connecting to Twilio

We used Twilio’s Programmable SMS to set this up as an SMS service. Specifically, we wrote a function that will communicate with the Twilio API to provide a response, `sms_reply()`. For this function we use the `route()` decorator to tell Flask which URL should trigger this function.

``` python
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
```

This function is triggered whenever a message is sent to our Twilio number. With `requests.values.get`, we retrieve several attributes associated with the message received from a user, including their phone number. To indicate this, we made the first parameter `From`; this yields a result in the format “+1XXXXXXXXXX.”

``` python
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('From', None)
```


## Matching Algorithm

The matching algorithm takes four criteria when considering matches: 

1. The location of departure, i.e. JFK vs LGA vs EQR
2. The date of departure
3. The time of departure
4. The number of passengers


## Data Models

### User

| Attribute | Type |
| --------- | ----------- |
| id | Integer |
| UNI | String |
| max_passengers | Integer |
| phone_number | String | 
| flights | relationship |
| verification_code | Integer |
| verified | String |

### Flight

| Attribute | Type |
| --------- | ----------- |
| id | Integer |
| airport | String |
| flight_date | Integer |
| departure_time | Integer | 
| passenger_id | Integer |
| match_id | Integer |

### Match

| Attribute | Type |
| --------- | ----------- |
| id | Integer |
| airport | String |
| ride_date | Integer |
| ride_departureTime | Integer | 
| flights | relationship |
| available_seats | Integer |
| riders | relationship |
