import unittest
from unittest.case import TestCase
from server import app
import server
from model import Drivers, connect_to_db, db
from seed import create_example_data
from flask import session
import services.driver_service as driver_service


class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""
        result = self.client.get("/")
        self.assertIn(b"Account Sign In", result.data)


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///hopskipdrive", echo=False)
            
        db.create_all()
        create_example_data()

        with self.client as c:             
            with c.session_transaction() as sess:
                sess['driver_full_name'] = "Will Fox"
                sess['driver_email'] = "will@gmail.com"
                sess['driver_id'] = 2

    def tearDown(self):                            
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_rides(self):          
        """Test rides page."""
        
        result = self.client.get("/rides", data={"email": "will@gmail.com", "password": "password123"}, follow_redirects=True)
        self.assertIn(b"earnings", result.data)

    def test_find_driver(self):
        """Can we find a driver in the sample data?"""

        will = Drivers.query.filter(Drivers.full_name == "Will Fox").first()
        self.assertEqual(will.full_name, "Will Fox")

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['driver_email'] = 'will@gmail.com'
                sess['driver_id'] = 2

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'driver_email', session)
            self.assertIn(b'Account Sign In', result.data)


class DriverServiceTests(unittest.TestCase):
    """Driver Service logic unit tests"""

    def test_earnings(self):
        assert driver_service.calculate_earnings(20, 60) == 25
    
    def test_score(self):
         assert driver_service.calculate_score(10, 40, 60) == 10
    
    def test_dict_sort(self):
        assert driver_service.sort_dictionary({1: 'a', 3:'c', 2:'b'}) == {3:'c', 2:'b', 1: 'a'}

    def test_dumps(self):
        assert isinstance(driver_service.convert_dict_to_json({3:'c', 2:'b', 1: 'a'}), str)


class MockAPITests(unittest.TestCase):
    """Flask tests that use the database and mock API call."""

    def setUp(self):
        """Before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///hopskipdrive", echo=False)
              
        db.create_all()
        create_example_data()

        with self.client as c:             
            with c.session_transaction() as sess:
                sess['driver_email'] = "will@gmail.com"
                sess['driver_full_name'] = "Will Fox"
                sess['driver_id'] = 2

        def _mock_get_distance_api(waypoints):
            """Mock test of API call"""

            return {'html_attributions': [], 'result': {"36": {"earnings": 15.0, "start_address": "ChIJOR1geCGHhYARQ484akGas0M", "end_address": "ChIJVVVVVYx3j4ARP-3NGldc8qQ"}, "35": {"earnings": 14.15, "start_address": "ChIJQ-U7wYqAhYAReKjwcBt6SGU", "end_address": "ChIJkeRXUeaFj4ARcJTwcuK8jaY"}, "29": {"earnings": 10.1, "start_address": "ChIJHRGLQeuAhYARm3G81gyW59Y", "end_address": "ChIJ3ygHDwGFhYARNd_3AnMlZsM"}, "19": {"earnings": 5.75, "start_address": "ChIJPwvLyD5-j4AR2fM8C0bbVC8", "end_address": "ChIJo7HdhWKAhYARp5lDOzOnnK0"}, "17": {"earnings": 7.65, "start_address": "ChIJx6E1sUuHj4ARCB_Ub0Lb8fI", "end_address": "ChIJRzfD3i98hYAR7TeEIqsZjys"}, "14": {"earnings": 5.1, "start_address": "ChIJKY2A05J9hYAR3ftxkR1ZTho", "end_address": "ChIJcQMtojp8hYARg3TZouAOzFE"}, "7": {"earnings": 3.0, "start_address": "ChIJ64OBgvGKj4AR3jMzcn9tdWI", "end_address": "ChIJ22W3TsJhhYARGF5WvDq2FhA"}}, 'status': 'OK'}

        server.get_distance_api = _mock_get_distance_api

    def tearDown(self):                            
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

if __name__ == "__main__":
    import unittest

    unittest.main()