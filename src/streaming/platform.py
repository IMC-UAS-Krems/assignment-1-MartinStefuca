"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from streaming.albums import Album
from streaming.artists import Artist
from streaming.playlists import Playlist
from streaming.sessions import ListeningSession
from streaming.tracks import Track
from streaming.users import User



class StreamingPlatform:
    def __init__(self, name, _catalogue : dict[str, Track], _users : dict[str, User], _artists : dict[str, Artist], _albums : dict[str, Album], _playlists : dict[str, Playlist], _sessions : list[ListeningSession]):
        self.name = name

    def add_track(self, track):
        pass

    def add_user(self, user):
        pass

    def add_artist(self, artist):
        pass

    def add_album(self, album):
        pass

    def add_playlist(self, playlist):
        pass

    def record_session(self, session):
        pass

    def get_track(self, track_id):
        pass

    def get_user(self, user_id):
        pass

    def get_artist(self, artist_id):
        pass

    def get_album(self, album_id):
        pass

    def all_users(self):
        pass

    def all_tracks(self):
        pass
