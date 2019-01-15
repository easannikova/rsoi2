import psycopg2
import flask 
from flask import jsonify
from flask import request
import json
import math

app = flask.Flask(__name__)

# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def db_conn():
    con = None
    con = psycopg2.connect(database = 'moviesDB', user = 'sea')
    print(con)
    return con


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def movie_validate():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/1.0/movies')

# e.g. failed to parse json
@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return resp(405, {})


@app.route('/api/1.0/movies', methods=['GET'])
def get_movies():
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from movies;')
        rows = cur.fetchall()
        movies = []
        for row in rows:
            movies.append({"id": row[0], "title": row[1], "year": row[2], "country": row[3], "genre": row[4], "rating": row[5], "FC": row[6]})
        return jsonify({"movies": movies})
        #return True

@app.route('/api/1.0/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from movies where id = %s;', (str(movie_id)))
        row = cur.fetchone()
        movie = {"id": row[0], "title": row[1], "year": row[2], "country": row[3], "genre": row[4], "rating": row[5], "FC": row[6]}
        return jsonify({"movie": movie})


@app.route('/api/1.0/movies', methods=['POST'])
def post_movie():
    with db_conn() as db:
        cur = db.cursor()
        title = request.json['title']
        country = request.json['country']
        id = request.json['id']
        year = request.json['year']
        genre = request.json['genre']
        rating = request.json['rating']
        FC = request.json['FC']
        print(id, title, country)
        insert = cur.execute("INSERT INTO movies (id, title, year, country, genre, rating, FC) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                             + "RETURNING id", (str(id), title, year, country, genre, rating, FC))
        db.commit()
        movie = {"id": id, "title": title, "country": country, "year": year, "genre": genre, "rating": rating, "FC": FC}
        return jsonify({"New movie": movie})

@app.route('/api/1.0/movies/<int:movie_id>', methods=['PUT'])
def put_movie(movie_id):

    with db_conn() as db:
        cur = db.cursor()
        title = request.json['title']
        query = "UPDATE movies SET title = %s WHERE id = %s"
        update = cur.execute(query, (title, str(movie_id)))
        db.commit()
        return jsonify({'Result of updating': 'Succes'})


@app.route('/api/1.0/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    with db_conn() as db:
        movie_id = str(movie_id)
        print(movie_id)

        print(type(movie_id))
        cur = db.cursor()
        query = "DELETE FROM movies WHERE id = %s"  %  movie_id 
        delete = cur.execute(query)
        db.commit()
        return jsonify({'Result of deleting': 'Succes'})


@app.route('/api/1.0/movies/size=<int:size>&index=<int:index>', methods=['GET'])
def get_movies_pagination(size, index):
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from movies;')
        rows = cur.fetchall()
        movies = []
        for row in rows:
            movies.append({"id": row[0], "title": row[1], "year": row[2], "country": row[3], "genre": row[4], "rating": row[5], "FC": row[6]})
        cnt = len(movies)
        pageCount = math.ceil(cnt/size)
        if (index > pageCount):
            return  'Page not found!'
        left = size*(index-1)
        if left < 0:
            left = 0
        right = size*index
        '''if right > cnt:
            right = '''
        movies = movies[left:right]
        print(left, right, movies)
        return jsonify({"movies": movies})
        #return True
#pageSize=3&pageIndex=0
        

if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run()
