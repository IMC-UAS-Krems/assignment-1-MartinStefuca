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
    def __init__(self, playlist_id: str, name:str, owner: User):
        self.tracks: list[Track] = []
        self.owner = owner
        self.name = name
        self.playlist_id = playlist_id

    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)
        else:
            return

    def remove_track(self, track_id):
        for i in self.tracks:
            if i.track_id == track_id:
                self.tracks.remove(i)
                break

    def total_duration_seconds(self) -> int:
        total = 0
        for i in self.tracks:
            total += i.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner):
        super().__init__(playlist_id, name, owner)
        self.contributors: list[User] = [owner]

    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)
        else:
            return

    def remove_contributor(self, user):
        if user != self.owner:
            self.contributors.remove(user)
