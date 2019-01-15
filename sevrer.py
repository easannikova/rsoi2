import requests
import psycopg2
import flask 
from flask import jsonify
from flask import request
import json

app = flask.Flask(__name__)
#url = 'http://localhost:5000/api/1.0/movies'
'''delete'''
#url += '/' + '2'
#r = requests.delete(url)
'''post'''
#params = {"id": 8, "title": "My little pony", "country": "USA"}
#r = requests.post(url, json = params)
'''get'''
#r = requests.get(url)
#print(r.status_code,r.json())
m_url = "http://localhost:5000/api/1.0/movies"
h_url = "http://localhost:5001/api/1.0/halls"
s_url = "http://localhost:5002/api/1.0/seanses"

def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )

def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/1.0/get_seanses')

@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return resp(405, {})

@app.route('/api/1.0/get_movies', methods=['GET'])
def app_get_movies():
    url = m_url
    r = requests.get(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/get_halls', methods=['GET'])
def app_get_halls():
    url = h_url
    r = requests.get(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/get_seanses', methods=['GET'])
def app_get_seanses():
    url = s_url
    r = requests.get(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/get_movies/<int:id>', methods=['GET'])
def app_get_movie(id):
    url = m_url  + "/"  + str(id)
    r = requests.get(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/get_halls/<int:id>', methods=['GET'])
def app_get_hall(id):
    url = h_url  + "/"  + str(id)
    r = requests.get(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/get_seanses/<int:id>', methods=['GET'])
def app_get_seanse(id):
    url = s_url  + "/"  + str(id)
    print(url)
    r = requests.get(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

'''@app.route('/api/1.0/movies/<int:id>', methods=['DELETE_MOVIE'])
def app_delete_movie(id):
    url = m_url  + "/"  + str(id)
    r = requests.delete(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/halls/<int:id>', methods=['DELETE_HALL'])
def app_delete_hall(id):
    url = h_url  + "/"  + str(id)
    r = requests.delete(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/seanses/<int:id>', methods=['DELETE_SEANSE'])
def app_delete_seanse(id):
    url = s_url  + "/"  + str(id)
    print(url)
    r = requests.delete(url)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/halls/<int:id>', methods=['PUT_MOVIE'])
def app_put_movie(id):
    url = m_url  + "/"  + str(id)
    country = request.json['country']
    data = {'country': country}
    r = requests.put(url, json = data)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/halls/<int:id>', methods=['PUT_HALL'])
def app_put_hall(id):
    url = h_url  + "/"  + str(id)
    number = request.json['number']
    data = {'number': number}
    r = requests.put(url, json = data)
    resp = r.json()
    return(jsonify({"Response": resp}))

@app.route('/api/1.0/halls/<int:id>', methods=['PUT_SEANSE'])
def app_put_seanse(id):
    url = s_url  + "/"  + str(id)
    number = request.json['number']
    data = {'number': number}
    r = requests.put(url, json = data)
    resp = r.json()
    return(jsonify({"Response": resp}))'''


'''Agregate requests'''
@app.route('/api/1.0/halls/<int:id>', methods=['PUT'])
def app_change_hall(id):
    #get old hall number 
    url1 = h_url  + "/"  + str(id)
    r = requests.get(url1)
    hall = r.json()["hall"]
    old_number = hall["number"]
    print('old,number', old_number)
    #change hall number in halls
    url1 = h_url  + "/"  + str(id)
    number = request.json['new_number']
    data = {'number': number}
    r = requests.put(url1, json = data)
    #update hall number in seanses DB
    url2 = s_url
    r = requests.get(url2)
    seanses = r.json()["seanses"]
    print(seanses)
    ids_change = []
    for seanse in seanses:
        if seanse['hall_number'] == old_number:
            ids_change.append(seanse['id'])
    for id_ch in ids_change:
        url = s_url + "/" + str(id_ch)
        data = {'value': number, 'object': 'hall_number'}
        r = requests.put(url, json = data)
    resp = r.json()
    return(jsonify({"Result of updating": 'Succes'}))

@app.route('/api/1.0/movies/<int:id>', methods=['PUT'])
def app_change_movie(id):
    #get old hall number 
    url1 = m_url  + "/"  + str(id)
    r = requests.get(url1)
    movie = r.json()["movie"]
    old_title = movie["title"]
    #change movie title in movies
    url1 = m_url  + "/"  + str(id)
    title = request.json['new_title']
    data = {'title': title}
    r = requests.put(url1, json = data)

    #update movie title in seanses DB
    url2 = s_url
    r = requests.get(url2)
    seanses = r.json()["seanses"]
    ids_change = []
    for seanse in seanses:
        movie_id = seanse['movie_title'].replace(' ', '')
        if movie_id == old_title:
            ids_change.append(seanse['id'])
    for id_ch in ids_change:
        url = s_url + "/" + str(id_ch)
        data = {'value': title, 'object': 'movie_title'}
        r = requests.put(url, json = data)
    resp = r.json()
    return(jsonify({"Result of updating": 'Succes'}))

@app.route('/api/1.0/seanses/<int:id>', methods=['GET'])
def app_get_ext_info(id):

    #get seanse
    url = s_url + "/" +str(id)
    r = requests.get(url)
    seanse = r.json()["seanse"]

    #get movie name and hall number
    title = seanse["movie_title"].replace(' ', '')
    number = seanse["hall_number"]
    print("ttttttttttnnnnnnnnnnn", title, number)

    #get movie id
    m_id = 0
    r = requests.get(m_url)
    movies = r.json()["movies"]
    for movie in movies:
        if movie["title"] == title:
            m_id = movie["id"]

    print("mmmmmmmmmmmmm", m_id)

    #get hall id
    h_id = 0
    r = requests.get(h_url)
    halls = r.json()["halls"]
    
    for hall in halls:
        if hall["number"] == number:
            h_id = hall["id"]

    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", h_id)
    #get movie FC
    url = m_url + "/" +str(m_id)
    r = requests.get(url)
    movie = r.json()["movie"]
    fc = movie["FC"]

    #get hall floor
    url = h_url + "/" +str(h_id)
    r = requests.get(url)
    hall = r.json()["hall"]
    floor = hall["floor"]


    #agregate info
    ext_seanse = seanse
    ext_seanse["FC"] = fc
    ext_seanse["floor"] = floor

    print(ext_seanse)
    return(jsonify({"Extended info about seanse": ext_seanse}))

if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run(host = "localhost", port =   5005)