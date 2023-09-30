#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, url_for, redirect, session
from flask_restful import Resource
from flask_bcrypt import bcrypt

# Local imports
from config import app, db, api, oauth


# Add your model imports
from models import User, Festival, Artist, Song, User_Festival, Lineup, Favorite


# Views go here!

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            username=username, 
            password_hash=hashed_password, 
            first_name=first_name, 
            last_name=last_name,
            email=email
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    return 'Signup Page'

@app.route('/festlist_login', methods=['GET', 'POST'])
def festlist_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return 'Invalid login credentials', 401
    return 'FestList Login Page'

@app.route('/')
def index():
    print('running index')
    email = dict(session).get('email', None)
    name = dict(session).get('display_name')
    return f'FestList Home Page. Hello, {name}'

@app.route('/spotify_login')
def spotify_login():
    print('running login')
    spotify = oauth.create_client('spotify')
    redirect_uri = url_for('authorize', _external=True)
    response = spotify.authorize_redirect(redirect_uri)
    return response

@app.route('/redirect')
def redirect_page():
    return 'redirect'

@app.route('/authorize')
def authorize():
    try:
        spotify = oauth.create_client('spotify')
        token = spotify.authorize_access_token()
        
        if token:
            # Fetch user information using the correct Spotify API endpoint.
            resp = spotify.get('v1/me', token=token)
            user_info = resp.json()
            
            # Storing user info in session
            session['email'] = user_info.get('email')
            session['display_name'] = user_info.get('display_name')
            session['spotify_id'] = user_info.get('id')

            
            print('User Info:', user_info)
            return redirect('/')
        else:
            return "Authorization failed", 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred during authorization", 400

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

