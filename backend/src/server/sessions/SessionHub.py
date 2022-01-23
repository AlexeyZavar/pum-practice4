from typing import Dict

from src.game.Session import Session


class SessionHub:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def start(self, session: Session):
        pass
