"""Server for HopSkipDrive Challenge."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
import requests
from jinja2 import StrictUndefined
from model import connect_to_db, db, Drivers, Rides
import crud


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
        print('******* DICT RESPONSE *********')
        print(dict_response)

        drivers_rides[record.ride_id] = {}
        drivers_rides[record.ride_id]['leg1'] = {}
        drivers_rides[record.ride_id]['leg1']['start_address'] = dict_response['routes'][0]['legs'][0]['start_address']
        drivers_rides[record.ride_id]['leg1']['end_address'] = dict_response['routes'][0]['legs'][0]['end_address']
        drivers_rides[record.ride_id]['leg1']['distance'] = dict_response['routes'][0]['legs'][0]['distance']['text']
        drivers_rides[record.ride_id]['leg1']['duration'] = dict_response['routes'][0]['legs'][0]['duration']['text']
        drivers_rides[record.ride_id]['leg2'] = {}
        drivers_rides[record.ride_id]['leg2']['start_address'] = dict_response['routes'][0]['legs'][1]['start_address']
        drivers_rides[record.ride_id]['leg2']['end_address'] = dict_response['routes'][0]['legs'][1]['end_address']
        drivers_rides[record.ride_id]['leg2']['distance'] = dict_response['routes'][0]['legs'][1]['distance']['text']
        drivers_rides[record.ride_id]['leg2']['duration'] = dict_response['routes'][0]['legs'][1]['duration']['text']
    
    return render_template("rides.html",
                           drivers_rides=drivers_rides)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True) 