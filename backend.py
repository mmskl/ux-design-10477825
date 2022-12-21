#!/usr/bin/python

from flask import Flask
from flask import jsonify, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

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

auth = HTTPBasicAuth()

def get_user():
    username = auth.username()
    res = cur.execute('select id, username from users where username=?', [ username ])
    return res.fetchone()

@auth.verify_password
def verify_password(username, password):

    if username == "admin" and password == "admin":
        return "admin"

    res = cur.execute('select username, hash from users where username=?', [ username ])
    u = res.fetchone()

    if u and check_password_hash(u['hash'], password):
        return username

    return False



@app.route('/logout')
def logout():
    return '', 401


@app.route('/')
def home():
    u = auth.username()
    return render_template('index.html', user=u)


@app.route('/users')
@auth.login_required
def users_list():
    users = [
            {'id':1, 'username':'john'}
            ]
    return render_template('users.html', users=users)



@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/register', methods=['POST'])
@auth.login_required
def register_send():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, hash) VALUES (?, ?);"
        cur.execute(sql, (username, password_hash))
        con.commit()

        return redirect(url_for('home'))

    return render_template('register.html')



@app.route('/api/dangers', methods=['GET'])
def get_dangers():

    res = cur.execute('select * from dangers')
    
    return jsonify(res.fetchall())


@app.route('/api/login')
@auth.login_required
def login():
    return jsonify({})


@app.route('/api/user')
def user():
    return jsonify({'username': auth.username()})


@app.route('/api/dangers', methods=['POST'])
@auth.login_required
def add_danger():
    data = request.json
    username = auth.username()
    print('adding danger')
    cur.execute("INSERT INTO dangers(level, desc, lat,lng, username) VALUES(?, ?, ?, ?, ?)",
            [data['level'], data['desc'], data['lat'], data['lng'], username])

    con.commit()

    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
