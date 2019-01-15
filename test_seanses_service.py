import unittest
import json
from flask import request
import pytest
import flask

from seanses_service import db_conn
from seanses_service import affected_num_to_code
from seanses_service import get_seanses
from seanses_service import get_seanse
from seanses_service import post_seanse
from seanses_service import delete_seanse
from seanses_service import put_seanse

from seanses_service import app

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
        
    def test_get_seanses(self):
        with app.test_request_context():
            # mock object
            resp = get_seanses()
            #print(resp.json["seanses"][0])
            seanses = resp.json["seanses"]
            count = len(seanses)
            self.assertEqual(count, 5)
            seanse1 = seanses[4]
            print(seanse1)
            m1 = {"hall_number": 3, "id": 3, "movie_title": 'Mirror                                            '}
            self.assertEqual(sorted(seanse1.items()), sorted(m1.items()))
    
    def test_get_seanse(self):
        with app.test_request_context():
            # mock object
            resp = get_seanse(3)
            seanse = resp.json["seanse"]
            m1 = {"hall_number": 3, "id": 3, "movie_title": 'Mirror                                            '}

            self.assertEqual(sorted(seanse.items()), sorted(m1.items()))

    def test_put_seanse(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.put('/api/1.0/seanses/3', 
                    json = {'value': 3, 'object': 'hall_number'})
            res = resp.json["Result of updating"]
            self.assertEqual(res, 'Succes')

            resp = client.put('/api/1.0/seanses/3', 
                    json = {'value': 'Mirror', 'object': 'movie_title'})
            res = resp.json["Result of updating"]
            self.assertEqual(res, 'Succes')

    def test_post_seanse(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            m1 = {"hall_number": 10, "id": 10, "movie_title": '99 franks'}
            resp = client.post('/api/1.0/seanses', json = m1)
            print(resp.json)
            seanse = resp.json["New seanse"]
            self.assertEqual(sorted(seanse.items()), sorted(m1.items()))

    def test_delete_seanse(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.delete('/api/1.0/seanses/10')
            print(resp)
            res = resp.json["Result of deleting"]

            self.assertEqual(res, 'Succes')

if __name__ == '__main__':
      unittest.main()
