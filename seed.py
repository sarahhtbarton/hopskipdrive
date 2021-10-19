"""Script to seed a database"""

import os
import crud
import model 
import server
import csv


# create seed functions here


def create_example_data():
    # include all above functions here


if __name__ == '__main__':
    os.system('dropdb DATABASENAME-if-exists')
    os.system('createdb DATABASENAME')
    model.connect_to_db(server.app)
    model.db.create_all()
    create_example_data()