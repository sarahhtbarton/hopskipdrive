"""Server for HopSkipDrive Challenge."""

from flask import Flask, render_template, request, session, flash, redirect
from jinja2 import StrictUndefined
from model import connect_to_db
import crud
import services.driver_service as driver_service


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('login.html')


@app.route("/login", methods=['POST'])
def handle_login():
    """Action for login form; log a user in."""

    email = request.form.get('email')
    password = request.form.get('password')

    driver = crud.get_driver_by_email(email)

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

        driver = crud.get_driver_by_email(email)

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
    """Display ranked rides."""

    driver = crud.get_driver(session['driver_id'])
    all_rides = crud.get_rides()

    drivers_rides = {}

    for ride in all_rides:

        commute = crud.get_or_create_commute(ride, driver)
        earnings = driver_service.calculate_earnings(ride.ride_distance, ride.ride_duration)
        score = driver_service.calculate_score(earnings, commute.commute_duration, ride.ride_duration)
        
        driver_service.populate_driver_rides_dict(drivers_rides, score, earnings, ride.start_address, ride.end_address)

    scores = driver_service.sort_dictionary(drivers_rides)

    json_scores = driver_service.convert_dict_to_json(scores)

    return json_scores

    # return render_template("rides.html",
    #                        scores=scores)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True) 