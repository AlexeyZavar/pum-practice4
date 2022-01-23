import uuid

from src.game.Player import Player
from src.game.Session import Session
from src.server.Database import User

USER1 = User()
USER1.id = uuid.uuid4().hex
USER1.name = 'Alexey1'

USER2 = User()
USER2.id = uuid.uuid4().hex
USER2.name = 'Sanya1'

players = [Player(USER1), Player(USER2)]
print(players)

s = Session(uuid.uuid4().hex, players)

s.event_request_ore(USER1, 4, 5_000_000)  # 1
s.event_request_ore(USER2, 3, 6_000_000)  # 3
print('-' * 120)
s.event_request_sell(USER1, 1, 8_000_000)
s.event_request_sell(USER2, 2, 4_000_000)
print('-' * 120)
s.event_request_airship_build(USER1, 3)
s.event_request_airship_build(USER2, 2)
print('-' * 120)
s.trigger_next_month()
print('-' * 120)
print(players)
print('-' * 120)
s.event_request_sell(USER1, 2, 3_000_000)
s.event_request_sell(USER2, 2, 4_000_000)
print('-' * 120)
s.trigger_next_month()
print('-' * 120)
print(players)
