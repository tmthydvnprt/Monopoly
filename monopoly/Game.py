"""
Player.py - File for defining a Game class.
"""

import copy
import logging
import datetime
import textwrap
import numpy as np

from monopoly.Constants import TOTAL_MONEY, CARD_WIDTH, PROPERTY_INDX, PROPERTY_DEFS
from monopoly.Constants import GO, JAIL
from monopoly.Constants import ILLINOIS, ST_CHARLES, UTILITIES, RAILROADS, READING, BOARDWALK

from monopoly.Card import Card
from monopoly.Property import Property
from monopoly.Player import Player
from monopoly.Bank import Bank, FreeParking

# Create list of Property objects
PROPERTIES = [Property(**dict(zip(PROPERTY_INDX, p))) for p in PROPERTY_DEFS]

# Game Chance and Community Chest Cards
# Rule functin is called with a tuple of (player, game)
# pylint:disable=bad-whitespace
CHANCE_CARDS = [
    Card('Chance',                               'Advance to Go', lambda p, g, c: p.go_to_space(GO)),
    Card('Chance',                         'Advance to Illinois', lambda p, g, c: p.go_to_space(ILLINOIS)),
    Card('Chance',                'Advance to St. Charles Place', lambda p, g, c: p.go_to_space(ST_CHARLES)),
    Card('Chance',                  'Advance to Nearest Utility', lambda p, g, c: p.go_to_nearest(UTILITIES)),
    Card('Chance',                 'Advance to Nearest Railroad', lambda p, g, c: p.go_to_nearest(RAILROADS)),
    Card('Chance',                      'Bank pays you dividend', lambda p, g, c: p.add(50.0, g.bank)),
    Card('Chance',                        'Get out of Jail Free', lambda p, g, c: p.cards.append(c)),
    Card('Chance',                            'Go Back 3 Spaces', lambda p, g, c: p.go_to_space(p.position - 3)),
    Card('Chance',                                  'Go To Jail', lambda p, g, c: p.go_to_space(JAIL, pass_go=False, just_visiting=False)),
    Card('Chance',                        'Make General Repairs', lambda p, g, c: p.pay(25.0 * p.num_houses + 100.0 * p.num_hotels, g.freeparking)),
    Card('Chance',                                'Pay Poor Tax', lambda p, g, c: p.pay(15.0, g.freeparking)),
    Card('Chance',                 'Advance to Reading Railroad', lambda p, g, c: p.go_to_space(READING)),
    Card('Chance',                        'Advance to Boardwalk', lambda p, g, c: p.go_to_space(BOARDWALK)),
    Card('Chance', 'You have been elected Chairman of the Board', lambda p, g, c: map(p.pay, [50.0] * len(g.others(p)), g.others(p))),
    Card('Chance',                  'Your building loan matures', lambda p, g, c: p.add(150.0, g.bank)),
    Card('Chance',        'You have won a crossword competition', lambda p, g, c: p.add(100.0, g.bank))
]
COMMUNITY_CHEST_CARDS = [
    Card('Chest',                                 'Advance to Go', lambda p, g, c: p.go_to_space(GO)),
    Card('Chest',                      'Bank Error in Your Favor', lambda p, g, c: p.add(200.0, g.bank)),
    Card('Chest',                                'Doctor\'s fees', lambda p, g, c: p.pay(50.0, g.freeparking)),
    Card('Chest',                    'From Sale of Stock You Get', lambda p, g, c: p.add(50.0, g.bank)),
    Card('Chest',                          'Get out of Jail Free', lambda p, g, c: p.cards.append(c)),
    Card('Chest',                                    'Go To Jail', lambda p, g, c: p.go_to_space(JAIL, pass_go=False, just_visiting=False)),
    Card('Chest',                             'Grand Opera Night', lambda p, g, c: map(p.add, [50.0] * len(g.others(p)), g.others(p))),
    Card('Chest',                          'Holiday Fund Matures', lambda p, g, c: p.add(100.0, g.bank)),
    Card('Chest',                             'Income Tax Refund', lambda p, g, c: p.add(20.0, g.bank)),
    Card('Chest',                           'It is Your Birthday', lambda p, g, c: map(p.add, [10.0] * len(g.others(p)), g.others(p))),
    Card('Chest',                        'Life Insurance Matures', lambda p, g, c: p.add(100.0, g.bank)),
    Card('Chest',                              'Pay Hospital Fee', lambda p, g, c: p.pay(100.0, g.freeparking)),
    Card('Chest',                               'Pay School Fees', lambda p, g, c: p.pay(150.0, g.freeparking)),
    Card('Chest',                       'Receive Consultancy Fee', lambda p, g, c: p.add(25.0, g.bank)),
    Card('Chest',           'You are Assessed for Street Repairs', lambda p, g, c: p.pay(40.0 * p.num_houses + 115.0 * p.num_hotels, g.freeparking)),
    Card('Chest', 'You Have Won Second Prize in a Beauty Contest', lambda p, g, c: p.add(10.0, g.bank)),
    Card('Chest',                                   'You Inherit', lambda p, g, c: p.add(100.0, g.bank))
]
# pylint:enable=bad-whitespace

