import unittest
import json
from flask import request
import pytest
import flask

from sevrer import app_change_hall
from sevrer import app_change_movie
from sevrer import app_get_ext_info
from sevrer import affected_num_to_code

from sevrer import app

def test_affected_num_to_code():
    code1 = affected_num_to_code(0)
    assert code1 == 404
    code2 = affected_num_to_code(3)
    assert code2 == 200

class TestFunctions(unittest.TestCase):
    def setup(self):
        app.config['TESTING'] = True
        #self.app = app.test_client()
        # Test of Output function

    def test_change_hall(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.put('/api/1.0/halls/1', json = {'new_number': 6666})
            res = resp.json["Result of updating"]

            self.assertEqual(res, 'Succes')
    

    def test_change_movie(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.put('/api/1.0/movies/1', json = {'new_title': 'Mirror'})
            res = resp.json["Result of updating"]

            self.assertEqual(res, 'Succes')

    def test_get_ext_info(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.get('/api/1.0/seanses/1')
            seanse = resp.json["Extended info about seanse"]
            s1 = {'FC': 18, 'floor': 3, 
                'hall_number': 6666, 'id': 1, 'movie_title': 'Wildp                                             '}

            self.assertEqual(sorted(seanse.items()), sorted(s1.items()))




if __name__ == '__main__':
      unittest.main()

