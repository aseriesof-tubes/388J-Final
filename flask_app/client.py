import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Song(object):
    def __init__(self, track_json):
        self.title = track_json["name"]
        self.artists = [artist["name"] for artist in track_json["artists"]]
        self.album = track_json["album"]["name"]
        self.release_year = track_json["album"]["release_date"][:4]
        self.album_image_url = track_json["album"]["images"][0]["url"] if track_json["album"]["images"] else None
        self.track_id = track_json["id"]
        self.duration_ms = track_json["duration_ms"]
    def __repr__(self):
        return f"{self.title} by {', '.join(self.artists)}"


class SongClient(object):
    def __init__(self, id_key, secret_key):
        self.client = SpotifyClientCredentials(id_key, secret_key)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client)

    def search(self, search_query):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        results = self.sp.search(q=search_query, type="track", limit=5)
        tracks = results["tracks"]["items"]

        if not tracks:
            raise ValueError(f"No songs found for '{search_query}'.")

        songs = [Song(track) for track in tracks]
        return songs

    def get_song_features(self, track_id):
        """
        Retrieves detailed audio features for a given track ID.
        """
        track_features = self.sp.audio_features(track_id)[0]
        print(track_features)
        if track_features is None:
            raise ValueError(f"No features found for track ID '{track_id}'.")
        return track_features


## -- Example usage -- ###
if __name__ == "__main__":
    client_id = "f8576bd3cccf442d853261c942c0e81f"
    client_secret = "f946df74175c4864a8d0c171c802a4dd"
    client = SongClient(client_id, client_secret)

    search_query = "guardians"
    songs = client.search(search_query, limit=5)
    for song in songs:
        print(song)
