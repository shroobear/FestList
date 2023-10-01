#!/usr/bin/env python3

# Standard library imports
from datetime import datetime

# Remote library imports
from flask import Flask, request, url_for, redirect, session, jsonify, make_response
from flask_restful import Resource
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import joinedload

# Local imports
from config import app, db, api, oauth, bcrypt, host_port
from helpers import Routing


# Add your model imports
from models import (
    User,
    Festival,
    Artist,
    Song,
    User_Festival,
    Lineup,
    Favorite,
    Song_Artist,
)


ma = Marshmallow(app)


# Views go here!
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("userbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )


singular_user_schema = UserSchema()
plural_user_schema = UserSchema(many=True)


class FestivalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Festival

    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
    date = ma.auto_field()
    website = ma.auto_field()
    url = ma.Method("generate_urls")

    def generate_urls(self, obj):
        return {
            "self": f"/v1/festivals/{obj.id}",
            "collection": "/v1/festivals",
            "lineup": f"/v1/festivals/{obj.id}/lineup",
        }


singular_festival_schema = FestivalSchema()
plural_festival_schema = FestivalSchema(many=True)


class ArtistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist

    id = ma.auto_field()
    name = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("artistbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("artists"),
        }
    )


singular_artist_schema = ArtistSchema()
plural_artist_schema = ArtistSchema(many=True)


class SongSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song

    id = ma.auto_field()
    name = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("songbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("artists"),
        }
    )


singular_song_schema = SongSchema()
plural_song_schema = SongSchema(many=True)


class Index(Resource):
    def get(self):
        name = dict(session).get("display_name")
        response_dict = {
            "index": f"Welcome to the FestList API. Hello, {name}",
            "endpoint directory": [
                {
                    "festivals": f"{host_port}/v1/festivals",
                    "users": f"{host_port}/v1/users",
                    "artists": f"{host_port}/v1/artists",
                    "songs": f"{host_port}/v1/songs",
                }
            ],
        }

        response = make_response(
            response_dict,
            200,
        )

        return response


api.add_resource(Index, "/v1")


class Users(Resource):
    def get(self):
        return Routing.get_all(self, User, plural_user_schema)

    def post(self):
        new_user = User(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            username=request.form["username"],
            email=request.form["email"],
        )
        new_user.password_hash = request.form["password"]

        db.session.add(new_user)
        db.session.commit()

        response = make_response(
            singular_user_schema.dump(new_user),
            201,
        )

        return response


api.add_resource(Users, "/v1/users")


class UserByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, User, singular_user_schema)

    def patch(self, id):
        return Routing.patch(self, id, User, singular_user_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, User, "User")


api.add_resource(UserByID, "/v1/users/<int:id>")


class Festivals(Resource):
    def get(self):
        return Routing.get_all(self, Festival, plural_festival_schema)

    def post(self):
        date_str = request.form["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        new_festival = Festival(
            name=request.form["name"],
            address=request.form["address"],
            city=request.form["city"],
            state=request.form["state"],
            date=date_obj,
            website=request.form["website"],
        )
        db.session.add(new_festival)
        db.session.commit()

        response = make_response(
            singular_festival_schema.dump(new_festival),
            201,
        )

        return response


api.add_resource(Festivals, "/v1/festivals")


class FestivalByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Festival, singular_festival_schema)

    def patch(self, id):
        return Routing.patch(self, id, Festival, singular_festival_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, Festival, "Festival")


api.add_resource(FestivalByID, "/v1/festivals/<int:id>")


class FestivalLineup(Resource):
    def get(self, id):
        lineup = Routing.get_relationship(self, id, Lineup, "artist", "festival_id")

        artists = [entry.artist for entry in lineup]

        response = make_response(plural_artist_schema.dump(artists), 200)

        return response


api.add_resource(FestivalLineup, "/v1/festivals/<int:id>/lineup")


class Artists(Resource):
    def get(self):
        return Routing.get_all(self, Artist, plural_artist_schema)

    def post(self):
        new_artist = Artist(name=request.form["name"])
        db.session.add(new_artist)
        db.session.commit()

        response = make_response(
            singular_artist_schema.dump(new_artist),
            201,
        )

        return response


