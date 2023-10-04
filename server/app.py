#!/usr/bin/env python3

# Standard library imports
from datetime import datetime

# Remote library imports
from flask import Flask, request, url_for, redirect, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.orm import joinedload
import requests
from sqlalchemy import and_

# Local imports
from config import app, db, api, oauth, bcrypt, host_port, FRONTEND_BASE_URL
from helpers import Routing

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
from schemas import (
    UserSchema,
    FestivalSchema,
    ArtistSchema,
    SongSchema,
    LineupSchema,
    SongArtistSchema,
    RSVPSchema,
)



singular_user_schema = UserSchema()
plural_user_schema = UserSchema(many=True)
singular_festival_schema = FestivalSchema()
plural_festival_schema = FestivalSchema(many=True)
singular_artist_schema = ArtistSchema()
plural_artist_schema = ArtistSchema(many=True)
singular_song_schema = SongSchema()
plural_song_schema = SongSchema(many=True)
singular_lineup_schema = LineupSchema()
plural_lineup_schema = LineupSchema(many=True)
singular_song_artist_schema = SongArtistSchema()
plural_song_artist_schema = SongArtistSchema(many=True)
singular_rsvp_schema = RSVPSchema()
plural_rsvp_schema = RSVPSchema(many=True)


# User Routes ------------------------------------------------------------

class Users(Resource):
    def get(self):
        return Routing.get_all(self, User, plural_user_schema)

    def post(self):
        data = request.get_json()
        password = data["password"]
        username = data["username"]
        new_user = User(
            username=username,
            first_name=data["firstName"],
            last_name=data["lastName"],
            email=data["email"],
        )
        new_user.password_hash = password

        if User.query.filter(User.username == new_user.username).first():
            return make_response({"message": "Username already taken"}, 409)

        elif User.query.filter(User.email == new_user.email).first():
            return make_response(
                {"message": "An account already exists under that email"}, 409
            )

        if username and password:
            db.session.add(new_user)
            db.session.commit()

            response = make_response(singular_user_schema.dump(new_user), 201)

            return response

        return {"error": "422 Unprocessable Entity"}, 422
    
class UserByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, User, singular_user_schema)

    def patch(self, id):
        return Routing.patch(self, id, User, singular_user_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, User, "User")
    

# Festival Routes ------------------------------------------------------------

class Festivals(Resource):
    def get(self):
        return Routing.get_all(self, Festival, plural_festival_schema)

    def post(self):
        date_str = request.json["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        new_festival = Festival(
            name=request.json["name"],
            address=request.json["address"],
            city=request.json["city"],
            state=request.json["state"],
            date=date_obj,
            website=request.json.get("website", ""),
            user_id=session["user_id"],
        )
        db.session.add(new_festival)
        db.session.commit()

        response = make_response(
            singular_festival_schema.dump(new_festival),
            201,
        )

        return response
    
class FestivalByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Festival, singular_festival_schema)

    def patch(self, id):
        return Routing.patch(self, id, Festival, singular_festival_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, Festival, "Festival")
    
# Artist Routes ------------------------------------------------------------------------------

class Artists(Resource):
    def get(self):
        return Routing.get_all(self, Artist, plural_artist_schema)

    def post(self):
        new_artist = Artist(
            name=request.json["name"], spotify_id=request.json["spotify_id"]
        )
        db.session.add(new_artist)
        db.session.commit()

        response = make_response(
            singular_artist_schema.dump(new_artist),
            201,
        )

        return response


class ArtistByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Artist, singular_artist_schema)

    def patch(self, id):
        return Routing.patch(self, id, Artist, singular_artist_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, Artist, "Artist")


class ArtistByName(Resource):
    def get(self, name):
        artist = Artist.query.filter(Artist.name.ilike(name)).first()

        if not artist:
            return make_response({"message": "Entry not found"}, 404)

        response = make_response(singular_artist_schema.dump(artist), 200)

        return response
    


# Song Routes ------------------------------------------------------------
class SongsByArtist(Resource):
    def get(self, id):
        songs_by_artist = Routing.get_relationship(
            self, id, Song_Artist, "song", "artist_id"
        )

        songs = [entry.song for entry in songs_by_artist]

        response = make_response(plural_song_schema.dump(songs), 200)

        return response


class Songs(Resource):
    def get(self):
        return Routing.get_all(self, Song, plural_song_schema)

    def post(self):
        new_song = Song(
            name=request.json["name"],
            spotify_id=request.json['spotify_id']
            )
        db.session.add(new_song)
        db.session.commit()

        response = make_response(singular_song_schema.dump(new_song), 201)

        return response


class SongByID(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Song, singular_song_schema)

    def patch(self, id):
        return Routing.patch(self, id, Song, singular_song_schema)

    def delete(self, id):
        return Routing.delete_entry(self, id, Song, "song")

class SongBySpotifyId(Resource):
    def get(self, spotify_id):
        song = Song.query.filter(Song.spotify_id == spotify_id).first()
        if not song:
            return make_response({"message": "Song not Found"}, 404)
        
        response = make_response(singular_artist_schema.dump(song), 200)

        return response
 
