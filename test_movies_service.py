import unittest
import json
from flask import request
import pytest
import flask

from movies_service import db_conn
from movies_service import affected_num_to_code
from movies_service import get_movies
from movies_service import get_movie
from movies_service import post_movie
from movies_service import delete_movie
from movies_service import put_movie

from movies_service import app

#app = flask.Flask(__name__)
m_url = "http://localhost:5000/api/1.0/movies"

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
        
    def test_get_movies(self):
        with app.test_request_context():
            # mock object
            resp = get_movies()
            #print(resp.json["movies"][0])
            movies = resp.json["movies"]
            count = len(movies)
            self.assertEqual(count, 3)
            movie1 = movies[1]

            m1 = {'FC': 16,"country": "Russia", "genre": 'thriller', "id": 1, "rating": 5, 
                    "title": "Mirror", "year": 2012}
            self.assertEqual(sorted(movie1.items()), sorted(m1.items()))
    
    def test_get_movie(self):
        with app.test_request_context():
            # mock object
            resp = get_movie(1)
            movie = resp.json["movie"]
            m1 = {'FC': 16,"country": "Russia", "genre": 'thriller', "id": 1, "rating": 5, 
                    "title": "Mirror", "year": 2012}

            self.assertEqual(sorted(movie.items()), sorted(m1.items()))

    def test_put_movie(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.put('/api/1.0/movies/1', json = {'title': 'Mirror'})
            res = resp.json["Result of updating"]

            self.assertEqual(res, 'Succes')
    
    def test_post_movie(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            m1 = {'FC': 16,"country": "France", "genre": 'comedy', "id": 10, "rating": 5, 
                    "title": "99 franks", "year": 2008}
            resp = client.post('/api/1.0/movies', json = m1)
            print(resp)
            movie = resp.json["New movie"]
            self.assertEqual(sorted(movie.items()), sorted(m1.items()))

    def test_delete_movie(self):
        with app.test_request_context():
            # mock object
            client = app.test_client()
            resp = client.delete('/api/1.0/movies/10')
            print(resp)
            res = resp.json["Result of deleting"]

            self.assertEqual(res, 'Succes')

if __name__ == '__main__':
      unittest.main()
