import datetime

from flask import Flask, request
from flask_jwt_extended import current_user, get_current_user
from flask_socketio import Namespace, join_room

from src.server.Authentication import ws_authenticated
from src.server.Database import DBSession, User
from src.server.sessions.LobbyHub import LobbyHub
from src.server.sessions.SessionHub import SessionHub

lobby_hub = LobbyHub()
session_hub = SessionHub()


def now():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


class KBPumNamespace(Namespace):
    def __init__(self, app: Flask):
        super().__init__('/')
        self.app = app

    @ws_authenticated
    def on_disconnect(self):
        self.app.logger.info('disconnected')

        if lobby_hub.has_lobby(current_user):
            lobby = lobby_hub.remove_user(current_user)
            self.emit('lobby_updated', lobby.dictify(), room=lobby.lobby_id)

        if session_hub.has_session(current_user):
            session = session_hub.get_session(current_user)
            session.remove_player(current_user)

            db_session = DBSession()
            user = db_session.get(User, current_user.id)
            user.looses += 1

            db_session.commit()

            self.emit('game_updated', session.dictify(), room=session.session_id)

    @ws_authenticated
    def on_create_lobby(self, message=None):
        self.app.logger.warn(f'User {current_user.name} creates lobby.')

        if lobby_hub.has_lobby(current_user):
            self.app.logger.warn('User tried to create a lobby while being in the lobby.')
            return

        lobby, lobby_user = lobby_hub.create_lobby(get_current_user())

        join_room(lobby.lobby_id)

        self.emit('lobby_created', {'lobby_id': lobby.lobby_id}, room=lobby.lobby_id)
        self.emit('lobby_updated', lobby.dictify(), room=lobby.lobby_id)

    @ws_authenticated
    def on_join_lobby(self, message=None):
        lobby_id = message['lobby_id']

        if lobby_hub.has_lobby(current_user):
            self.app.logger.warn('User tried to join a lobby while being in the lobby.')
            self.emit('lobby_probe', {'success': False}, room=request.sid)
            return

        if not lobby_hub.lobby_exists(lobby_id):
            self.app.logger.warn('User tried to join a nonexistent lobby.')
            self.emit('lobby_probe', {'success': False}, room=request.sid)
            return

        join_room(lobby_id)

        lobby, lobby_user = lobby_hub.add_user(lobby_id, get_current_user())

        self.emit('lobby_probe', {'success': True}, room=request.sid)
        self.emit('lobby_updated', lobby.dictify(), room=lobby_id)

    @ws_authenticated
    def on_lobby_user_ready_switch(self, message=None):
        lobby = lobby_hub.get_lobby_by_user(current_user)
        lobby.user_ready_switch(current_user)

        self.emit('lobby_updated', lobby.dictify(), room=lobby.lobby_id)

        if lobby.all_ready:
            session = lobby.create_session()
            session_hub.start(session)

            self.emit('game_updated', session.dictify(), room=lobby.lobby_id)
            self.emit('game_started', room=lobby.lobby_id)

    @ws_authenticated
    def on_game_send_message(self, message=None):
        session = session_hub.get_session(current_user)

        self.emit('game_new_message', {'user_id': current_user.id, 'date': now(), 'text': message['text']},
                  room=session.session_id)

    @ws_authenticated
    def on_game_make_move(self, message=None):
        session = session_hub.get_session(current_user)

        session.trigger_move(get_current_user(), **message)

        for message in session.messages_queue:
            self.emit('game_new_message', {'user_id': None, 'date': now(), 'text': message})

        session.messages_queue.clear()

        if session.ended:
            db_session = DBSession()

            alive = session.get_alive_players()

            for player in session.players:
                user = db_session.get(User, player.user.id)
                if player in alive:
                    user.wins += 1
                else:
                    user.looses += 1

            db_session.commit()

        self.emit('game_updated', session.dictify(), room=session.session_id)
