import requests
import os


# Token Refresh Logic
def refresh_spotify_token(refresh_token):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, data=token_data)
    response_data = response.json()

    new_token = response_data.get("access_token")
    if new_token:
        return new_token
    else:
        print("Error refreshing token:", response_data.get("error_description"))
        return None


# Get Artist's Top Tracks Method
def get_top_tracks(artist_id, access_token, market="US"):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market={market}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        refresh_token = "AQAq0fl-k9q9NZ3xHJc8d3RgiLw5r6xUmuhgQnZt8idE320CAEm7rk4q3dN9wBGxbXsuzdDWt_8HiW71N5rwLWv3W27VCCJNaRxdfvX18-_oNJslOQ_w0R98CwnS4Urxowk"
        new_token = refresh_spotify_token(refresh_token)
        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Error getting top tracks for artist {artist_id}: {response.json().get('error_description')}"
        )
        return {}

    tracks = {track["name"]: track["id"] for track in response.json().get("tracks", [])}
    return tracks


def populate_songs_from_artists(artist_dict, access_token):
    songs_by_artist = {}
    for artist_name, artist_id in artist_dict.items():
        top_tracks = get_top_tracks(artist_id, access_token)
        if top_tracks:
            songs_by_artist[artist_name] = {
                "spotify_id": artist_id,
                "songs": top_tracks,
            }

    return songs_by_artist


artist_dict = {
    "The Beatles": "3WrFJ7ztbogyGnTHbHJFl2"
    # ... (other artists can be added here) ...
}

# Assuming you've already got an access_token
access_token = "YOUR_INITIAL_ACCESS_TOKEN"
resulting_structure = populate_songs_from_artists(artist_dict, access_token)

print(resulting_structure)
