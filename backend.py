#!/usr/bin/python

from flask import Flask
from flask import jsonify, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from flask_cors import CORS

import sqlite3

def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

con = sqlite3.connect("dangers.db", check_same_thread=False) 
con.row_factory = dict_factory
cur = con.cursor()


app = Flask(__name__,
            static_url_path='/web', 
            static_folder='web',
            template_folder='web')

CORS(app)

auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("john1"),
    "susan": generate_password_hash("susan1")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def home():
   return render_template('index.html')






@app.route('/api/dangers', methods=['GET'])
@auth.login_required
def get_dangers():

    res = cur.execute('select * from dangers')
    
    return jsonify(res.fetchall())


@app.route('/api/dangers', methods=['POST'])
@auth.login_required
def add_danger():
    data = request.json
    
    cur.execute("INSERT INTO dangers(level, desc, lat,lng) VALUES(?, ?, ?, ?)", [data['level'], data['desc'], data['lat'], data['lng']])
    con.commit()

    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
