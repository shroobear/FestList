#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, url_for, redirect, session
from flask_restful import Resource


# Local imports
from config import app, db, api, oauth


# Add your model imports
from models import User, Festival, Artist, Song, User_Festival, Lineup, Favorite


# Views go here!

@app.route('/')

def index():
    print('running index')
    email = dict(session).get('email', None)
    name = dict(session).get('display_name')
    return f'FestList Home Page. Hello, {name}'

@app.route('/login')
def login():
    print('running login')
    spotify = oauth.create_client('spotify')
    redirect_uri = url_for('authorize', _external=True)
    response = spotify.authorize_redirect(redirect_uri)
    return response

@app.route('/redirect')
def redirect_page():
    return 'redirect'

# @app.route('/authorize')
# def authorize():
#     # import ipdb; ipdb.set_trace()
#     print('running authorize')
#     spotify = oauth.create_client('spotify')
#     token = spotify.authorize_access_token()
#     print(token)
#     resp = spotify.get('userinfo', token=token)
#     user_info = resp.json()
#     print('user Info::::::', user_info)
#     # user = oauth.spotify.userinfo()
#     # session['email'] = user_info['email']
#     return redirect('/')

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
            session['id'] = user_info.get('id')

            
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

