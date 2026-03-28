"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""
from streaming.tracks import Track


class Artist:
    def __init__(self, artist_id, name, genre):
        self.tracks = []
        self.genre = genre
        self.name = name
        self.artist_id = artist_id

    def add_track(self, track):
        self.tracks.append(track)

    def track_count(self):
        if self.tracks == []:
            return 0
        else:
            return len(self.tracks)