"""Logic for driver routes"""

from math import trunc
import json


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