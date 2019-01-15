import psycopg2
import flask 
from flask import jsonify
from flask import request
import json

app = flask.Flask(__name__)

# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def db_conn():
    con = None
    con = psycopg2.connect(database = 'hallsDB', user = 'sea')
    return con


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def hall_validate():
    errors = []
    json = request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    '''for field_name in ['number']:
        if type(json.get(field_name)) is not str:
            errors.append(
                "Field '{}' is missing or is not a string".format(
          field_name))'''

    return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/1.0/halls')

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


@app.route('/api/1.0/halls', methods=['GET'])
def get_halls():
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from halls;')
        rows = cur.fetchall()
        halls = []
        for row in rows:
            halls.append({"id": row[0], "number": row[1], "floor": row[2], "seats_count": row[3], "is3d": row[4]})
        return jsonify({"halls": halls})

@app.route('/api/1.0/halls/<int:hall_id>', methods=['GET'])
def get_hall(hall_id):
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from halls where id = %s;', (str(hall_id)))
        row = cur.fetchone()
        hall = {"id": row[0], "number": row[1], "floor": row[2], "seats_count": row[3], "is3d": row[4]}
        return jsonify({"hall": hall})


@app.route('/api/1.0/halls', methods=['POST'])
def post_hall():
    
    with db_conn() as db:
        print("dddddddddd")
        cur = db.cursor()
        number = request.json['number']
        hall_id = request.json['id']
        insert = cur.execute("INSERT INTO halls (id, number) VALUES (%s, %s)"
                             + "RETURNING id", (str(hall_id), str(number)))
                             #+ "RETURNING id", (str(id), number, floor))
        db.commit()
        hall = {"id": hall_id, "number": number}
        return jsonify({"New hall": hall})

@app.route('/api/1.0/halls/<int:hall_id>', methods=['PUT'])
def put_hall(hall_id):
    (json, errors) = hall_validate()
    if errors:  # list is not empty
        return resp(400, {"errors": errors})
    with db_conn() as db:
        cur = db.cursor()
        number = request.json['number']
        print(hall_id, number)
        query = "UPDATE halls SET number = %s WHERE id = %s"
        update = cur.execute(query, (str(number), str(hall_id)))
        db.commit()
    return jsonify({'Result of updating': 'Succes'})


@app.route('/api/1.0/halls/<int:hall_id>', methods=['DELETE'])
def delete_hall(hall_id):
    with db_conn() as db:
        cur = db.cursor()
        query = "DELETE FROM halls WHERE id = %s" % (str(hall_id))
        delete = cur.execute(query)
        db.commit()
        return jsonify({'Result of deleting': 'Succes'})

if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run(host = "localhost", port = 5001)
