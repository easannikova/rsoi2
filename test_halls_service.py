import unittest
import json
from flask import request
import pytest
import flask

from halls_service import db_conn
from halls_service import affected_num_to_code
from halls_service import get_halls
from halls_service import get_hall
from halls_service import post_hall
from halls_service import delete_hall
from halls_service import put_hall

from halls_service import app

#app = flask.Flask(__name__)

#test db connection
def test_db_conn():
    con = db_conn()
    assert con.closed == 0

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
        
    def test_get_halls(self):
        with app.test_request_context():
            # mock object
            resp = get_halls()
            #print(resp.json["halls"][0])
            halls = resp.json["halls"]
            count = len(halls)
            self.assertEqual(count, 3)
            '''hall1 = halls[2]

            m1 = {'floor': 3,"is3d": True, "number": 6666, "id": 1, "seats_count": 100}
            self.assertEqual(sorted(hall1.items()), sorted(m1.items()))'''
    
    def test_get_hall(self):
        with app.test_request_context():
            # mock object
            resp = get_hall(1)
            hall = resp.json["hall"]
            m1 = {'floor': 3,"is3d": True, "number": 6666, "id": 1, "seats_count": 100}

            self.assertEqual(sorted(hall.items()), sorted(m1.items()))

    def test_put_hall(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.put('/api/1.0/halls/1', json = {'number': 6666})
            res = resp.json["Result of updating"]

            self.assertEqual(res, 'Succes')
    

    def test_1post_hall(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            m1 = {"number": 43, "id": 10}
            resp = client.post('/api/1.0/halls', json = m1)
            print(resp.json)
            hall = resp.json["New hall"]
            self.assertEqual(sorted(hall.items()), sorted(m1.items()))

    def test_2delete_hall(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.delete('/api/1.0/halls/10')
            print(resp)
            res = resp.json["Result of deleting"]

            self.assertEqual(res, 'Succes')




if __name__ == '__main__':
      unittest.main()