# Lineup Routes ----------------------------------------------------------

class LineupByFestival(Resource):
    def get(self, id):
        lineup = Routing.get_relationship(self, id, Lineup, "artist", "festival_id")

        artists = [entry.artist for entry in lineup]

        response = make_response(plural_artist_schema.dump(artists), 200)

        return response

class Lineups(Resource):
    def get(self):
        return Routing.get_all(self, Lineup, plural_lineup_schema)


class LineupById(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Lineup, singular_lineup_schema)


class LineupByPair(Resource):
    def get(self, festival_id, artist_id):
        lineup = Lineup.query.filter(and_(Lineup.festival_id == festival_id, Lineup.artist_id == artist_id)).first()

        if not lineup:
            return ({"message": "Lineup pair not found"}, 404)

        response = make_response(singular_lineup_schema.dump(lineup), 200)

        return response
    
    def post(self, festival_id, artist_id):
        existing_pair = Lineup.query.filter(and_(Lineup.festival_id == festival_id, Lineup.artist_id == artist_id)).first()
        if existing_pair:
            return {"message": "This lineup pair already exists"}, 400

        new_lineup = Lineup(
            festival_id=festival_id,
            artist_id=artist_id
        )
        db.session.add(new_lineup)
        db.session.commit()
        
        response = make_response(singular_lineup_schema.dump(new_lineup), 201)
        return response

# Favorites Routes -----------------------------------------------------

class Favorites(Resource):
    def get(self, id):
        favorites = Routing.get_relationship(self, id, Favorite, "artist", "user_id")

        artists = [entry.artist for entry in favorites]

        response = make_response(plural_artist_schema.dump(artists), 200)

        return response
    
# Song_Artist Routes -----------------------------------------------------------
class ArtistsOfSong(Resource):
    def get(self, id):
        artists_by_song = Routing.get_relationship(
            self, id, Song_Artist, "artist", "song_id"
        )

        artists = [entry.artist for entry in artists_by_song]

        response = make_response(plural_artist_schema.dump(artists), 200)

        return response

class SongArtists(Resource):
    def get(self):
        return Routing.get_all(self, Song_Artist, plural_song_artist_schema)

class SongArtistById(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, Song_Artist, singular_song_artist_schema)


class SongArtistByPair(Resource):
    def get(self, artist_id, song_id):
        check_pair = Song_Artist.query.filter(and_(Song_Artist.artist_id == artist_id), Song_Artist.song_id == song_id).first()

        if not check_pair:
            return ({"message": "Song_Artist pair not found"}, 404)
        
        response = make_response(singular_song_artist_schema.dump(check_pair), 200)

        return response
    
    def post(self, artist_id, song_id):
        existing_pair = Song_Artist.query.filter(and_(Song_Artist.artist_id == artist_id), Song_Artist.song_id == song_id)

        if existing_pair:
            return {"message": "This song_artist pair already exists"}, 400
        
        new_song_artist = Song_Artist(
            song_id=song_id,
            artist_id=artist_id
        )
        db.session.add(new_song_artist)
        db.session.commit()

        response = make_response(singular_song_artist_schema.dump(new_song_artist), 201)
        return response

# RSVP Routes

class RSVPsById(Resource):
    def get(self, id):
        return Routing.get_by_id(self, id, User_Festival, singular_rsvp_schema)

class RSVPs(Resource):
    def get(self):
        return Routing.get_all(self, User_Festival, plural_rsvp_schema)
    
    def post(self):
        new_rsvp = User_Festival(
            user_id = request.json['user_id'],
            festival_id = request.json['festival_id']
        )
        db.session.add(new_rsvp)
        db.session.commit()

        response = make_response(singular_rsvp_schema.dump(new_rsvp), 201)
        return response

# Other Join Routes ----------------------------------------------------------------


class UserRSVPs(Resource):
    def get(self, id):
        festival_rsvps = Routing.get_relationship(
            self, id, User_Festival, "festival", "user_id"
        )

        festivals = [entry.festival for entry in festival_rsvps]

        response = make_response(plural_festival_schema.dump(festivals), 200)

        return response


