import json
import os
from xmlrpc.client import ResponseError
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

spotify_token = os.getenv('SPOTIFY_TOKEN')
spotify_user_id = os.getenv('SPOTIFY_USER_ID')
spotify_playlist_id = os.getenv('SPOTIFY_PLAYLIST_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


class CreatePlaylist:
    def __init__(self):
        self.songs = []
        self.playlist_id = spotify_playlist_id
        self.spotify_token = spotify_token

    def authentication_spotify(self):
        """Authentication with Spotify"""
        query = "https://accounts.spotify.com/api/token"

        hash = base64.b64encode(
            f'{client_id}:{client_secret}'.encode('ascii')).decode('ascii')

        response = requests.post(
            query,
            data={
                "grant_type": "client_credentials",
                "scope": "playlist-modify-public playlist-modify-private"
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic {}".format(hash)
            }
        )

        print(response)

        response_json = response.json()

        print(response_json)

        self.spotify_token = response_json["access_token"]

        return response_json["access_token"]

    def create_playlist(self):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": "Chat Liked Songs",
            "description": "All liked songs from Chat",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        print(response)
        response_json = response.json()

        # playlist id
        print(response_json["id"])

        return response_json["id"]

    def get_spotify_uri(self, song_name, artist, owner):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )

        try:
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            print(response)
            response_json = response.json()
            songs = response_json["tracks"]["items"]

            if songs:
                # only use the first song
                uri = songs[0]["uri"]

                song = {
                    "uri": uri,
                    "owner": owner
                }

                self.songs.append(song)

                return song['uri']

            else:
                return None

        except ResponseError:
            raise ResponseError

    def add_song_to_playlist(self, uri):
        """Add all liked songs into a new Spotify playlist"""

        # collect all of uri

        # create a new playlist
        if self.playlist_id:
            playlist_id = self.playlist_id
        else:
            playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps([uri])

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        print(response)

    def get_player_state(self):

        query = "https://api.spotify.com/v1/me/player"

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        print(response)

        response_json = response.json()

        uri = response_json["item"]["uri"]

        return uri

    def skip_song(self):

        query = 'https://api.spotify.com/v1/me/player/next'

        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        print(response)
