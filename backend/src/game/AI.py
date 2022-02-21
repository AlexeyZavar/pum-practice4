import uuid

from src import Player, Session
from src.server import User

AI_AVATAR = 'https://avatarfiles.alphacoders.com/307/307892.png'


class AI(Player):
    def __init__(self):
        bot_id = uuid.uuid4().hex
        super().__init__(User(bot_id, name=f'AI ({bot_id})', password='', avatar=AI_AVATAR, wins=69, looses=1338))

    def get_move(self, session: Session):
        pass
