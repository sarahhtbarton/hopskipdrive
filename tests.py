import unittest
from server import app
import server
from model import Drivers, connect_to_db, db
from seed import create_example_data
from flask import session


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

    def test_new_users(self):
        """Test user profile creation page."""
        result = self.client.get('/signup', follow_redirects=True)
        self.assertIn(b"Account Information", result.data)


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

    def tearDown(self):                            
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_rides(self):          
        """Test rides page."""
        result = self.client.get("/rides")
        self.assertIn(b"Earnings", result.data)

    def test_find_driver(self):
        """Can we find a driver in the sample data?"""

        will = Drivers.query.filter(Drivers.full_name == "Will Fox").first()
        self.assertEqual(will.full_name, "Will Fox")

    def test_rides_page(self):               
        """Test ride view page."""

        result = self.client.get("/rides", data={"username": "will@gmail.com", "password": "password123"},
                              follow_redirects=True)
        self.assertIn(b"Score", result.data)

    def test_login(self):                         
        """Test log in form."""

        result = self.client.post("/login", data={'username': 'will@gmail.com', 'password': 'password123'}, follow_redirects=True)
        self.assertIn(b"Welcome Will", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['driver_email'] = 'will@gmail.com'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'driver_email', session)
            self.assertIn(b'Account Sign In', result.data)


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

        def _mock_get_distance_api(waypoints):
            """Mock test of API call"""

            return {'html_attributions': [], 'result': {'formatted_address': '1515 Keats Ave N, Lake Elmo, MN 55042, USA', 'name': 'Lake Elmo Park Reserve', 'photos': [{'height': 1731, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113941198282368414473">Lake Elmo Park Reserve</a>'], 'photo_reference': 'ATtYBwKvFPmxDJU48oKGydyRAP1_LT1v-Ui6RMXtb59LFzfUEL51BU2RjmcBUD96wMWk4kgrqXQC5oQ0QDFx6WhS2wF_3sNSM4gsZ35NareAdh0UfJ2KEF7zeBvQBgZHFfgyIalUvm6I-t-xm_xaQ7ISK0uEgugL36WcmUuRM-dcds5JF03X', 'width': 2600}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109627993211852364929">Andrew Gontarek</a>'], 'photo_reference': 'ATtYBwKoEPsi6yzM35cIKvqgAPcduf2tEEpxKjPainbYTKSMt8v4WIIFwhFD2Wv4FSJSbi0d4tVHwMWLURhUzjoBsye4F-69DJLfpcMiIy2A8qUMVwz31jX0_ip_Q8JrOLqnU6m5I64Tbv9Fluu3vmUuNYVCCxfzphnDbABPNyRBcECUPNXJ', 'width': 4032}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104646741841860661226">Yazmin Reyes</a>'], 'photo_reference': 'ATtYBwJgBBWPSE_DvP250v7FpwNYDOIb-ZWKLdHuroCklaeIYwGOimr_zSUXikgunm8lvWcoOZ9H0aYRcuV5jdk0S4_68E5rwCSvswhVKM6ib-DLSLiOgHKTxYFfRV5xm3UqGI4E0pZarnf-XKWrcxbOJaBPBy077t5YuswmC6eEzbfWQhzl', 'width': 3024}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117000989128220333729">Alison Bowker</a>'], 'photo_reference': 'ATtYBwIjTYxnt4h2Ke0zMDbmIJNEiEceeY1D0sEdlxb6OwH5buANMdvB9ibRKPMC1Q6SZdfwgZZmptyo8rkvG1ufQj8i7PcmlTLqdKgNg5OUw0Ylxmu6wx5bLQM00FWEsMN8YGtkHVD0oPtrChxZPRj0ymVpYfsqOOwq8SS185bbyJN5OefI', 'width': 4032}, {'height': 3583, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112582953006911993341">Leah Charlsen</a>'], 'photo_reference': 'ATtYBwILE1DuH2A7sDYUpDd7eFTTrdXdYy9tmnNAvvbFZYPYnX4NCz_755OCQWQ_535xwNJ4WbN40acP92a12r0-CZdemuUWjFapLc_PyymGNGJKJji4IlNnQVOzJg2wxKlLSRFkrTUdKXoIugaZ9rR__1q-XsNV_b5TXw7Or5NwNo1OoTTY', 'width': 1908}, {'height': 3456, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/102974591944691502780">Lizabeth Kyser</a>'], 'photo_reference': 'ATtYBwLh-UC-AbkcAMXpN_rMR1eeErSz5wVnhT6xwXa7hTgckpHUS1JHPlmrQqwPv0Fs9zgPvms3iWL07Q0oYY_Sa6vA-pyfDrWG07E7hyAx4alfwqfUmIKd5MF7b9MTEOWy_ccgkogONsl76640XUIi3pzifRVL9NwoGeGMVG9Pm3AzwBTr', 'width': 4608}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111658228381463654223">Aaron Bolduc</a>'], 'photo_reference': 'ATtYBwKgt_wSlKL2v-3vHM_Mza_8_IxG1JoQMUrBErnMVTMHeNSG_zkBKQWG_LfuMhVOgKXQ93cMtoM568DkRi5Hf34erhS9gkvH4bWK4qiMGI0Xo2816JeDlVIaUkHU-ZjbfDiHjV78rwdx_3MrTNS08M5h2ZeHNXqC4gTGungxFrUD5SR7', 'width': 4032}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104183341438553618909">Ken Boyd</a>'], 'photo_reference': 'ATtYBwIR4myfVaiMDj4TyBNn4eYw73z5GsbX4z79lv-sbzKuQ3SKaoUvjYYrDO6OaPwsvfDQwVD3Xyx1ag1mpe--MJO4qdd2YcF1JhDoN5fF6iK0tBXOhK_SQ6ZrRaIHNNPvYE4h-Xkw9-dQmQoC2rUwn2YT1y3DXF5P2PDgCbolMdk0Ggt_', 'width': 3024}, {'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111658228381463654223">Aaron Bolduc</a>'], 'photo_reference': 'ATtYBwIueZUj9Ei0q8lvC3B813wo3igQIylOB61G04syrOe1ZeS12SBBJtLi2k7UelP2eZ00UOm8A60X1wAwuo3ihXmDvLYsNlIcXn__F1fFkG9yD--x58zFZKPVpVUZ4jP6AgtPJeUCQrOgZgIvTy8jAR5QMaN8QRILQrF8FdfuY0jQUmwO', 'width': 4032}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113668662980540441669">Mari Boyd</a>'], 'photo_reference': 'ATtYBwLGZmaf0axPkbxRuAjGVzSgt1z4A2Jqn3lz5LXQO-e5kNSB032N0RkW84E4QD-wtCkxVrk5F-ArCZG7KyyQSQRh37MmJeIja69iZBB0UgUtQYY_b8z4MdCuQDTCKEG7YG-V2U-yH5K6ej3OHkXNIm0fbRPuDq8j2pvEDLWRhW_PbXY', 'width': 3024}]}, 'status': 'OK'}

        server.get_distance_api = _mock_get_distance_api

    def tearDown(self):                            
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

if __name__ == "__main__":
    import unittest

    unittest.main()