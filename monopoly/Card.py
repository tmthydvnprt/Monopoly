#pylint:disable=too-few-public-methods
"""
Player.py - File for defining a Card class.
"""

from monopoly.Constants import CARD_WIDTH

class Card(object):
    """Defines a game card."""

    def __init__(self, deck='', name='', rule=None):
        """Initialize a card"""
        self.deck = deck
        self.name = name
        self.rule = rule

    def __str__(self):
        """String print out of card."""

        card_str = ['-' * CARD_WIDTH]
        card_str.append(''.center(CARD_WIDTH))
        card_str.append(self.deck.center(CARD_WIDTH))
        card_str.append(self.name.center(CARD_WIDTH))
        card_str.append(''.center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)

        return '\n'.join('|{}|'.format(l) for l in card_str)

    def __repr__(self):
        return '{} {}'.format(self.deck, self.name)
