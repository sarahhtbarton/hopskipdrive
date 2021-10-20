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


def create_ride(start_address, end_address):
    """Create and return a new ride."""

    ride = Rides(start_address=start_address,
                     end_address=end_address)
    
    db.session.add(ride)
    db.session.commit()

    return ride


if __name__ == '__main__':
    from server import app
    connect_to_db(app)