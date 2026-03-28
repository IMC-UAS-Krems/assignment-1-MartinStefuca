"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from streaming.sessions import ListeningSession


class User:
    def __init__(self, user_id, name, age):
        self.sessions = []
        self.user_id = user_id
        self.name = name
        self.age = age
        self.unique_tracks = set()

    def add_session(self, session):
        self.sessions.append(session)
        self.unique_tracks.add(session.track.track_id)
    
    def total_listening_seconds(self):
        if len(self.sessions) == 0:
            return 0
        else:
            a = 0
            for i in self.sessions:
                a +=i.duration_listened_seconds
            return a
    
    def total_listening_minutes(self):
        return self.total_listening_seconds()/60
    
    def unique_tracks_listened(self):
        return self.unique_tracks
        
class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FreeUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.MAX_SKIPS_PER_HOUR = 6

class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        # parent is FamilyAccountUseer
        self.parent = parent

class FamilyAccountUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        self.sub_users.insert(0,self)
        return self.sub_users