class Game(object):
    """Define the Game Monopoly."""

    def __init__(self, number, num_players):
        """Initialize a game."""
        self.number = number
        self.players = [Player(i, self) for i in xrange(num_players)]
        self.bankrupted = []
        self.bank = Bank(TOTAL_MONEY, self)
        self.freeparking = FreeParking(0.0, self, name='FreeParking', clipmoney=True)
        self.chance = copy.deepcopy(CHANCE_CARDS)
        self.community_chest = copy.deepcopy(COMMUNITY_CHEST_CARDS)
        self.properties = copy.deepcopy(PROPERTIES)
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0
        self.record = []
        # Shuffle the cards
        np.random.shuffle(self.chance)
        np.random.shuffle(self.community_chest)

    def __str__(self):
        """String print out of Game"""
        card_str = ['-' * CARD_WIDTH]
        card_str.append('Game {}'.format(self.number).center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)
        card_str.append(''.center(CARD_WIDTH))
        card_str.append(' Bank: ${} (x{})'.format(self.bank.money, self.bank.turnover).ljust(CARD_WIDTH))
        card_str.append(''.center(CARD_WIDTH))
        card_str.append(' Free Parking: ${}'.format(self.freeparking.money).ljust(CARD_WIDTH))
        card_str.append(''.center(CARD_WIDTH))
        card_str.append(' Players:'.ljust(CARD_WIDTH))
        for plyr in self.players:
            card_str.append(' Player {} @ {} (T: {}, R: {})'.format(plyr.number, plyr.position, plyr.turn, plyr.round).ljust(CARD_WIDTH))
            card_str.append(' M: ${}, P: {}'.format(plyr.money, len(plyr.properties)).ljust(CARD_WIDTH))
            card_str.append(' NW: ${}'.format(plyr.networth).ljust(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
        card_str.append(''.center(CARD_WIDTH))
        card_str.append('Chance Shuffle Order:'.ljust(CARD_WIDTH))
        card_str.extend([_.ljust(CARD_WIDTH) for _ in textwrap.wrap(str(self.chance), CARD_WIDTH)])
        card_str.append(''.center(CARD_WIDTH))
        card_str.append('Community Chest Shuffle Order:'.ljust(CARD_WIDTH))
        card_str.extend([_.ljust(CARD_WIDTH) for _ in textwrap.wrap(str(self.community_chest), CARD_WIDTH)])
        card_str.append(''.center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)
        return '\n'.join('|{}|'.format(l) for l in card_str)

    def __repr__(self):
        return 'Game {}'.format(self.number)

    @property
    def ranking(self):
        """Determine the Game rankings."""
        return sorted(self.players, key=lambda x: x.networth, reverse=True)

    @property
    def winner(self):
        """Determine the Game winner."""
        return self.ranking[0]

    def others(self, player=None):
        """Return the other players."""
        return [plyr for plyr in self.players if plyr is not player]

    def get_property(self, number=0):
        """Get a property position from Game's property list."""
        indx = [i for i, prop in enumerate(self.properties) if number == prop.loc]
        return self.properties.pop(indx[0]) if indx else None

    def auction(self, number=0):
        """Allow players to auction properties."""
        current_bid = 0
        bidders = copy.copy(self.players)
        # Bid until only one bidder left
        while len(bidders) > 1:
            for i, plyr in enumerate(bidders):
                bid = plyr.bid(number, 0)
                if bid > current_bid:
                    current_bid = bid
                    logging.debug('Player %s has the current bid ($%s).', plyr.number, current_bid)
                if bid < current_bid:
                    bidders.pop(i)
                    logging.debug('Player %s bid too low, done bidding ($%s < $%s).', plyr.number, bid, current_bid)
        # Best bidder buys property
        logging.debug('Player %s won the bid at $%s.', bidders[0].number, current_bid)
        bidders[0].buy_property(number, current_bid)

    def play_game(self, max_rounds=100):
        """Play the game."""
        self.start_time = datetime.datetime.now()
        logging.info('Game %s starting at %s', self.number, self.start_time)
        rounds = 1
        while len(self.players) > 1 and rounds < max_rounds:
            logging.debug('Round %s', rounds)
            # Each round all players take a turn
            for plyr in self.players:
                plyr.take_turn()
                # Between each turn, all players have opportunity to develop
                for plyr in self.players:
                    plyr.develop()
            rounds += 1
        self.end_time = datetime.datetime.now()
        self.elapsed_time = self.end_time - self.start_time
        logging.info('Game %s ended at %s', self.number, self.end_time)
        if rounds >= max_rounds:
            logging.info('Game %s ended due to Max Rounds (%s).', self.number, max_rounds)
        else:
            logging.info('Game %s had %s rounds played.', self.number, rounds)
            logging.info('Game %s ended due to bankruptcy.', self.number, )
        logging.info('Player %s is the winner of Game %s!', self.winner.number, self.number)
        logging.info('Game %s took %s s', self.number, self.elapsed_time)
        return self.record

    @staticmethod
    def draw_card(deck=None):
        """Draw a card from the top of a deck then replace it on the bottom. Return the card."""
        card = deck.pop(0)
        if card.name is not 'Get out of Jail Free':
            deck.append(card)
        return card

    def draw_chance(self):
        """Draw a Chance Card."""
        return self.draw_card(self.chance)

    def draw_community_chest(self):
        """Draw a Cummunity Chest Card."""
        return self.draw_card(self.community_chest)
