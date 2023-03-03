#!/usr/bin/env python3
"""Flask Application
"""


from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from os import getenv


# Create application
app = Flask(__name__)

# instantiate Auth
AUTH = Auth()


# home route
@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    '''
    '''
    return jsonify({"message": "Bienvenue"}), 200


# users route
@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''
    '''
    if request.method == 'POST':
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        try:
            AUTH.register_user(email, password)
            return jsonify({"email": email, "message": "user created"}), 200
        except ValueError:
            return jsonify({"message": "email already registered"}), 200


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''
        Login user by setting cookies
    '''
    if request.method == 'POST':
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        valid = AUTH.valid_login(email, password)
        if valid:
            session_id = AUTH.create_session(email)
            resp = jsonify({"email": email, "message": "logged in"})
            resp.set_cookie('session_id', session_id)
            return resp
        else:
            abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    '''
        Log Out user getting cookies and destroying the cookies
    '''
    if request.method == 'DELETE':
        cook = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(cook)
        if user is None:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    '''
    '''
    cook = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(cook)
    if user is None:
        abort(403)
    return jsonify({'email': user.email }), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    '''
    '''
    if request.method == 'POST':
        email = str(request.form.get('email'))
        try:
            token = AUTH.get_reset_password_token(email)
            return jsonify({'email': email, "reset_token": token}), 200
        except ValueError:
            abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    '''
    '''
    if request.method == 'PUT':
        email = str(request.form.get('email'))
        reset_token = str(request.form.get('reset_token'))
        new_password = str(request.form.get('new_password'))
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify({"email": email, "message": "Password updated"}), 200
        except ValueError:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
