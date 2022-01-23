import uuid
from typing import Tuple, Dict

from src.server.Database import User
from src.server.sessions.Lobby import Lobby
from src.server.sessions.LobbyUser import LobbyUser


class LobbyHub:
    def __init__(self):
        self.lobbies: Dict[str, Lobby] = {}
        self.users: Dict[str, Lobby] = {}

    def create_lobby(self, creator: User) -> Tuple[Lobby, LobbyUser]:
        lobby_id = uuid.uuid4().hex[:8]
        lobby = Lobby(lobby_id)

        self.lobbies[lobby_id] = lobby
        _, lobby_user = self.add_user(lobby_id, creator)

        return lobby, lobby_user

    def has_lobby(self, user: User) -> bool:
        return user.id in self.users

    def lobby_exists(self, lobby_id: str) -> bool:
        return lobby_id in self.lobbies

    def add_user(self, lobby_id: str, user: User) -> Tuple[Lobby, LobbyUser]:
        lobby = self.lobbies[lobby_id]
        lobby_user = lobby.add_user(user)

        self.users[user.id] = lobby

        return lobby, lobby_user

    def remove_user(self, user: User) -> Lobby:
        lobby = self.users.pop(user.id)
        lobby.remove_user(user)

        return lobby

    def get_lobby(self, user: User) -> Lobby:
        return self.users[user.id]
