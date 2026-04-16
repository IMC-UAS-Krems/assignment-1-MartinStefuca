"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import AlbumTrack
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist

# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels",    genre="pop")
    david  = Artist("a2", "David",    genre="rock")
    bruno  = Artist("a3", "Bruno",    genre="pop")
    for i in (pixels, david, bruno):
        platform.add_artist(i)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)

    best_album = Album("alb2", "Yes Best", artist=david, release_year=2023)
    td1 = AlbumTrack("td1", "Rain", 180, "rock", david, track_number=1)
    td2 = AlbumTrack("td2", "Horizon", 210, "rock", david, track_number=2)
    td3 = AlbumTrack("td3", "Fields", 200, "rock", david, track_number=3)
    for track in (td1, td2, td3):
        best_album.add_track(track)
        platform.add_track(track)
        david.add_track(track)
    platform.add_album(best_album)


    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    jon   = PremiumUser("u3", "JON",   age=30, subscription_start=date(2024, 1, 1))
    mom   = FamilyAccountUser("u4", "mother", 40)
    son   = FamilyMember("u5", "Sonny", 8,mom)

    for user in (alice, bob, jon,mom,son):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # Collaborative playlist
    # ------------------------------------------------------------------
    col_playlist1 = CollaborativePlaylist("p1", "fav_songs",bob)
    col_playlist1.add_track(t1)
    col_playlist1.add_track(t2)
    col_playlist1.add_track(t3)

    col_playlist2 = CollaborativePlaylist("p2", "best_songs",bob)
    col_playlist2.add_track(t1)
    col_playlist2.add_track(t2)
    col_playlist2.add_track(td3)

    standard_play = Playlist("p3", "Normal", mom)
    standard_play.add_track(td2)
    standard_play.add_track(td3)

    standard_play2 = Playlist("p4", "Usual", alice)
    standard_play2.add_track(td1)


    for i in (col_playlist1, col_playlist2, standard_play, standard_play2):
        platform.add_playlist(i)

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------
    s1 = ListeningSession("s1", bob, t1, RECENT, 180) # premium
    s2 = ListeningSession("s2", jon, t1, RECENT, 180) # premium
    s_3 = ListeningSession("s3", alice, t1, RECENT, 180) #free
    s_4 = ListeningSession("s4", alice, t2, RECENT, 180) #free
    s_5 = ListeningSession("s5", mom, t2, OLD, 180) #FamilyAccount
    s_6 = ListeningSession("s6", son, t2, OLD, 210) #FamilyMember
    s7 = ListeningSession("s7", alice, t3, RECENT, 180) #free




    for i in (s1, s_3, s2, s_4, s_5, s_6, s7):
        platform.record_session(i)


    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
