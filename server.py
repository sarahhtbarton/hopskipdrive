"""Server for HopSkipDrive Challenge."""

from flask import Flask, render_template, request, session, flash, redirect
import requests
from jinja2 import StrictUndefined
from model import connect_to_db, db, Drivers, Rides
import crud
from math import trunc
# from driver_service import get_rides()


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = 'AIzaSyC2PdjW1EgQRKkIYXyL-IZdp7I3XdlberY'


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('login.html')


@app.route("/login", methods=['POST'])
def handle_login():
    """Action for login form; log a user in."""

    username = request.form.get('username')
    password = request.form.get('password')

    driver = Drivers.query.filter_by(email=username).first()

    if driver:
        if password == driver.password:
            session['driver_full_name'] = driver.full_name
            session['driver_email'] = driver.email
            session['driver_id'] = driver.driver_id
            return redirect('/rides')    
        else:
            flash('Email and password do not match. Try again.')
            return redirect ('/')
    else:
        flash('No driver with that email. Please create a new profile.')
        return render_template('signup.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    """Create a new user profile."""

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        home_address = request.form.get('address')

        driver = Drivers.query.filter_by(email=email).one()

        if driver:
            flash('Account already created with that email. Please login or try another email.')
            return redirect('/')

        else:
            crud.create_driver(full_name, email, password, home_address)
            flash('Account created! Please log in.')
            return redirect('/')
    
    elif request.method == 'GET':
        return redirect('/rides')


@app.route("/logout")
def logout():
    """Log out the current user and delete session information"""

    try:
        del session['driver_full_name']
        del session['driver_email']
        del session['driver_id']
    except KeyError:
        pass
    flash("You are logged out.")
    return redirect("/")


@app.route('/rides')
def rides():
    """View ranked rides."""

    driver_address = crud.get_driver(session['driver_id'])
    all_rides = Rides.query.all()

    drivers_rides = {}

    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

    for record in all_rides:
        
        #assemble api request
        parameters = {
            'origin': f"place_id:{driver_address.home_address}",
            'waypoints': f"place_id:{record.start_address}",
            'destination': f"place_id:{record.end_address}",
            'key': API_KEY
        }

        #make api request
        response = requests.get(endpoint, parameters)
        dict_response = response.json()

        #unpack api response
        ride_distance = float((dict_response['routes'][0]['legs'][1]['distance']['text'])[:-3])
        ride_duration = float((dict_response['routes'][0]['legs'][1]['duration']['text'])[:-5])
        commute_duration = float((dict_response['routes'][0]['legs'][0]['duration']['text'])[:-5])
        
        #calculated fields from unpacked api
        earnings = (ride_distance * .5) + (ride_duration * 15/60) #turn into own function
        score = trunc(earnings / (commute_duration + ride_duration) * 100) #turn into own function

        #add data to dictionary in order to pass needed fields to table in rides.html
        drivers_rides[score] = {}
        drivers_rides[score]['earnings'] = earnings
        drivers_rides[score]['start_address'] = dict_response['routes'][0]['legs'][1]['start_address']
        drivers_rides[score]['end_address'] = dict_response['routes'][0]['legs'][1]['end_address']

    #sort dictionary by score, descending
    scores = dict(sorted(drivers_rides.items(), key=lambda kv: kv[0], reverse=True))

    return render_template("rides.html",
                           scores=scores)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True) 