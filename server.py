"""Server for HopSkipDrive Challenge."""

from flask import Flask, render_template, request, session, flash, redirect
from jinja2 import StrictUndefined
from model import connect_to_db, db, Drivers, Rides
import crud
import services.driver_service as driver_service


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#delete from here and put in driver_service.py??
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

    driver_address = crud.get_driver_address(session['driver_id'])
    print(driver_address)
    all_rides = crud.get_rides()

    drivers_rides = {}

    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

    for ride in all_rides:

        parameters = driver_service.assemble_api_request(driver_address, ride.start_address, ride.end_address)
        
        dict_response = driver_service.make_api_request(endpoint, parameters)

        ride_distance, ride_duration, commute_duration, start_address, end_address = driver_service.unpack_api_response(dict_response)

        earnings = driver_service.calculate_earnings(ride_distance, ride_duration)
        
        score = driver_service.calculate_score(earnings, commute_duration, ride_duration)

        driver_service.populate_driver_rides_dict(drivers_rides, score, earnings, start_address, end_address)

    scores = driver_service.sort_dictionary(drivers_rides)

    json_scores = driver_service.convert_dict_to_json(scores)

    return render_template("rides.html",
                           scores=scores)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True) 