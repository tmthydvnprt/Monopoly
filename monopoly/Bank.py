"""
Player.py - File for defining a Bank  class.
"""

from monopoly.Constants import CARD_WIDTH, TOTAL_MONEY

class Bank(object):
    """Define a Bank for the Game."""

    def __init__(self, money=0, game=None, name='', clipmoney=False):
        """Initialize a Bank."""
        self.name = name if name else 'Bank'
        self.money = money
        self.game = game
        self.clipmoney = clipmoney
        self.turnover = 0

    def __str__(self):
        """String print out of Bank"""
        card_str = ['-' * CARD_WIDTH]
        card_str.append('{} (Game {})'.format(self.name, self.game.number).center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)
        card_str.append(''.center(CARD_WIDTH))
        card_str.append('Money: {}'.format(self.money).center(CARD_WIDTH))
        card_str.append('Turnover: {}'.format(self.turnover).center(CARD_WIDTH))

        card_str.append(''.center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)

        return '\n'.join('|{}|'.format(l) for l in card_str)

    def __repr__(self):
        return self.name

    def check_turnover(self):
        """Check to see if money has run out."""
        if self.money < 0.0:
            self.money += TOTAL_MONEY
            self.turnover += 1
        return self

    def add(self, amount=0.0, addfrom=None):
        """Add an amount of money from someone."""
        self.money += amount
        if addfrom:
            addfrom.pay(amount)
        return self

    def pay(self, amount=0.0, payto=None):
        """Pay an amount of money to someone."""
        if self.money > 0 or not self.clipmoney:
            self.money -= amount
            if payto:
                payto.add(amount)
            self.check_turnover()
        return self

class FreeParking(Bank):
    """Defines a Bank without turnover money."""

    def check_turnover(self):
        if self.money <= 0.0:
            self.turnover += 1
        return self
