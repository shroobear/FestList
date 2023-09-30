from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy


from config import db, bcrypt

# Models go here!

class Festival(db.Model, SerializerMixin):
    __tablename__ = 'festivals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    website = db.Column(db.String)
    # Many to many relationship with Artist through lineups table
    lineup = db.relationship('Lineup', back_populates='festival')

    user_festival = db.relationship('User_Festival', back_populates='festival')

class Artist(db.Model, SerializerMixin):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # Many to many relationship with Festival through lineup table
    lineup = db.relationship('Lineup', back_populates='artist')
    # Many to many relationship with Song through Song_Artist table
    song_artists = db.relationship('Song_Artist', back_populates='artist')
    #  Define many to many relationship with User through Favorite table
    favorites = db.relationship('Favorite', back_populates='artist')


class Lineup(db.Model):
    __tablename__ = 'lineups'
    # Ensure that all Artist Festival combinations are unique within the join table
    __table_args__ = (UniqueConstraint('festival_id', 'artist_id', name='unique_lineup'),)

    id = db.Column(db.Integer, primary_key=True)
    festival_id = db.Column(db.Integer, db.ForeignKey('festivals.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

    festival = db.relationship('Festival', back_populates='lineup')
    artist = db.relationship('Artist', back_populates='lineup')

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    spotify_id = db.Column(db.String)
    # Many to many relationship with Artist through Song_Artist table
    song_artists = db.relationship('Song_Artist', back_populates='song')

class Song_Artist(db.Model):
    __tablename__ = 'song_artists'
    # Ensure all combinations of Artists and songs are unique to prevent duplicates
    __table_args__ = (UniqueConstraint('song_id', 'artist_id', name='unique_collaboration'),)

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

    song = db.relationship('Song', back_populates='song_artists')
    artist = db.relationship('Artist', back_populates='song_artists')


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(55), nullable=False)
    last_name = db.Column(db.String(55), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(55), nullable=False, unique=True)
    spotify_access_token = db.Column(db.String)
    spotify_refresh_token = db.Column(db.String)
    # Defines many to many relationship through favorite table with artists
    favorites = db.relationship('Favorite', back_populates='user')
    user_festivals = db.relationship('User_Festival', back_populates='user')

    # formatted for bcrypt hashing
    _password_hash = db.Column(db.String, nullable=False)

    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed")
    
    @password_hash.setter
    def password_hash(self, password):
        hashed_password = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')
        self._password_hash = hashed_password

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    # Unique constraint to prevent duplicate favorites
    __table_args__ = (UniqueConstraint('user_id', 'artist_id', name='unique_favorite'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

    user = db.relationship('User', back_populates='favorites')
    artist = db.relationship('Artist', back_populates='favorites')

class User_Festival(db.Model):
    __tablename__ = 'user_festivals'
    __table_args__ = (UniqueConstraint('user_id', 'festival_id', name='unique_rsvp'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    festival_id = db.Column(db.Integer, db.ForeignKey('festivals.id'), nullable=False)

    user = db.relationship('User', back_populates='user_festivals')
    festival = db.relationship('Festival', back_populates='user_festival')