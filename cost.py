import json
import requests


def get_cost(location, num_passengers):
    """ Provides Skybot with Lyft cost from Columbia to needed airport

    Args:
        location (str): JFK, LGA, or EWR
        num_passengers (int): number of passengers

    Return:
        cost (str): cost of the lyft ride
    """
    # Gets the cost of a Lyft from Columbia to JFK Airport
    jfk = requests.get('https://api.lyft.com/v1/cost?start_lat=40.8075&start_lng=-73.9626&end_lat=40.6413&end_lng=-73.7781')
    jfk_json = json.loads(jfk.text)

    # Gets the cost of a Lyft from Columbia to La Guardia Airport (LGA)
    lga = requests.get('https://api.lyft.com/v1/cost?start_lat=40.8075&start_lng=-73.9626&end_lat=40.7769&end_lng=-73.8740')
    lga_json = json.loads(lga.text)

    # Gets cost of a Lyft from Columbia to Newark International Airport (EWR)
    ewr = requests.get('https://api.lyft.com/v1/cost?start_lat=40.8075&start_lng=-73.9626&end_lat=40.6895&end_lng=-74.1745')
    ewr_json = json.loads(ewr.text)

    # Returns the cost of the ride based on the passed airport location
    if location.upper() == "JFK":
        jfk_cost = '%.2f' % ((jfk_json['cost_estimates'][1]['estimated_cost_cents_max']/100) / num_passengers)
        cost = '$'+str(jfk_cost)
    if location.upper() == "LGA":
        lga_cost = '%.2f' % ((lga_json['cost_estimates'][1]['estimated_cost_cents_max']/100) / num_passengers)
        cost = '$'+str(lga_cost)
    if location.upper() == "EWR":
        ewr_cost = '%.2f' % ((ewr_json['cost_estimates'][1]['estimated_cost_cents_max']/100) / num_passengers)
        cost = '$'+str(ewr_cost)

    return cost
