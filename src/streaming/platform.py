"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import timedelta, datetime

from requests import session

from streaming.albums import Album
from streaming.artists import Artist
from streaming.playlists import Playlist, CollaborativePlaylist
from streaming.sessions import ListeningSession
from streaming.tracks import Track, Song, AlbumTrack
from streaming.users import User, PremiumUser, FreeUser, FamilyMember, FamilyAccountUser


class StreamingPlatform:
    def __init__(self, name):
        self._catalogue = {} #dict[str, Track]
        self._users = {} #dict[str, User]
        self._artists = {} #dict[str, Artist]
        self._albums = {} #dict[str, Album]
        self._playlists = {} #dict[str, Playlist]
        self._sessions = [] #list[ListeningSession]
        self.name = name

    def add_track(self, track):
        self._catalogue.update({track.track_id:track})

    def add_user(self, user):
        self._users.update({user.user_id:user})

    def add_artist(self, artist):
        self._artists.update({artist.artist_id:artist})

    def add_album(self, album):
        self._albums.update({album.album_id:album})

    def add_playlist(self, playlist):
        self._playlists.update({playlist.playlist_id:playlist})

    def record_session(self, session):
        self._sessions.append(session)

    def get_track(self, track_id):
        return self._catalogue[track_id]

    def get_user(self, user_id):
        return self._users[user_id]

    def get_artist(self, artist_id):
        return self._artists[artist_id]

    def get_album(self, album_id):
        return self._albums[album_id]

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self._catalogue.values())


# Q1
    def total_listening_time_minutes(self,start,end):
        total_listening = 0
        for ses in self._sessions:
            if start <= ses.timestamp <= end:
                total_listening += ses.duration_listened_seconds

        return total_listening/60

# Q2
    def avg_unique_tracks_per_premium_user(self, days=0):
        time = datetime.now().replace(microsecond=0) - timedelta(days=days)
        all_unique_set = set()
        premium_user_count = 0
        for i in self._sessions:
            if i.timestamp > time and isinstance(i.user, PremiumUser):
                all_unique_set.add(i.track.track_id)
        for i in self.all_users():
            if isinstance(i, PremiumUser):
                premium_user_count += 1
        if premium_user_count != 0:
            result = len(all_unique_set)/premium_user_count
            return result
        elif days == 0:
            return 0.0
        else:
            return 0.0

# Q3
    def track_with_most_distinct_listeners(self):
        track_unique_users = {}
        for i in self._sessions:
            if i.track.track_id not in track_unique_users:
                track_unique_users.update({i.track.track_id:[]})
            else:
                if i.user not in track_unique_users[i.track.track_id]:
                    track_unique_users[i.track.track_id].append(i.user)
        if track_unique_users == {}:
            return None
        return self.get_track(max(track_unique_users, key=lambda x: len(x[1])))

    # Q4
    def avg_session_duration_by_user_type(self):
        # counts per user type
        d = {
            "PremiumUser":0,
             "FreeUser":0,
             "FamilyAccountUser":0
            }
        for i in self._users.values():
            if isinstance(i, PremiumUser):
                d["PremiumUser"] += 1
            elif isinstance(i, FreeUser):
                d["FreeUser"] += 1
            else:
                d["FamilyAccountUser"] += 1
        time_per_type = {
            "PremiumUser": 0,
            "FreeUser": 0,
            "FamilyAccountUser": 0
        }
        for i in self._sessions:
            if isinstance(i.user, PremiumUser):
                time_per_type["PremiumUser"] += i.duration_listened_seconds
            elif isinstance(i.user, FreeUser):
                time_per_type["FreeUser"] += i.duration_listened_seconds
            else:
                time_per_type["FamilyAccountUser"] += i.duration_listened_seconds

            a = time_per_type["PremiumUser"]/d["PremiumUser"]
            b = time_per_type["FreeUser"]/d["FreeUser"]
            c = time_per_type["FamilyAccountUser"]/d["FamilyAccountUser"]


        return sorted([("PremiumUser",a),("FreeUser",b),("FamilyAccountUser",c)],key= lambda x: x[1], reverse=True)

# Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold=0):
        if age_threshold == 0:
            return 0.0
        total = 0.0
        for i in self._sessions:
            if isinstance(i.user, FamilyMember) and i.user.age < age_threshold:
                total += i.duration_listened_seconds/60
        return total

# Q6
    def top_artists_by_listening_time(self, n):
        artist_listening_min = {}
        for i in self._artists.values():
            artist_listening_min.update({i.artist_id:0.0})
        for i in self._sessions:
            if isinstance(i.track, Song):
                artist_listening_min[i.track.artist.artist_id] += i.duration_listened_seconds /60
        result = []
        for i,j in artist_listening_min.items():
            result.append((self.get_artist(i),j))

        a = sorted(result,key= lambda x: x[1], reverse=True)[:n]
        return a
# Q7
    def user_top_genre(self, user_id):
        if user_id not in self._users:
            return None
        user_genres_time = []
        for i in self._sessions:
            if i.user.user_id == user_id:
                user_genres_time.append((i.track.genre, i.duration_listened_seconds))
        total_listening = 0
        for i in user_genres_time:
            total_listening += i[1]
        top_genre = max(user_genres_time, key= lambda x: x[1])
        return top_genre[0], top_genre[1] / total_listening *100

# Q8
    def collaborative_playlists_with_many_artists(self, threshold=0):
        result = []
        actual_result = []
        for i in self._playlists.values():
            artist_unique = set()
            for track in i.tracks:
                if isinstance(track, Song):
                    artist_unique.add(track.artist.artist_id)
            result.append((i,len(artist_unique)))
        for i in result:
            if i[1] > threshold:
                actual_result.append(i[0])

        return actual_result

# Q9
    def avg_tracks_per_playlist_type(self):
        calculation = []
        for i in self._playlists.values():
            if type(i) == CollaborativePlaylist:
                calculation.append(("CollaborationPlaylist",len(i.tracks)))
            else:
                calculation.append(("Playlist",len(i.tracks)))

        playlist_count = 0
        collab_count = 0
        play_track_count = 0
        collab_track_count = 0
        for i in calculation:
            if i[0] == "Playlist":
                playlist_count += 1
                play_track_count += i[1]
            else:
                collab_count += 1
                collab_track_count += i[1]
        if playlist_count != 0:
            a = play_track_count / playlist_count
        else:
            a = 0.0
        if collab_count != 0:
            b = collab_track_count / collab_count
        else:
            b = 0.0
        result_dict = {
            "Playlist": a,
            "CollaborativePlaylist": b
        }
        return result_dict

# Q10 Not working yet
    def users_who_completed_albums(self):
        result = []
        d = {}
        albums_set_dic = {}
        for i in self._sessions:
            a = set()
            if isinstance(i.track, AlbumTrack):
                if i.user.user_id not in d:
                    d.update({i.user.user_id:set()})
                else:
                    d[i.user.user_id].add(i.track.title)
                for j in i.track.album.tracks:
                    a.add(j.title)
            if i.user.user_id not in albums_set_dic:
                albums_set_dic.update({i.user.user_id: []})
            else:
                albums_set_dic[i.user.user_id].append(i.track.title)
        for i in d.keys():
            for j in albums_set_dic.keys():
                if i == j:
                    for k in albums_set_dic[j]:
                        if d[i].union(k) == d[i]:
                            for l in range(len(result)):
                                if range(len(result)) == 0:
                                    result.append((self.get_user(i), [k[0].album.title]))
                                elif result[l][0] != i:
                                    result.append((self.get_user(i),[k[0].album.title]))
                                else:
                                    result[l][1].append(k[0].album.title)

        return result

