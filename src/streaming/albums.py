"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""


class Album:
    def __init__(self, album_id, title, artist, release_year):
        self.tracks = []
        self.release_year = release_year
        self.artist = artist
        self.title = title
        self.album_id = album_id
        self.tra_ids = set()

    def add_track(self, track):
        self.tracks.insert(0,track)
        track.album = self
        self.tracks = sorted(self.tracks, key=lambda x: x.track_number)

    def track_ids(self):
        return {track.track_id for track in self.tracks}

    def duration_seconds(self):
        if not self.tracks:
            return 0
        a = 0
        for i in self.tracks:
            a += i.duration_seconds
        return a