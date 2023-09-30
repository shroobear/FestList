#!/usr/bin/env python3

# Standard library imports
from datetime import datetime

# Remote library imports
from flask import Flask, request, url_for, redirect, session, jsonify, make_response
from flask_restful import Resource
from flask_marshmallow import Marshmallow

# Local imports
from config import app, db, api, oauth, bcrypt


# Add your model imports
from models import User, Festival, Artist, Song, User_Festival, Lineup, Favorite


ma = Marshmallow(app)

# Views go here!
class UserSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = User

    first_name = ma.auto_field()
    last_name = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "userbyid",
                values = dict(id='<id>')),
                "collection": ma.URLFor("users"),
        }
    )

singular_user_schema = UserSchema()
plural_user_schema = UserSchema(many=True)

class FestivalSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Festival

    name = ma.auto_field()
    address = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
    date = ma.auto_field()
    website = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "festivalbyid",
                values = dict(id='<id>')),
            "collection": ma.URLFor("festivals"),
        }
    )

singular_festival_schema = FestivalSchema()
plural_festival_schema = FestivalSchema(many=True)

class ArtistSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Artist

    name = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "artistbyid",
                values=dict(id='<id>')),
            "collection": ma.URLFor('artists'),
        }
    )

singular_artist_schema = ArtistSchema()
plural_artist_schema = ArtistSchema(many=True)

class SongSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Song

        name = ma.auto_field()

        url = ma.Hyperlinks(
            {
                "self": ma.URLFor(
                    "songbyid",
                    values=dict(id='<id>')),
                "collection": ma.URLFor("artists"),
            }
        )

singular_song_schema = SongSchema()
plural_song_schema = SongSchema(many=True)

class Index(Resource):

    def get(self):

        response_dict = {
            "index": "Welcome to the FestList API"
        }

        response = make_response(
            response_dict,
            200,
        )

        return response
    
api.add_resource(Index, '/v1')

class Users(Resource):

    def get(self):

        users = User.query.all()

        response = make_response(
            plural_user_schema.dump(users),
            200,
        )

        return response
    
api.add_resource(Users, '/v1/users')

class UserByID(Resource):

    def get(self, id):

        user = User.query.filter_by(id=id).first()

        response = make_response(
            singular_user_schema.dump(user),
            200,
        )

        return response

api.add_resource(UserByID, '/v1/users/<int:id>')

class Festivals(Resource):
    def get(self):

        festivals = Festival.query.all()

        response = make_response(
            plural_festival_schema.dump(festivals),
            200,
        )

        return response
    
    def post(self):
        
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        new_festival = Festival(
            name=request.form['name'],
            address=request.form['address'],
            city=request.form['city'],
            state=request.form['state'],
            date=date_obj,
            website=request.form['website'],
        )
        db.session.add(new_festival)
        db.session.commit()

        response = make_response(
            singular_festival_schema.dump(new_festival),
            201,
        )

        return response

api.add_resource(Festivals, '/v1/festivals')

class FestivalByID(Resource):
    def get(self, id):

        festival = Festival.query.filter_by(id=id).first()

        response = make_response(
            singular_festival_schema.dump(festival),
            200,
        )

        return response
    
    def patch(self, id):

        festival = Festival.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(festival, attr, request.form[attr])

        db.session.add(festival)
        db.session.commit()

        response = make_response(
            singular_festival_schema.dump(festival),
            200
        )

        return response
    
    def delete(self, id):

        festival = Festival.query.filter_by(id=id).first()

        db.session.delete(festival)
        db.session.commit()

        response_dict = {"message": "festival successfully deleted"}

        response = make_response(
            response_dict,
            200
        )

        return response
    
api.add_resource(FestivalByID, '/v1/festivals/<int:id>')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        new_user = User(
            username=username, 
            first_name=first_name, 
            last_name=last_name,
            email=email
        )
        new_user.password_hash = password
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

# @app.route('/')
# def index():
#     print('running index')
#     email = dict(session).get('email', None)
#     name = dict(session).get('display_name')
#     return f'FestList Home Page. Hello, {name}'

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

