#!/usr/bin/python

from flask import Flask
from flask import jsonify, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from flask_cors import CORS


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

    return jsonify([
            {'lat': 50.257302985794446, 'lng': 18.97321701049805},
            {'lat': 50.26630164859335, 'lng': 19.061965942382816}
        ])
    # return jsonify({'asd': 'efg'})


@app.route('/api/dangers', methods=['POST'])
@auth.login_required
def add_danger():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