api.add_resource(Artists, "/v1/artists")


class ArtistByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Artist, singular_artist_schema)

    def patch(self, id):
        return Routing.patch(self, id, Artist, singular_artist_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, Artist, "Artist")


api.add_resource(ArtistByID, "/v1/artists/<int:id>")


class Favorites(Resource):
    def get(self, id):
        favorites = Routing.get_relationship(self, id, Favorite, "artist", "user_id")

        artists = [entry.artist for entry in favorites]

        response = make_response(plural_artist_schema.dump(artists), 200)

        return response


api.add_resource(Favorites, "/v1/users/<int:id>/favorites")


class SongsByArtist(Resource):
    def get(self, id):
        songs_by_artist = Routing.get_relationship(
            self, id, Song_Artist, "song", "artist_id"
        )

        songs = [entry.song for entry in songs_by_artist]

        response = make_response(plural_song_schema.dump(songs), 200)

        return response


api.add_resource(SongsByArtist, "/v1/artists/<int:id>/songs")


class Songs(Resource):
    def get(self):
        return Routing.get_all(self, Song, plural_song_schema)

    def post(self):
        new_song = Song(name=request.form["name"])
        db.session.add(new_song)
        db.session.commit()

        response = make_response(singular_song_schema.dump(new_song), 201)

        return response


api.add_resource(Songs, "/v1/songs")


class SongByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Song, singular_song_schema)

    def patch(self, id):
        return Routing.patch(self, id, Song, singular_song_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, Song, "song")


api.add_resource(SongByID, "/v1/songs/<int:id>")


class ArtistsOfSong(Resource):
    def get(self, id):
        artists_by_song = Routing.get_relationship(
            self, id, Song_Artist, "artist", "song_id"
        )

        artists = [entry.artist for entry in artists_by_song]

        response = make_response(plural_artist_schema.dump(artists), 200)

        return response


api.add_resource(ArtistsOfSong, "/v1/songs/<int:id>/artists")


class FestivalRSVPs(Resource):
    def get(self, id):
        festival_rsvps = Routing.get_relationship(
            self, id, User_Festival, "festival", "user_id"
        )

        festivals = [entry.festival for entry in festival_rsvps]

        response = make_response(plural_festival_schema.dump(festivals), 200)

        return response


api.add_resource(FestivalRSVPs, "/v1/users/<int:id>/rsvps")


class Attendees(Resource):
    def get(self, id):
        attendees = Routing.get_relationship(
            self, id, User_Festival, "user", "festival_id"
        )

        users = [entry.user for entry in attendees]

        response = make_response(plural_user_schema.dump(users), 200)

        return response


api.add_resource(Attendees, "/v1/festivals/<int:id>/attendees")


@app.route("/v1/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")

        new_user = User(
            username=username, first_name=first_name, last_name=last_name, email=email
        )
        new_user.password_hash = password
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("index"))
    return "Signup Page"


@app.route("/v1/festlist_login", methods=["GET", "POST"])
def festlist_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            return "Invalid login credentials", 401
    return "FestList Login Page"


# @app.route('/')
# def index():
#     print('running index')
#     email = dict(session).get('email', None)
#     name = dict(session).get('display_name')
#     return f'FestList Home Page. Hello, {name}'


@app.route("/v1/spotify_login")
def spotify_login():
    print("running login")
    spotify = oauth.create_client("spotify")
    redirect_uri = url_for("authorize", _external=True)
    response = spotify.authorize_redirect(redirect_uri)
    return response


@app.route("/v1/redirect")
def redirect_page():
    return "redirect"


@app.route("/v1/authorize")
def authorize():
    try:
        spotify = oauth.create_client("spotify")
        token = spotify.authorize_access_token()

        if token:
            # Fetch user information using the correct Spotify API endpoint.
            resp = spotify.get("v1/me", token=token)
            user_info = resp.json()

            # Storing user info in session
            session["email"] = user_info.get("email")
            session["display_name"] = user_info.get("display_name")
            session["spotify_id"] = user_info.get("id")

            print("User Info:", user_info)
            return redirect("/v1")
        else:
            return "Authorization failed", 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred during authorization", 400


@app.route("/v1/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/v1")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
