from config import app
from models import User, Festival, Artist, Song, User_Festival, Lineup, Favorite, Song_Artist

from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

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

class ArtistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist

    id = ma.auto_field()
    name = ma.auto_field()
    spotify_id = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("artistbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("artists"),
        }
    )

class SongSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song

    id = ma.auto_field()
    name = ma.auto_field()
    spotify_id = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("songbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("artists"),
        }
    )

class LineupSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lineup

    artist_id = ma.auto_field()
    festival_id = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("lineupbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("lineups"),
        }
    )

class SongArtistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song_Artist

    artist_id = ma.auto_field()
    song_id = ma.auto_field()

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("songartistbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("songartists"),
        }
    )
