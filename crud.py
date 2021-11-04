"""CRUD operations."""

from model import db, connect_to_db, Drivers, Rides, Commutes
from configuration.api_key import API_KEY
import requests


def create_driver(full_name, email, password, home_address):
    """Create and return a new driver."""

    driver = Drivers(full_name=full_name,
                     email=email,
                     password=password,
                     home_address=home_address)
    
    db.session.add(driver)
    db.session.commit()

    return driver


def get_driver(primary_key):
    "Return driver by primary key"

    return db.session.query(Drivers).filter_by(driver_id=primary_key).one()


def get_driver_by_email(email):
    """Return driver by email"""

    return db.session.query(Drivers).filter_by(email=email).first()


def create_ride(start_address, end_address, ride_distance, ride_duration):
    """Create and return a new ride."""

    ride = Rides(start_address=start_address,
                 end_address=end_address,
                 ride_distance=ride_distance,
                 ride_duration=ride_duration
                )
    
    db.session.add(ride)
    db.session.commit()

    return ride


def get_rides():
    """Return all rides"""

    return Rides.query.all()


def create_commute(driver_id, ride_id, commute_duration):
    """Create and return commute"""

    commute = Commutes(driver_id=driver_id,
                       ride_id=ride_id,
                       commute_duration=commute_duration
                      )
    db.session.add(commute)
    db.session.commit()

    return commute


def get_or_create_commute(ride, driver):
    """Get commute from or create in database"""

    commute_check = db.session.query(Commutes).filter(Commutes.ride_id == ride.ride_id, Commutes.driver_id == driver.driver_id).first()
        
    if commute_check:
        commute = get_commute(commute_check.commute_id)
    else:
        commute = make_commute_request(driver, ride)
    
    return commute


def make_commute_request(driver, ride):
    """Computes commute for given driver and ride"""

    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

    parameters = {
        'origin': f"place_id:{driver.home_address}",
        'destination': f"place_id:{ride.start_address}",
        'key': API_KEY
    }
    
    response = requests.get(endpoint, parameters)
    dict_response = response.json()

    commute_duration = float((dict_response['routes'][0]['legs'][0]['duration']['text'])[:-5])

    commute = create_commute(driver.driver_id, ride.ride_id, commute_duration)

    return commute


def get_commutes():
    """Return all commutes"""

    return Commutes.query.all()


def get_commute(primary_key):
    "Return commute by primary key"

    return db.session.query(Commutes).filter_by(commute_id=primary_key).one()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)