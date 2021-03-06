""" Models for HopSkipDrive app. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Drivers(db.Model):
    """Drivers"""

    __tablename__ = 'drivers'

    driver_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    home_address = db.Column(db.String)

    def __repr__(self):
        """Show info about Drivers"""
        return f"<Drivers driver_id={self.driver_id} email={self.email}>"


class Rides(db.Model):
    """Rides"""

    __tablename__ = 'rides'

    ride_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    start_address = db.Column(db.String)
    end_address = db.Column(db.String)
    ride_distance = db.Column(db.Float)
    ride_duration = db.Column(db.Float)

    def __repr__(self):
        """Show info about Rides"""
        return f"<Rides ride_id={self.ride_id} start_address={self.start_address} end_address={self.end_address}>"


class Commutes(db.Model):
    """Commute times for a driver's potential rides"""

    __tablename__ = 'commutes'

    commute_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True
                          )
    driver_id = db.Column(db.Integer,
                          db.ForeignKey('drivers.driver_id')
                         )
    ride_id = db.Column(db.Integer,
                        db.ForeignKey('rides.ride_id')
                       )
    commute_duration = db.Column(db.Float)
    
    rides = db.relationship('Rides', backref='commute')
    drivers = db.relationship('Drivers', backref='commute')

    def __repr__(self):
        """Show info about Commutes"""
        return f"<Commutes commute_id={self.commute_id} commute_duration={self.commute_duration}>"


def connect_to_db(flask_app,
                  db_uri='postgresql:///hopskipdrive',
                  echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)