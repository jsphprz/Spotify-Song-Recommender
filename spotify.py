import json
import requests
from song import Song

class SpotifyRecom:
    def __init__(self, token):
        self.token = token

    def get_last_played_tracks(self, limit=10):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Song(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"])
        for track in response_json["items"]]
        return tracks

    def get_track_recommendations(self, seed_tracks, limit=10):
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Song(track["name"], track["id"], track["artists"][0]["name"])
        for track in response_json["tracks"]]
        return tracks

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        return response