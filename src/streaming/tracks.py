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
class Track:
    def __init__(self, track_id, title, duration_seconds, genre):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        pass

class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number, album):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.album = album
        self.track_number = track_number

class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host, description):
        super().__init__(track_id, title, duration_seconds, genre)
        self.description = description
        self.host = host

class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, description, season, episode_number):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.episode_number = episode_number
        self.season = season

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, description, guest):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest

class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        super().__init__(track_id, title, duration_seconds, genre)
        self.narrator = narrator
        self.author = author