class Attendees(Resource):
    def get(self, id):
        attendees = Routing.get_relationship(
            self, id, User_Festival, "user", "festival_id"
        )

        users = [entry.user for entry in attendees]

        response = make_response(plural_user_schema.dump(users), 200)

        return response
    
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
api.add_resource(Users, "/v1/users")
api.add_resource(UserByID, "/v1/users/<int:id>")
api.add_resource(Festivals, "/v1/festivals")
api.add_resource(FestivalByID, "/v1/festivals/<int:id>")
api.add_resource(LineupByPair, "/v1/lineups/pair/<int:festival_id>/<int:artist_id>")
api.add_resource(Lineups, "/v1/lineups")
api.add_resource(LineupById, "/v1/lineups/<int:id>")
api.add_resource(LineupByFestival, "/v1/festivals/<int:id>/lineup")
api.add_resource(Artists, "/v1/artists")
api.add_resource(ArtistByID, "/v1/artists/<int:id>")
api.add_resource(ArtistByName, "/v1/artists/search/<string:name>")
api.add_resource(Favorites, "/v1/users/<int:id>/favorites")
api.add_resource(SongsByArtist, "/v1/artists/<int:id>/songs")
api.add_resource(Songs, "/v1/songs")
api.add_resource(SongByID, "/v1/songs/<int:id>")
api.add_resource(SongBySpotifyId, "/v1/songs/search/<string:spotify_id>")
api.add_resource(ArtistsOfSong, "/v1/songs/<int:id>/artists")
api.add_resource(SongArtists, '/v1/song_artists')
api.add_resource(SongArtistByPair, "/v1/song_artists/pair/<int:song_id>/<int:artist_id>")
api.add_resource(SongArtistById, "/v1/song_artists/<int:id>")
api.add_resource(UserRSVPs, "/v1/users/<int:id>/rsvps")
api.add_resource(Attendees, "/v1/festivals/<int:id>/attendees")
api.add_resource(RSVPs, "/v1/rsvps")
api.add_resource(RSVPsById, "/v1/rsvps/<int:id>")


@app.route("/v1/festlist_login", methods=["POST"])
def festlist_login():
    data = request.get_json()

    if request.method == "POST":
        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.authenticate(password) == True:
            session["user_id"] = user.id
            if user.spotify_access_token and user.spotify_refresh_token:
                session["spotify_token"] = user.spotify_access_token
                session["spotify_refresh_token"] = user.spotify_refresh_token
            return (
                jsonify(
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    username=user.username,
                ),
                200,
            )
        else:
            return jsonify({"message": "Invalid login credentials"}), 401
    return "FestList Login Page"


@app.route("/v1/check_session", methods=["GET"])
def current_user():
    print("Session data", session)

    user_id = session.get("user_id")
    if not user_id:
        return {"error": "No user ID found in the session"}, 401

    user = User.query.filter(User.id == user_id).first()
    if not user:
        return {"error": f"No user found in the database with user ID: {user_id}"}, 404

    return (
        jsonify(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
        ),
        200,
    )


@app.route("/v1/spotify_login")
def spotify_login():
    print("running login")
    spotify = oauth.create_client("spotify")
    redirect_uri = url_for("authorize", _external=True)
    response = spotify.authorize_redirect(redirect_uri)
    return response


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
            session["spotify_email"] = user_info.get("email")
            session["spotify_display_name"] = user_info.get("display_name")
            session["spotify_id"] = user_info.get("id")
            session["spotify_token"] = token["access_token"]
            session["spotify_refresh_token"] = token["refresh_token"]

            user = User.query.filter_by(id=session["user_id"]).first()
            if user:
                user.spotify_access_token = token["access_token"]
                user.spotify_refresh_token = token["refresh_token"]
                db.session.commit()

            print("User Info:", user_info)
            return redirect(f"{FRONTEND_BASE_URL}/profile?linked=true")
        else:
            return {"Authorization failed", 401}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}, 500


@app.route("/v1/search_artist", methods=["POST"])
def search_artist():
    data = request.get_json()
    query = data["query"]

    headers = {"Authorization": f"Bearer {session['spotify_token']}"}
    response = requests.get(
        f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=12",
        headers=headers,
    )

    if response.status_code == 401:  # Token expired
        refreshed = refresh_spotify_token()
        if not refreshed:
            return jsonify({"error": "Token refresh failed"}), 401
        headers["Authorization"] = f"Bearer {session['spotify_token']}"
        response = requests.get(
            f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=12",
            headers=headers,
        )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Spotify"})

    artists = response.json().get("artists", {}).get("items", [])

    return jsonify(artists)


def refresh_spotify_token():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": session["spotify_refresh_token"],
        "client_id": app.config["SPOTIFY_CLIENT_ID"],
        "client_secret": app.config["SPOTIFY_CLIENT_SECRET"],
    }

    response = requests.post("https://accounts.spotify.com/api/token", data=data)

    if response.status_code != 200:
        print("Error refreshing token")
        return False

    token_info = response.json()
    session["spotify_token"] = token_info["access_token"]

    return True

@app.route("/v1/artist_top_tracks/<string:artist_spotify_id>", methods=["GET"])
def get_artist_top_tracks(artist_spotify_id):
    if 'spotify_token' not in session:
        return {"error": "Spotify token not found in session. Please login again."}, 401

    headers = {"Authorization": f"Bearer {session['spotify_token']}"}
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_spotify_id}/top-tracks?market=US",
        headers=headers
    )

    if response.status_code == 401:  # Token expired
        refreshed = refresh_spotify_token()
        if not refreshed:
            return jsonify({"error": "Token refresh failed"}), 401
        headers["Authorization"] = f"Bearer {session['spotify_token']}"
        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_spotify_id}/top-tracks?market=US",
            headers=headers
        )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Spotify"})

    tracks = response.json().get("tracks", [])

    

    return jsonify(tracks)
    


@app.route("/v1/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/v1")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
