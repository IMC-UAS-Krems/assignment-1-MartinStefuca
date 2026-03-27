"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from streaming.tracks import AlbumTrack


class Album:
    def __init__(self, album_id, title, artist, release_year, tracks : list[AlbumTrack]):
        self.tracks = tracks
        self.release_year = release_year
        self.artist = artist
        self.title = title
        self.album_id = album_id

    def add_track(self, track):
        pass

    def track_ids(self):
        pass

    def duration_seconds(self):
        pass