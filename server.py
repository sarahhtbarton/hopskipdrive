"""Server for HopSkipDrive Challenge."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
import requests
from jinja2 import StrictUndefined
from model import connect_to_db, db, Drivers, Rides
import crud
from math import trunc


app = Flask(__name__)
# app.secret_key = "dev" #only used for session?
app.jinja_env.undefined = StrictUndefined

API_KEY = 'AIzaSyC2PdjW1EgQRKkIYXyL-IZdp7I3XdlberY'


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/rides')
def rides():
    """View ranked rides."""

    full_name = request.args.get('full-name')
    driver_address = db.session.query(Drivers.home_address).filter_by(full_name=full_name).one()
    all_rides = Rides.query.all()

    drivers_rides = {}

    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

    for record in all_rides:
        parameters = {
            'origin': f"place_id:{driver_address.home_address}",
            'waypoints': f"place_id:{record.start_address}",
            'destination': f"place_id:{record.end_address}",
            'key': API_KEY
        }

        response = requests.get(endpoint, parameters)
        dict_response = response.json()

        ride_distance = float((dict_response['routes'][0]['legs'][1]['distance']['text'])[:-3])
        ride_duration = float((dict_response['routes'][0]['legs'][1]['duration']['text'])[:-5])
        commute_duration = float((dict_response['routes'][0]['legs'][0]['duration']['text'])[:-5])
        earnings = (ride_distance * .5) + (ride_duration * 15/60)
        score = trunc(earnings / (commute_duration + ride_duration) * 100)

        drivers_rides[score] = {}
        drivers_rides[score]['earnings'] = earnings
        drivers_rides[score]['start_address'] = dict_response['routes'][0]['legs'][1]['start_address']
        drivers_rides[score]['end_address'] = dict_response['routes'][0]['legs'][1]['end_address']

    scores = dict(sorted(drivers_rides.items(), key=lambda kv: kv[0], reverse=True))

    print(type(scores))
    print(scores)
    
    return render_template("rides.html",
                           scores=scores)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True) 