from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/cost', methods=['POST'])
def cost():
    pickup_location = request.form['airport']
    total_passengers = int(request.form['passengers'])
    jfk = requests.get('https://api.lyft.com/v1/cost?start_lat=40.8075&start_lng=-73.9626&end_lat=40.6413&end_lng=-73.7781')
    jfk_json = json.loads(jfk.text)
    lga = requests.get('https://api.lyft.com/v1/cost?start_lat=40.8075&start_lng=-73.9626&end_lat=40.7769&end_lng=-73.8740')
    lga_json = json.loads(lga.text)
    ewr = requests.get('https://api.lyft.com/v1/cost?start_lat=40.8075&start_lng=-73.9626&end_lat=40.6895&end_lng=-74.1745')
    ewr_json = json.loads(ewr.text)

    if pickup_location.upper() == "JFK":
        jfk_cost = '%.2f' % ((jfk_json['cost_estimates'][1]['estimated_cost_cents_max']/100) / total_passengers)
        return '$'+str(jfk_cost)
    if pickup_location.upper() == "LGA" :
        lga_cost = '%.2f' % ((lga_json['cost_estimates'][1]['estimated_cost_cents_max']/100) / total_passengers)
        return '$'+str(lga_cost)
    if pickup_location.upper() == "EWR" :
        ewr_cost = '%.2f' % ((ewr_json['cost_estimates'][1]['estimated_cost_cents_max']/100) / total_passengers)
        return '$'+str(ewr_cost)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
        app.run(debug=True)

    