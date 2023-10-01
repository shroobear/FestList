# Standard library imports

# Remote library imports
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

# Local imports

# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SPOTIFY_CLIENT_SECRET'] = os.getenv("CLIENT_SECRET")
app.config['SPOTIFY_CLIENT_ID'] = os.getenv("CLIENT_ID")
app.config['SESSION_COOKIE_NAME'] = 'Spotify OAuth cookie'
app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

app.secret_key = b'\xe2\xac\x1aF\x01\xbd2\xe5V\xf4\xb6\x0c\xf4|\x90\x1b'

# Instantiate CORS
CORS(app)

# Instantiate OAuth
oauth = OAuth(app)

spotify = oauth.register(
    name='spotify',
    client_id= os.getenv("CLIENT_ID"),
    client_secret= os.getenv("CLIENT_SECRET"),
    access_token_url='https://accounts.spotify.com/api/token',
    access_token_params=None,
    authorize_url='https://accounts.spotify.com/authorize',
    authorize_params=None,
    api_base_url='https://api.spotify.com',
    userinfo_endpoint='https://api.spotify.com/v1/me',
    client_kwargs={'scope': 'user-read-private, user-read-email'}
)

# Instantiate bcrypt
bcrypt = Bcrypt(app)

host_port = "http://localhost:5555"