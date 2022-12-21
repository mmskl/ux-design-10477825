#!/usr/bin/python

from flask import Flask
from flask import jsonify, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPDigestAuth
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from sys import exit

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

app.secret_key = b'_5#2"4aslkdj23u8xec]/'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


class User():
    def __init__(self, user_id, username='anonymous'):
        self.id = user_id
        self.username = username
    @property
    def get_username(self):
        return self.username
    @property
    def is_authenticated(self):
        return self.is_active
    @property
    def is_active(self):
        return True
    def is_anonymous(self):
        return True

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

@login_manager.user_loader
def load_user(user_id):
    res = cur.execute('select id, username from users where id=?', [ user_id ])
    r = res.fetchone()
    return User(r['id'], r['username'])


def verify_password(username, password):

    # if username == "admin" and password == "admin":
    #     return "admin"

    res = cur.execute('select id, username, hash from users where username=?', [ username ])
    u = res.fetchone()

    if u and check_password_hash(u['hash'], password):
        return User(u['id'], u['username'])

    return None



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/register', methods=['POST', 'GET'])
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        result =  verify_password(username, password)
        print('result', result)
        if result != None:
            login_user(result)
            flash('Zalogowałeś się!')
            return redirect(url_for('home'))

        flash('Hasło/Użytkownik nieprawidłowy')
    return render_template('login.html')




@app.route('/api/dangers', methods=['GET'])
def get_dangers():

    res = cur.execute('select * from dangers')
    
    return jsonify(res.fetchall())


@app.route('/api/dangers', methods=['POST'])
@login_required
def add_danger():
    data = request.json
    username = current_user.get_username
    cur.execute("INSERT INTO dangers(level, desc, lat,lng, username) VALUES(?, ?, ?, ?, ?)",
            [data['level'], data['desc'], data['lat'], data['lng'], username])

    con.commit()

    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
