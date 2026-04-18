"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import timedelta, datetime

from streaming.artists import Artist
from streaming.playlists import CollaborativePlaylist
from streaming.tracks import Song, AlbumTrack, Track
from streaming.users import PremiumUser, FreeUser, FamilyMember, FamilyAccountUser


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
    def total_listening_time_minutes(self,start,end) -> float:
        """Calculates the total listening time of all users"""

        total_listening = 0
        for ses in self._sessions:
            if start <= ses.timestamp <= end:
                total_listening += ses.duration_listened_seconds

        return float(total_listening/60)

    # Q2
    def avg_unique_tracks_per_premium_user(self,  days=30) -> float:
        """Calculates distinct tracks per PremiumUser in the last n days.
           - Sums the number of unique tracks of every PremiumUser.
           - Divides it by the total number of PremiumUsers.
        """

        time = datetime.now().replace(microsecond=0) - timedelta(days=days)
        premium_user_count = 0
        number_of_tracks = 0
        dic_users_their_u_tracks = {}
        for i in self._sessions:
            if i.timestamp > time and isinstance(i.user, PremiumUser):   # for each premium user we get
                u_id = i.user.user_id                                    # user_id : {set of their unique tracks}
                if u_id not in dic_users_their_u_tracks:
                    dic_users_their_u_tracks[u_id] = set()
                dic_users_their_u_tracks[u_id].add(i.track.track_id)
        for i in self.all_users():
            if isinstance(i, PremiumUser):                 # total number of premium user
                premium_user_count += 1
        for tracks in dic_users_their_u_tracks.values():   # this part calculates the total number
            number_of_tracks += len(tracks)                #  of unique tracks per user
        if premium_user_count != 0:
            result = number_of_tracks/premium_user_count
            return result
        else:
            return 0.0  # if the number of days selected is 0 or there is 0 PremiumUsers

    # Q3
    def track_with_most_distinct_listeners(self) -> Track | None:
        """Return the track with the highest number of distinct listeners (not total plays).
            - Count the number of unique users who have listened to each track.
            - Return the one with the most.
            - Return None if no sessions exist.
        """

        if not self._sessions:  # no sessions
            return None
        track_unique_users = {}
        for i in self._sessions:
            if i.track.track_id not in track_unique_users:
                track_unique_users.update({i.track.track_id:set()})   # for each track we create ->
            track_unique_users[i.track.track_id].add(i.user.user_id)  # {track_id : {set of unique user_ids}}

        return self.get_track(max(track_unique_users, key=lambda x: len(x[1])))

    # Q4
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        """Calculates average session duration (in seconds) for each user type.
        - Return a list of (type_name, average_duration) tuples.
        - Sort results from longest to shortest duration.
        """

        di = {
            "PremiumUser":0,    # counts per user type
            "FreeUser":0,
            "FamilyAccountUser":0,
            "FamilyMember":0,
                                # total time per user type
            "PremiumUser_time": 0,
            "FreeUser_time": 0,
            "FamilyAccountUser_time": 0,
            "FamilyMember_time": 0,
        }
        for i in self._sessions:
            user = i.user
            if isinstance(user, PremiumUser):
                di["PremiumUser"] += 1
                di["PremiumUser_time"] += i.duration_listened_seconds
            elif isinstance(user, FreeUser):
                di["FreeUser"] += 1
                di["FreeUser_time"] += i.duration_listened_seconds
            elif isinstance(user, FamilyAccountUser):
                di["FamilyAccountUser"] += 1
                di["FamilyAccountUser_time"] += i.duration_listened_seconds
            else:
                di["FamilyMember"] += 1
                di["FamilyMember_time"] += i.duration_listened_seconds
        a = 0
        if di["PremiumUser"] != 0:                  # avoiding ZeroDivisioError
            a = di["PremiumUser_time"]/di["PremiumUser"]
        b = 0
        if di["FreeUser"] != 0:
            b = di["FreeUser_time"]/di["FreeUser"]
        c = 0
        if di["FamilyAccountUser"] != 0:
            c = di["FamilyAccountUser_time"]/di["FamilyAccountUser"]
        d = 0
        if di["FamilyMember"] != 0:
            d = di["FamilyMember_time"]/di["FamilyMember"]

        return sorted([("PremiumUser",a),("FreeUser",b),("FamilyAccountUser",c),("FamilyMember",d)],key= lambda x: x[1], reverse=True)

    # Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        """Sums the total listening time (minutes) of FamilyMember users under the age threshold.
        - Default threshold = 18.
        - Returns 0.0 if no underage users or their sessions exist.
        """
        if age_threshold == 0:   # not necessary, but no need to iterate if the threshold is 0
            return 0.0
        total = 0.0
        for i in self._sessions:
            if isinstance(i.user, FamilyMember) and i.user.age < age_threshold:
                total += i.duration_listened_seconds/60
        return total

    # Q6
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        """Returns ordered list of N tuples in the form (Artist, total_listening_time)
        from highest to lowest.
        - Only counting Song tracks
        """
        artist_listening_min = {}
        for i in self._artists.values():
            artist_listening_min.update({i.artist_id:0.0})
        for i in self._sessions:
            if isinstance(i.track, Song):
                artist_listening_min[i.track.artist.artist_id] += i.duration_listened_seconds /60
        result = []
        for i,j in artist_listening_min.items():
            result.append((self.get_artist(i),j))  # result -> [(Artist, listened_minutes), ...]
        if len(result) < n:
            print("There is not enough artists on the platform!")
            return list(sorted(result,key= lambda x: x[1], reverse=True))
        return list(sorted(result,key= lambda x: x[1], reverse=True))[:n]

    # Q7
    def user_top_genre(self, user_id) -> tuple[str, float] | None:
        """For a specific user, returns a tuple in the form (genre_name, percentage_of_total_time)
        - Returns None if user doesn't exist or has no sessions
        """
        if user_id not in self._users:
            return None
        user_genres_time = []
        for i in self._sessions:            # list of (genre, listening_time) tuples
            if i.user.user_id == user_id:   # for each listening session
                user_genres_time.append((i.track.genre, i.duration_listened_seconds))
        if not user_genres_time:  # no session -> None
            return None

        total_listening = 0    #total listening across all genres
        genre_time = {}
        for i in user_genres_time:
            total_listening += i[1]
            if i[0] not in genre_time:
                genre_time[i[0]] = 0
            genre_time[i[0]] += i[1]

        top_genre = max(genre_time, key= lambda x: x[1])

        return top_genre, genre_time[top_genre] / total_listening * 100

    # Q8
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        """Return all CollaborativePlaylist instances with more distinct artists than the threshold
        - Only counts Song tracks
        - Returns playlists in registration order
        - Returns [] when there is no CollaborativePlaylist with more distinct artists than the threshold
        """
        result = []
        for playlist in self._playlists.values():
            if isinstance(playlist,CollaborativePlaylist):
                artist_unique = set()
                for track in playlist.tracks: # for every playlist there is a set of unique artists
                    if isinstance(track, Song):
                        artist_unique.add(track.artist.artist_id)
                result.append((playlist,len(artist_unique)))
             # result is a list of tuples in the form (playlist, n_unique_artists)
        actual_result = []
        for i in result:
            if i[1] > threshold:
                actual_result.append(i[0])

        return actual_result

    # Q9
    def avg_tracks_per_playlist_type(self):
        """Computes the average number of tracks per playlist,
        distinguishing between standard Playlist and CollaborativePlaylist instances.
        - Returns a dictionary with keys "Playlist" and "CollaborativePlaylist"
        mapped to their respective averages.
        - Returns 0.0 for a type with no instances.
        """
        calculation = []
        for i in self._playlists.values():
            if type(i) == CollaborativePlaylist:
                calculation.append(("CollaborativePlaylist",len(i.tracks)))
            else:
                calculation.append(("Playlist",len(i.tracks)))

        playlist_count = 0     # number of playlists
        collab_count = 0       #

        play_track_count = 0   # number of tracks per playlist
        collab_track_count = 0 #
        for i in calculation:
            if i[0] == "Playlist":
                playlist_count += 1
                play_track_count += i[1]
            else:
                collab_count += 1
                collab_track_count += i[1]

        average_for_playlist = 0.0
        if playlist_count != 0:
            average_for_playlist = play_track_count / playlist_count
        average_for_collab_p = 0.0
        if collab_count != 0:
            average_for_collab_p = collab_track_count / collab_count

        result_dict = {
            "Playlist": average_for_playlist,
            "CollaborativePlaylist": average_for_collab_p
        }
        return result_dict

    # Q10
    def users_who_completed_albums(self):
        """Returns users who have listened to every track on at least one album
        - Returns (User, [album_titles]) tuples (with all completed albums listed)
        - Ignores albums with no tracks
        """
        # we need {user : {playlist : set{tracks of the playlist that the user has listened to}}}
        main_list = {} # something like: {'u2': [{'alb1': {'t1'}}], 'u1': [{'alb1': {'t1', 't3', 't2'}}], 'u3': [{'alb1': {'t1'}}], 'u4': [{'alb1': {'t2'}}], 'u5': [{'alb1': {'t2'}}]}
        for session in self._sessions:
            if isinstance(session.track, AlbumTrack):
                userID = session.user.user_id
                albumID = session.track.album.album_id
                trackID = session.track.track_id

                if userID not in main_list:
                    main_list.update( {userID:[] } )
                is_album_there = False
                for album_tracks in main_list[userID]:
                    if album_tracks[albumID]:
                        is_album_there = True
                        album_tracks[albumID].add(trackID)
                if not is_album_there:
                    main_list[userID].append({albumID:{trackID}})

        # let's create a list containing (album_id, number of tracks) tuples for every album
        album_tracks_n = [] #afterwards looks like: [('alb1', 3), ('alb2', 3)]
        for album in self._albums.values():
            album_tracks_n.append((album.album_id,len(album.tracks)))

        result = [] # becomes [('u1', {'alb1': {'t1', 't3', 't2'}})]
        for user, albums in main_list.items():
            for album in albums:
                for i in album_tracks_n:
                    if album.get(i[0]) and len (album[i[0]]) == i[1] and i[1] > 0:
                        result.append((user,album))

        result_dict = {} # {'u1': ['Digital Dreams']}
        for user_tuple in result:
            if user_tuple[0] not in result_dict: #user not in result_dict
                result_dict[user_tuple[0]] = []
            for album in user_tuple[1]:
                result_dict[user_tuple[0]].append(self.get_album(album).title)
        return_form = []
        for user, albums in result_dict.items():
            return_form.append((self.get_user(user),albums))

        return return_form