"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
from streaming.tracks import Track
from streaming.users import User


class Playlist:
    def __init__(self, playlist_id, name, owner, tracks : list[Track]):
        self.tracks = tracks
        self.owner = owner
        self.name = name
        self.playlist_id = playlist_id

    def add_track(self, track):
        pass

    def remove_track(self, track_id):
        pass

    def total_duration_seconds(self):
        pass

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner, tracks, contributors : list[User]):
        super().__init__(playlist_id, name, owner, tracks)
        self.contributors = contributors

    def add_contributor(self, user):
        pass

    def remove_contributor(self, user):
        pass
