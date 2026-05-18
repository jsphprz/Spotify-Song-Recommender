import json
import requests
from song import Song

class SpotifyRecom:
    def __init__(self, token):
        self.token = token

    def get_top_tracks(self, limit=10):
        # time_range can be short_term, medium_term, or long_term
        url = f"https://api.spotify.com/v1/me/top/tracks?limit={limit}&time_range=medium_term"
        response = self._place_get_api_request(url)
        
        if response.status_code != 200:
            return [f"Error: {response.status_code} - {response.text.strip() or 'No details'}"]
            
        response_json = response.json()
        if "items" not in response_json or not response_json["items"]:
            return ["No top tracks found. Make sure you play some music on Spotify!"]
            
        # The /me/top/tracks endpoint returns track objects directly, unlike recently-played which wrapped them in a 'track' node
        tracks = [Song(track["name"], track["id"], track["artists"][0]["name"])
        for track in response_json["items"]]
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