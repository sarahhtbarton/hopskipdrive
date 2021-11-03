"""CRUD operations."""

from model import db, connect_to_db, Drivers, Rides


def create_driver(full_name, email, password, home_address):
    """Create and return a new driver."""

    driver = Drivers(full_name=full_name,
                     email=email,
                     password=password,
                     home_address=home_address)
    
    db.session.add(driver)
    db.session.commit()

    return driver


def get_driver_address(primary_key):
    "Return driver home address by primary key"

    driver = db.session.query(Drivers).filter_by(driver_id=primary_key).one()

    return driver.home_address


def create_ride(start_address, end_address):
    """Create and return a new ride."""

    ride = Rides(start_address=start_address,
                     end_address=end_address)
    
    db.session.add(ride)
    db.session.commit()

    return ride


def get_rides():
    """Return all rides"""

    return Rides.query.all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)