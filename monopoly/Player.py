"""
Player.py - File for defining a Player class.
"""

import logging
import numpy as np

from monopoly.Constants import CARD_WIDTH, MAX_LEVEL, MAX_HOUSE_LEVEL, MAX_DOUBLES, JAIL_COST, NUM_PROPERTIES
from monopoly.Constants import COLOR_COUNTS, COLOR_PROPERTIES, PROPERTY_PRICES, PROPERTY_NAMES, SPACE
from monopoly.Constants import GO, JAIL, GO_TO_JAIL, LUXURY_TAX, INCOME_TAX, FREE_PARKING, COMMUNITY_CHEST, CHANCE

class Player(object):
    """Defines a Player of the Game."""

    def __init__(self, number, game):
        """Initialize a player."""
        self.number = number
        self.game = game
        self.position = 0
        self.money = 1500.0
        self.properties = []
        self.cards = []
        self.turn = 0
        self.round = 1
        self.risk_tolerance = np.random.normal(0.75, 0.1)
        self.just_visiting = True
        self.jail_double_try = 0

    @property
    def networth(self):
        """Calculate the instantaneous networth of the player."""
        return self.money + sum([p.value for p in self.properties])

    @property
    def num_houses(self):
        """Calculate the instantaneous number of houses a player has."""
        return sum([p.houses for p in self.properties])

    @property
    def num_hotels(self):
        """Calculate the instantaneous number of hotels a player has."""
        return sum([p.hotels for p in self.properties])

    @property
    def bankrupt(self):
        """Check is player has no money and no properties or cards."""
        # TODO: give assets to bank or player
        return self.money < 0 and len(self.properties) == 0 and len(self.cards) == 0

    def __str__(self):
        """String print out of Player."""

        card_str = ['-' * CARD_WIDTH]
        card_str.append('Player {} (Game {})'.format(self.number, self.game.number).center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)
        card_str.append(''.center(CARD_WIDTH))
        L = len(' Position  ')
        card_str.append(' Position  ' + ' {} '.format(self.position).rjust(CARD_WIDTH - L))
        card_str.append(' Turn      ' + ' {} '.format(self.turn).rjust(CARD_WIDTH - L))
        card_str.append(' Round     ' + ' {} '.format(self.round).rjust(CARD_WIDTH - L))
        card_str.append(' Money     ' + '${} '.format(self.money).rjust(CARD_WIDTH - L))
        card_str.append(' Net Worth ' + '${} '.format(self.networth).rjust(CARD_WIDTH - L))
        card_str.append(' Properties'.ljust(CARD_WIDTH))
        for prop in self.properties:
            modifier = 'h' * prop.houses + 'H' * prop.hotels + ('*' if prop.mortgaged else '')
            modifier = '({})'.format(modifier) if modifier else ''
            card_str.append('{} {}'.format(prop.name, modifier).center(CARD_WIDTH))
        card_str.append(' Cards'.ljust(CARD_WIDTH))
        for c in self.cards:
            card_str.append(c.name.center(CARD_WIDTH))
        card_str.append(''.center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)
        return '\n'.join('|{}|'.format(l) for l in card_str)

    def __repr__(self):
        return 'Player {}'.format(self.number)

    def owns(self, number=0):
        """Check if player owns a property position."""
        return number in [p.loc for p in self.properties]

    def get_property(self, number=0):
        """Find the property in the player's deeds. Assumes ownership is already determined."""
        prop = [prop for prop in self.properties if number == prop.loc]
        return prop[0] if prop else None

    def add(self, amount=0.0, addfrom=None):
        """Add an amount of money from someone."""
        self.money += amount
        if addfrom:
            addfrom.pay(amount)
        return self

    def pay(self, amount=0.0, payto=None):
        """Pay an amount of money to someone."""
        # Pay if player has enough money
        if self.money > amount:
            self.money -= amount
            if payto:
                payto.add(amount)
        # Check for liquidate money
        else:
            foundmoney = self.liquidate(amount)
            if foundmoney > amount:
                self.money -= amount
                if payto:
                    payto.add(amount)
            else:
                # Check for bankruptcy at begining of turn
                if self.bankrupt:
                    logging.debug('Player %s is bankrupt.', self.number)
                    self.game.bankrupted.append(self.game.players.pop(self.number))

        return self

    @staticmethod
    def bid(number=0, min_bid=0):
        """Make a bid on a property."""
        price = PROPERTY_PRICES[number]
        price_bid = np.random.normal(price, 0.5 * price)
        return min(price_bid, min_bid)

    @staticmethod
    def jail_pay_or_roll():
        """Pay or roll to get out of jail."""
        r = np.random.rand()
        return 0 if r > 0.5 else 1

    @staticmethod
    def liquidate_or_auction():
        """Liquidate money or just put up for auction."""
        r = np.random.rand()
        return 0 if r > 0.5 else 1

    @staticmethod
    def roll_dice():
        """Roll two dice with uniform randomness.  Return dice sum and doubles boolean."""
        dice1 = np.random.randint(1, 6)
        dice2 = np.random.randint(1, 6)
        return dice1 + dice2, dice1 == dice2, (dice1, dice2)

    def go_to_space(self, number=0, pass_go=True, just_visiting=True):
        """Move player to specific space."""
        # Handle passing go
        if pass_go and self.position > number:
            self.round += 1
            self.money += 200.0
        # Go to new position
        self.position = number
        # Set visiting flag
        self.just_visiting = just_visiting

        self.game.record.append([
            self.game.number,
            self.number,
            self.turn,
            self.round,
            0,
            False,
            self.position,
            SPACE[self.position][0]
        ])

        jailvisit = ' (just visiting)' if number == JAIL and just_visiting else ''
        logging.debug('Player %s goes to %s%s.', self.number, SPACE[self.position][0], jailvisit)
        self.handle_space()
        return self

    def go_to_nearest(self, space_list=None):
        """Helper function to go to the nearest instance of a space."""
        found = False
        for p in space_list:
            if self.position < p:
                found = True
                self.go_to_space(p)
        if not found:
            self.go_to_space(space_list[0])
        return self

    def develop(self):
        """Look for opportunities to develop properties."""

        # Look for ownership of all groups in player's properties
        monopolies = set()
        for prop in self.properties:
            if prop.category == 'property':
                same_color = sum([prop.color == otherprop.color and not otherprop.mortgaged for otherprop in self.properties])
                if same_color == COLOR_COUNTS[prop.color]:
                    monopolies.add(prop.color)

        # If monopoly exists develop
        for monopoly in monopolies:
            # Make list of monopoly
            monopoly_props = [self.get_property(p) for p in COLOR_PROPERTIES[monopoly]]
            monopoly_levels = [prop.level for prop in monopoly_props]
            dev_level = min(monopoly_levels)
            if dev_level < MAX_LEVEL:
                logging.debug(
                    'Player %s has a monopoly on %s %s with development at %s.',
                    self.number,
                    monopoly,
                    monopoly_props,
                    dev_level
                )
                # Loop thru properties to develop only the ones at the currect minimum development level
                # TODO: allow multiple development cycles.
                for prop in monopoly_props:
                    if prop.level == dev_level and prop.cost < self.risk_tolerance * self.money:
                        self.pay(prop.cost, self.game.bank)
                        if prop.houses < MAX_HOUSE_LEVEL:
                            prop.houses += 1
                            logging.debug('Player %s building house on %s.', self.number, prop.name)
                        elif prop.hotels < 1:
                            prop.hotels += 1
                            logging.debug('Player %s building hotel on %s.', self.number, prop.name)

        return self

    @staticmethod
    def liquidate(money=0.0):
        """Make decision to liquidate some assets."""
        money = 0.0
        # Sell get out of jail free cards
        # Sel houses and hotels
        # Mortgage lowest valued / non monopolied properties first

        return money

    def jail_time(self):
        """Make decision for what to do in jail."""

        # Set defaults
        roll, doubles, dice = None, None, None

        # Use get out of jail free card, if player has one
        if len(self.cards) > 0 and self.cards[0].name == 'Get out of Jail Free':
            logging.debug('Player %s using "Get out of Jail Free" Card.', self.number)
            self.just_visiting = True
            self.jail_double_try = 0
            card = self.cards.pop(0)
            # replace card in deck
            if card.deck == 'Chance':
                self.game.chance.append(card)
                logging.debug('Player %s returned card to chance.', self.number)
            elif card.deck == 'Chest':
                self.game.community_chest.append(card)
                logging.debug('Player %s returned card to community chest.', self.number)
            else:
                logging.warning('Card is not chance or community chest.')
        # Either roll or pay
        elif self.money > JAIL_COST:
            # Pay or Roll decision unless, already tried doubles 3 times
            pay_or_roll = self.jail_pay_or_roll() if self.jail_double_try < 3 else 1
            # Try to roll doubles
            if pay_or_roll == 0:
                roll, doubles, dice = self.roll_dice()
                if doubles:
                    self.just_visiting = True
                    self.jail_double_try = 0
                    logging.debug('Player %s rolled doubles to get out of jail.', self.number)
                else:
                    self.jail_double_try += 1
                    logging.debug('Player %s did NOT roll doubles. Still in jail.', self.number)
            # Just pay to get out
            elif pay_or_roll == 1:
                self.pay(JAIL_COST, self.game.freeparking)
                self.just_visiting = True
                self.jail_double_try = 0
                logging.debug('Player %s paid %s to get out of jail.', self.number, JAIL_COST)
            else:
                logging.warning('Pay or Roll decision not possible.')
        else:
            logging.debug('Player %s does not have enough money, liquidate some assets to get Jail fee.', self.number)
            foundmoney = self.liquidate(JAIL_COST)
            if foundmoney:
                pass
            else:
                logging.debug('Player %s could not find enough money. Still in jail.', self.number)
        return (roll, doubles, dice)

    def take_turn(self):
        """Player takes a turn."""

        # Set up Turn
        self.turn += 1
        doubles_count = 0
        roll, doubles, dice = None, None, None

        # Do Jail time or get out
        if self.position == JAIL and not self.just_visiting:
            roll, doubles, dice = self.jail_time()

        # Do normal turn if not in jail, just visiting jail or just got out of jail
        if self.position != JAIL or (self.position == JAIL and self.just_visiting):

            # Roll Dice
            if roll is None:
                roll, doubles, dice = self.roll_dice()

            # If rolled doubles and max doubles not rolled continue rolling
            # TODO: Code turn actions in between double rolls
            while doubles and doubles_count < MAX_DOUBLES:
                doubles_count += 1
                logging.debug('Player %s rolls %s = %s. Double count = %s.', self.number, dice, roll, doubles_count)
                roll, doubles, dice = self.roll_dice()

            logging.debug('Player %s rolls %s = %s. Double count = %s.', self.number, dice, roll, doubles_count)

            self.game.record.append([
                self.game.number,
                self.number,
                self.turn,
                self.round,
                roll,
                doubles,
                self.position,
                SPACE[self.position][0]
            ])

            # Go to rolled property or jail
            if doubles_count >= 3:
                self.go_to_space(JAIL, pass_go=False, just_visiting=False)
                logging.debug('Player %s rolled doubles 3 times, going to jail.', self.number)
            else:
                self.go_to_space((self.position + roll) % NUM_PROPERTIES)

        # Check for bankruptcy at end of turn
        if self.bankrupt:
            logging.debug('Player %s is bankrupt.', self.number)
            self.game.bankrupted.append(self.game.players.pop(self.number))

        return self

    def handle_space(self):
        """Determine what to do on specific space."""

        # Landing on Go, collect money
        if self.position == GO:
            self.money += 400.0
            logging.debug('Player %s landed on Go (+400)!', self.number)

        # Landing on Jail, just hang out until next turn
        elif self.position == JAIL:
            visiting = 'visiting' if self.just_visiting else 'in'
            logging.debug('Player %s is %s jail. Hang until next turn.', self.number, visiting)

        # Landing on Go to Jail, go to jail without passing Go
        elif self.position == GO_TO_JAIL:
            self.go_to_space(JAIL, pass_go=False, just_visiting=False)
            logging.debug('Player %s goes to jail.', self.number)

        # Landing on Luxury or Income Tax, pay indicated amount
        elif self.position == LUXURY_TAX or self.position == INCOME_TAX:
            tax = 75.0 if self.position == LUXURY_TAX else max(self.networth, 200.0)
            self.pay(tax, self.game.freeparking)
            logging.debug('Player %s pays $%s tax.', self.number, tax)

        # Landing on Free Parking, Collect the money
        elif self.position == FREE_PARKING:
            kitty = self.game.freeparking.money
            self.add(kitty, self.game.freeparking)
            logging.debug('Player %s collects $%s from free parking.', self.number, kitty)

        # Landing on Chance, follow card instructions
        elif self.position in CHANCE:
            card = self.game.draw_chance()
            logging.debug('Player %s draws "%s" from chance.', self.number, card.name)
            self.follow(card)

        # Landing on Community Chest, follow card instructions
        elif self.position in COMMUNITY_CHEST:
            card = self.game.draw_community_chest()
            logging.debug('Player %s draws "%s" from community chest.', self.number, card.name)
            self.follow(card)

        # Land on Property space, Buy Rent or hold
        else:
            self.handle_property()

        return self

    def handle_property(self):
        """Determine what to do with a property. Buy, rent or nothing."""

        # If self owns this do nothing
        if self.owns(self.position):
            prop = self.get_property(self.position)
            logging.debug('Player %s already owns %s. Do Nothing.', self.number, prop.name)
            return self
        else:
            owned = False
            # Check to see if other players own property to pay rent
            for plyr in self.game.others(self):
                if plyr.owns(self.position):
                    owned = True
                    prop = plyr.get_property(self.position)
                    # Property Mortgaged, do nothing
                    if prop.mortgaged:
                        logging.debug('%s is mortgaged. Do Nothing.', prop.name)
                        return self
                    # Pay Rent
                    else:
                        rent = prop.rent(plyr)
                        self.pay(rent, plyr)
                        logging.debug(
                            'Player %s pays $%s rent to Player %s for %s.', self.number, rent, plyr.number, prop.name
                        )
            # Try to Buy if nobody owns
            if not owned:
                if self.money > PROPERTY_PRICES[self.position]:
                    self.buy_property()
                else:
                    logging.debug(
                        'Player %s cannot afford %s for $%s.',
                        self.number,
                        PROPERTY_NAMES[self.position],
                        PROPERTY_PRICES[self.position]
                    )
                    find_money_or_auction = self.liquidate_or_auction()
                    # Look for money to buy property
                    if find_money_or_auction is 0:
                        logging.debug('Player %s decided to try liquidate some money.', self.number)
                        foundmoney = self.liquidate(PROPERTY_PRICES[self.position])
                        if foundmoney > PROPERTY_PRICES[self.position]:
                            self.buy_property()
                    # Auction the property for bid
                    elif find_money_or_auction is 1:
                        logging.debug('Player %s decided to auction off %s.', self.number, PROPERTY_NAMES[self.position])
                        self.game.auction(self.position)

        return self

    def buy_property(self, number=None, price=None):
        """Purchase a property. Pay money to bank and take property from Game list."""
        number = number if number else self.position
        prop = self.game.get_property(number)
        if prop:
            price = price if price else prop.price
            self.pay(price, self.game.bank)
            self.properties.append(prop)
            logging.debug('Player %s purchases %s for $%s.', self.number, prop.name, price)
        else:
            logging.warning('This should not happen, if property is not in Game list, somebody should own it.')
        return self

    def follow(self, card=None):
        """Follow the rules of a card."""
        card.rule(self, self.game, card)
        return self
