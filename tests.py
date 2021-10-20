import unittest
import server
from model import connect_to_db


class FlaskIntegrationTests(unittest.TestCase):
    """Integration Tests -- Testing Flask app/server -- checks routes."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        connect_to_db(server.app, "postgresql:///hopskipdrive")
    
    def test_homepage(self):
        """“Does this URL path map to a route function?”"""
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
    
    def test_get_request(self):
        """“Does this route function return the right HTML?”"""
        result = self.client.get('/rides')
        self.assertIn(b'<th scope="col">Earnings</th>', result.data)
    
    def test_post_form(self):
        result = self.client.post('/signup', data={'full_name': 'Sarah Barton', 'email': 'sarah@gmail.com', 'password': 'password123', 'home_address': 'ChIJKY2A05J9hYAR3ftxkR1ZTho'})
        self.assertIn(b'Sarah Barton', result.data)


if __name__ == "__main__":
    unittest.main()