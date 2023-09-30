#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker
from alive_progress import alive_bar, alive_it
from flask_bcrypt import bcrypt

# Local imports
from app import app
from models import db, User, Festival, Artist, Lineup, Song, Song_Artist, Favorite


fake = Faker()

def clear_table(table_class):
    db.session.query(table_class).delete()
    db.session.commit()

def seed_users():
    print("Seeding Users 👥\n")
    Faker.seed(0)
    with alive_bar(50) as bar:
        for i in range (50):
            user = fake.simple_profile()
            password = 'password123'
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                username = user['username'],
                email = fake.email(),
                password_hash = hashed_password
            )
            bar()
            db.session.add(new_user)
        db.session.commit()

def seed_festivals():
    print('seeding festivals 🎫')
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
    print('seeding artists 🎶🎸🎹🎶')
    with alive_bar(200) as bar:
        for i in range(200):
            new_artist = Artist(
                name = str(' '.join(fake.words(nb=3))).title()
            )
            bar()
            db.session.add(new_artist)
        db.session.commit()

def clear_all():
    clear_table(User)
    clear_table(Festival)
    clear_table(Artist)


if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        clear_all()
        seed_users()
        seed_festivals()
        seed_artists()