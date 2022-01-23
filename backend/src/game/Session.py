import logging
import sys
from typing import List, Dict

from .AirshipRequest import AirshipRequest
from .AirshipsSellRequest import AirshipsSellRequest
from .GameException import GameException
from .MarketState import MarketState
from .OreRequest import OreRequest
from .Player import Player
from .WorkshopBuildRequest import WorkshopBuildRequest
from ..server.Database import User

AIRSHIP_COST = 2_000_000
WORKSHOP_COST = 5_000_000

logger = logging.getLogger('Session')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class Session:
    def __init__(self, session_id: str, players: List[Player]):
        self.session_id: str = session_id
        self.players: List[Player] = players

        self.month: int = 1

        self.ore_requests: List[OreRequest] = []
        self.airship_requests: List[AirshipRequest] = []
        self.sell_requests: List[AirshipsSellRequest] = []
        self.workshop_requests: Dict[WorkshopBuildRequest, int] = {}

        self.market_state: MarketState = MarketState()

        logger.info(f'Initialized Session with ID: {self.session_id}')

    def get_alive_players(self):
        return list(filter(lambda x: not x.dead, self.players))

    def get_player(self, user: User):
        for item in self.players:
            if item.user.id == user.id:
                return item

    @property
    def p(self):
        return len(self.get_alive_players())

    def trigger_next_month(self):
        logger.info('Next month triggered')

        # EVENT 1
        # ore requests
        self.trigger_ore_requests()

        # EVENT 2
        # sell requests
        self.trigger_airships_sell()

        # EVENT 3
        # expenses paying
        for player in self.get_alive_players():
            player.event_store_ore()
            player.event_store_airships()
            player.event_store_workshops()

        # EVENT 4
        # market state determining
        self.market_state.set_random_state()
        logger.info(f'New market state: {self.market_state}')

        # EVENT 5
        # build airships
        self.trigger_airships_build()

        # EVENT 6
        # build workshops
        self.trigger_workshops_build()

        # and finally kill players with money < 0
        self.kill_players()

        self.month += 1

    def kill_players(self):
        for player in self.players:
            if player.money < 0:
                player.dead = True

                logger.info(f'{player} is dead now')

    def trigger_workshops_build(self):
        done = []

        for request, month in self.workshop_requests.items():
            if month == 4:
                player = self.get_player(request.user)
                player.trigger_workshop_build()

                done.append(request)

                logger.info(f'Built workshop for {request.user}')
            else:
                self.workshop_requests[request] += 1

                logger.info(f'Increase workshop month for {request.user}')

        for item in done:
            del self.workshop_requests[item]

    def trigger_airships_build(self):
        for request in self.airship_requests:
            player = self.get_player(request.user)
            player.airships += request.amount

            logger.info(f'Built {request.amount} airships for {player}')

    def trigger_ore_requests(self):
        logger.info('Ore requests triggered')
        amount = self.market_state.state['total_ore'](self.p)
        logger.info(f'Available ore: {amount}')

        while amount > 0 and self.ore_requests:
            highest = max(self.ore_requests, key=lambda r: r.price)
            predicates = [request for request in self.ore_requests if request.price == highest.price]
            logger.info(f'Highest: {highest}, predicates: {predicates}')

            for request in predicates:
                if amount <= 0:
                    break

                # if bank has fewer amount
                if amount - request.amount < 0:
                    satisfied = amount
                else:
                    satisfied = request.amount

                amount -= satisfied

                player = self.get_player(request.user)
                player.trigger_ore_request(satisfied, request.price)

                logger.info(f'Satisfied {satisfied} for {player} with price {request.price}')

                self.ore_requests.remove(request)

        logger.info(f'Remaining: {amount}')

        self.ore_requests.clear()

    def trigger_airships_sell(self):
        logger.info('Airships sell triggered')
        amount = self.market_state.state['airships_demand'](self.p)
        logger.info(f'Can buy: {amount}')

        while amount > 0 and self.sell_requests:
            lowest = min(self.sell_requests, key=lambda r: r.price)
            predicates = [request for request in self.sell_requests if request.price == lowest.price]
            logger.info(f'Lowest: {lowest}, predicates: {predicates}')

            for request in predicates:
                if amount <= 0:
                    break

                # if bank has fewer amount
                if amount - request.amount < 0:
                    satisfied = amount
                else:
                    satisfied = amount - request.amount

                amount -= satisfied

                player = self.get_player(request.user)
                player.trigger_sell_request(satisfied, request.price)

                logger.info(f'Satisfied {satisfied} for {player} with price {request.price}')

                self.sell_requests.remove(request)

        logger.info(f'Remaining: {amount}')

        self.sell_requests.clear()

    def event_request_ore(self, user: User, amount: int, price: int):
        if not (self.market_state.state['minimal_price'] <= price) or not (
                0 < amount <= self.market_state.state['total_ore'](self.p)):
            raise GameException()

        request = OreRequest(user, amount, price)
        self.ore_requests.append(request)

        logger.info(f'event_request_ore: {request}')

    def event_request_airship_build(self, user: User, amount: int):
        player = self.get_player(user)

        total_cost = amount * AIRSHIP_COST
        total_ore = amount

        if amount <= 0 or total_ore > player.ore or total_cost > player.money:
            raise GameException()

        player.money -= total_cost
        player.ore -= amount

        request = AirshipRequest(user, amount)
        self.airship_requests.append(request)

        logger.info(f'event_request_airship_build: {request}')

    def event_request_sell(self, user: User, amount: int, price: int):
        player = self.get_player(user)

        if player.airships < amount:
            raise GameException()

        request = AirshipsSellRequest(user, amount, price)
        self.sell_requests.append(request)

        logger.info(f'event_request_sell: {request}')

    def event_request_workshop_build(self, user: User):
        player = self.get_player(user)

        if player.money < WORKSHOP_COST:
            raise GameException()

        player.money -= WORKSHOP_COST

        request = WorkshopBuildRequest(user)
        self.workshop_requests[request] = 0

        logger.info(f'event_request_workshop_build: {request}')

    def dictify(self):
        return {
            'id': self.session_id,
            'players': [player.dictify() for player in self.players],
            'month': self.month,
            'market_state': self.market_state.dictify(self.p),
        }

    def __str__(self):
        return f'Session (session_id={self.session_id}, month={self.month}, market_state={self.market_state}, players={self.players})'
