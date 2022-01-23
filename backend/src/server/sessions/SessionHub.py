from typing import Dict

from src.game.Session import Session
from src.server.Database import User


class SessionHub:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.users: Dict[str, Session] = {}

    def start(self, session: Session):
        self.sessions[session.session_id] = session

        for player in session.players:
            self.users[player.user.id] = session

    def get_session(self, user: User):
        return self.users[user.id]

    def has_session(self, user: User):
        return user.id in self.users
