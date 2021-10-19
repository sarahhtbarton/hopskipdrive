"""CRUD operations."""

from model import db, connect_to_db, #CLASSES FROM MODEL.PY GO HERE


#CRUD functions go here


if __name__ == '__main__':
    from server import app
    connect_to_db(app)