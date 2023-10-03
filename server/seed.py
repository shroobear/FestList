#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker
from alive_progress import alive_bar, alive_it
from flask_bcrypt import bcrypt

# Local imports
from app import app
from models import db, User, Festival, Artist, Lineup, Song, Song_Artist, User_Festival, Favorite
from artists import artists, artist_top_songs_dict


fake = Faker()

def clear_table(table_class):
    db.session.query(table_class).delete()
    db.session.commit()
    print(f'{table_class} table cleared')

def seed_users():
    print("\nSeeding Users 👥\n")
    Faker.seed(0)
    with alive_bar(50) as bar:
        for i in range (50):
            user = fake.simple_profile()
            new_user = User(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                username = user['username'],
                email = fake.email(),
            )
            new_user.password_hash = 'password123'

            bar()
            db.session.add(new_user)
        db.session.commit()

def seed_festivals():
    print('\nseeding festivals 🧑‍🎤 \n')
    Faker.seed(0)
    with alive_bar(25) as bar:
        for i in range(25):
            new_festival = Festival(
                name = str(' '.join(fake.words(nb=3))).title(),
                address = fake.street_address(),
                city = fake.city(),
                state = fake.state_abbr(),
                date = fake.date_this_decade(before_today=False, after_today=True),
                website = fake.domain_name()
            )
            bar()
            db.session.add(new_festival)
        db.session.commit()

def seed_lineups():
    print('\ncreating lineups... ✨\n')
    Faker.seed(0)
    lineup_pairs = set()
    num_lineups = 750
    with alive_bar(num_lineups) as bar:
        while len(lineup_pairs) < num_lineups:
            festival_id = randint(1, 25)
            artist_id = randint(1, 500)

            pair = (festival_id, artist_id)

            if pair not in lineup_pairs:
                lineup_pairs.add(pair)
                artist_signing = Lineup(festival_id=festival_id, artist_id=artist_id)
                db.session.add(artist_signing)
                bar()
        db.session.commit()

def seed_favorites():
    print('\nAssigning Favorites 💖\n')
    Faker.seed(0)
    favorite_artists = set()
    with alive_bar(2000) as bar:
        while len(favorite_artists) < 2000:
            user_id = randint(1, 50)
            artist_id = randint(1, 500)

            pair = (user_id, artist_id)
            if pair not in favorite_artists:
                favorite_artists.add(pair)
                new_favorite = Favorite(
                    user_id = user_id,
                    artist_id = artist_id
                )
                db.session.add(new_favorite)
                bar()
        db.session.commit()

def seed_rsvps():
    print('\nSelling Festival Tickets 🎟️\n')
    sold_tickets = set()
    with alive_bar(300) as bar:
        while len(sold_tickets) < 300:
            user_id = randint(1,50)
            festival_id = randint(1, 25)
            pair = (user_id, festival_id)
            if pair not in sold_tickets:
                sold_tickets.add(pair)
                new_ticket = User_Festival(
                    user_id=user_id,
                    festival_id=festival_id
                )
                db.session.add(new_ticket)
                bar()
        db.session.commit()

def seed_songs_and_artists():
    print("\nseeding Artists, Songs, and relationships 🧑‍🎤🎶📝✨🥁\n")
    with alive_bar(3683) as bar:
        for artist_name, artist_data in artist_top_songs_dict.items():
            
            # Check if the artist already exists in the database
            artist = Artist.query.filter_by(name=artist_name).first()
            if not artist:
                artist = Artist(name=artist_name, spotify_id=artist_data["spotify_id"])
                db.session.add(artist)
                bar()

            # Commit the artist to the database
            db.session.commit()

            # Loop through the songs of the artist
            for song_name, song_spotify_id in artist_data["songs"].items():
                
                # Check if the song already exists in the database
                song = Song.query.filter_by(name=song_name).first()
                if not song:
                    song = Song(name=song_name, spotify_id=song_spotify_id)
                    db.session.add(song)
                    bar()

                # Commit the song to the database
                db.session.commit()

                # Check if the artist-song association already exists in the database
                song_artist_association = Song_Artist.query.filter_by(song_id=song.id, artist_id=artist.id).first()
                if not song_artist_association:
                    song_artist_association = Song_Artist(song_id=song.id, artist_id=artist.id)
                    db.session.add(song_artist_association)
                    bar()

                    # Commit the association to the database
                db.session.commit()


def clear_all():
    clear_table(Festival)
    clear_table(Artist)
    clear_table(Lineup)
    clear_table(Song)
    clear_table(Favorite)
    clear_table(User_Festival)
    clear_table(Song_Artist)



if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        clear_all()
        seed_festivals()
        seed_lineups()
        seed_favorites()
        seed_rsvps()
        seed_songs_and_artists()