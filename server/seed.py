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

def seed_artists():
    print('\nseeding artists 🎶🎸🎹🎶\n')
    Faker.seed(0)
    with alive_bar(500) as bar:
        for i in range(500):
            new_artist = Artist(
                name = str(' '.join(fake.words(nb=3))).title()
            )
            bar()
            db.session.add(new_artist)
        db.session.commit()

def seed_songs():
    print('\nSeeding Songs 🎧\n')
    Faker.seed(0)
    with alive_bar(1500) as bar:
        for i in range(1500):
            new_song = Song(
                name = str(' '.join(fake.words(nb=5))).title()
            )
            bar()
            db.session.add(new_song)
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
    with alive_bar(1000) as bar:
        while len(sold_tickets) < 1000:
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

def seed_song_artists():
    print('\nWriting Music 📝🎼\n')
    artist_songs = set()
    
    with alive_bar(2000) as bar:
        for song_id in range(1, 1501):  
            artist_id = randint(1, 500) 
            pair = (artist_id, song_id) 
            artist_songs.add(pair)
            song_written = Song_Artist(
                song_id=song_id,
                artist_id=artist_id
            )
            db.session.add(song_written)
            bar()
    
        while len(artist_songs) < 2000:
            artist_id = randint(1, 500)
            song_id = randint(1, 1500)
            pair = (artist_id, song_id)
            if pair not in artist_songs:
                artist_songs.add(pair)
                song_written = Song_Artist(
                    song_id=song_id,
                    artist_id=artist_id
                )
                db.session.add(song_written)
                bar()
        
    db.session.commit()


def clear_all():
    clear_table(User)
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
        seed_users()
        seed_festivals()
        seed_artists()
        seed_lineups()
        seed_songs()
        seed_favorites()
        seed_rsvps()
        seed_song_artists()