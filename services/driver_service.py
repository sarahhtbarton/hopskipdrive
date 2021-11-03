"""Logic for driver routes"""

import requests
import json
from math import trunc

API_KEY = 'AIzaSyC2PdjW1EgQRKkIYXyL-IZdp7I3XdlberY'


def assemble_api_request(origin, waypoints, destination):
    """assemble request for google directions api"""

    parameters = {
        'origin': f"place_id:{origin}",
        'waypoints': f"place_id:{waypoints}",
        'destination': f"place_id:{destination}",
        'key': API_KEY #where do you put API Key?
    }
    
    return parameters


def make_api_request(endpoint, parameters):
    """Make api request to google directions api, """

    response = requests.get(endpoint, parameters)
    dict_response = response.json()

    return dict_response


def unpack_api_response(dict_response):
    """Unpack api responses"""

    ride_distance = float((dict_response['routes'][0]['legs'][1]['distance']['text'])[:-3])
    ride_duration = float((dict_response['routes'][0]['legs'][1]['duration']['text'])[:-5])
    commute_duration = float((dict_response['routes'][0]['legs'][0]['duration']['text'])[:-5])
    start_address = dict_response['routes'][0]['legs'][1]['start_address']
    end_address = dict_response['routes'][0]['legs'][1]['end_address']

    return ride_distance, ride_duration, commute_duration, start_address, end_address


def calculate_earnings(ride_distance, ride_duration):
    """Calculate driver earnings for a given ride"""

    earnings = (ride_distance * .5) + (ride_duration * 15/60)

    return earnings


def calculate_score(earnings, commute_duration, ride_duration):
    """Calculate score (out of 100) of a given ride"""

    score = trunc(earnings / (commute_duration + ride_duration) * 100)

    return score


def populate_driver_rides_dict(drivers_rides, score, earnings, start_address, end_address):
    """Populate dictionary with information for driver about available rides"""

    drivers_rides[score] = {}
    drivers_rides[score]['earnings'] = earnings
    drivers_rides[score]['start_address'] = start_address
    drivers_rides[score]['end_address'] = end_address

    return drivers_rides


def sort_dictionary(drivers_rides):
    """Sort dictionrary by score, descending"""

    scores = dict(sorted(drivers_rides.items(), key=lambda kv: kv[0], reverse=True))

    return scores


def convert_dict_to_json(dict):
    """Conver dictionary into json object"""

    json_scores = json.dumps(dict)

    return json_scores

