"""Server for HopSkipDrive Challenge."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
import requests
from jinja2 import StrictUndefined
from model import connect_to_db, Drivers, Rides
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['GOOGLE_MAPS_KEY']


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/rides')
def rides():
    """View ranked rides."""

    full_name = request.form.get('full-name')
    driver_address = db.session.query(Drivers.home_address).filter_by(full_name=full_name).one()

    all_rides = Rides.query.all()

    drivers_rides = {}
    for record in all_rides:
        drivers_rides[record.ride_id] = {}
        drivers_rides[record.ride_id]['driver_address'] = driver_address.home_address
        drivers_rides[record.ride_id]['start_address'] = record.start_address
        drivers_rides[record.ride_id]['end_address'] = record.end_address



    # url = f"https://maps.googleapis.com/maps/api/directions/json?\
    #             origin=place_id:{drivers_rides[1]['driver_address']}&\
    #             waypoint=place_id:{drivers_rides[1]['start_address']}&\
    #             destination=place_id:{drivers_rides[1]['end_address']}&\
    #             key={API_KEY}"

    # response = requests.get(url)
    # return response.json()      # does .load() to response to make it a python dictionary



    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

    parameters = {
        'origin': f"place_id:{drivers_rides[1]['driver_address']}",
        'waypoint': f"place_id:{drivers_rides[1]['start_address']}",
        'destination': f"place_id:{drivers_rides[1]['end_address']}",
        'key': API_KEY
    }


    response = requests.get(endpoint, parameters)
    print(response.url) #just prints out the url string with all the parameters included
    print(response.json())
    
    return response.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 