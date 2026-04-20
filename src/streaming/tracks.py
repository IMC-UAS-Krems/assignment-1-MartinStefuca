"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""
from abc import ABC
from datetime import date


class Track(ABC):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds/60
    def __eq__(self, other):
        if isinstance(other, Track) and self.track_id == other.track_id:
            return True
        else:
            return False

class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.album = None
        self.track_number = track_number

class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date: date = release_date

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host, description = ""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.description: str = description
        self.host: str = host

class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, season, episode_number, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.episode_number: int = episode_number
        self.season: int = season

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, guest, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest

class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        super().__init__(track_id, title, duration_seconds, genre)
        self.narrator: str = narrator
        self.author: str = author
