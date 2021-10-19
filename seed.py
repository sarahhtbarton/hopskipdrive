"""Script to seed a database"""

import os
import crud
import model 
import server
import csv


def seed_drivers():
    """Seed Drivers table"""

    with open('data/drivers.csv', newline='') as drivers_csv:
        drivers_reader = csv.DictReader(drivers_csv)
        for row in drivers_reader:
            crud.create_driver(row['full_name'], 
                            row['place_id'])


def seed_rides():
    """Seed Riders table"""

    with open('data/rides.csv', newline='') as rides_csv:
        rides_reader = csv.DictReader(rides_csv)
        for row in rides_reader:
            crud.create_ride(row['start_address'], 
                            row['end_address'])


def create_example_data():
    seed_drivers()
    seed_rides()


if __name__ == '__main__':
    os.system('dropdb hopskipdrive-if-exists')
    os.system('createdb hopskipdrive')
    model.connect_to_db(server.app)
    model.db.create_all()
    create_example_data()