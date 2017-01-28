"""
Player.py - File for defining a Property class.
"""

from monopoly.Constants import CARD_WIDTH, MAX_LEVEL, UTILITIES, RAILROADS, COLOR_COUNTS

class Property(object):
    """Defines a property."""

    def __init__(self, name='', color='', loc=0, price=0.0, rents=None, mortgage=0.0, cost=0.0):
        """Initialize a property."""
        self.name = name
        self.color = color
        self.loc = loc
        self.price = price
        self.rents = rents
        self.mortgage = mortgage
        self.cost = cost
        self.mortgaged = False
        self.houses = 0
        self.hotels = 0

    @property
    def level(self):
        """Determine the development level of the property."""
        return MAX_LEVEL if self.hotels > 0 else self.houses

    @property
    def value(self):
        """Calculate the instantaneous value of a property."""
        if self.category == 'property':
            return self.mortgage + self.cost * (self.houses + self.hotels)
        else:
            return self.mortgage

    @property
    def category(self):
        """Determine the category type of the card."""
        if self.name in {'Go', 'Jail', 'Go To Jail', 'Free Parking', 'Income Tax', 'Luxury Tax'}:
            return 'other'
        elif self.name in {'Community Chest', 'Chance'}:
            return 'card'
        elif self.color == 'Railroad':
            return 'railroad'
        elif self.color == 'Utility':
            return 'utility'
        else:
            return 'property'

    def rent(self, player=None):
        """Determine the current rent of the property."""
        if player is None:
            return self.rents[0]
        else:
            same_color = sum([self.color == prop.color and not prop.mortgaged for prop in player.properties])
            rent = 0
            # Rent x times dice roll
            if self.loc in UTILITIES:
                roll, _, _ = player.roll_dice()
                rent = roll * self.rents[same_color - 1]
            # Rent times number owned
            elif self.loc in RAILROADS:
                rent = self.rents[same_color - 1]
            # Rent if all owned
            elif same_color == COLOR_COUNTS[self.color]:
                # Rent doubled if no houses or hotels
                if self.houses == 0 and self.hotels == 0:
                    rent = 2.0 * self.rents[0]
                # Rent for number of houses owned
                elif self.houses > 0 and self.hotels == 0:
                    rent = self.rents[self.houses]
                # Rent for hotel
                elif self.hotels > 0:
                    rent = self.rents[MAX_LEVEL]
            # Rent for a single property
            else:
                rent = self.rents[0]
            return rent

    def __str__(self):
        """String print out of card."""

        card_str = ['-' * CARD_WIDTH]

        if self.category in {'property', 'utility', 'railroad'}:
            card_str.append('Title Deed'.center(CARD_WIDTH))
            card_str.append(self.color.center(CARD_WIDTH))
            card_str.append('{} (${})'.format(self.name, self.price).center(CARD_WIDTH))
        else:
            card_str.append(''.center(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
            card_str.append(self.name.center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)
        if self.category in 'property':
            card_str.append('RENT ${}.'.format(self.rents[0]).center(CARD_WIDTH))
        else:
            card_str.append(''.center(CARD_WIDTH))
        if self.category is 'property':
            L = len(' With n Houses')
            card_str.append(' With 1 House ' + '${}. '.format(self.rents[1]).rjust(CARD_WIDTH - L))
            card_str.append(' With 2 Houses' + '${}. '.format(self.rents[1]).rjust(CARD_WIDTH - L))
            card_str.append(' With 3 Houses' + '${}. '.format(self.rents[1]).rjust(CARD_WIDTH - L))
            card_str.append(' With 4 Houses' + '${}. '.format(self.rents[1]).rjust(CARD_WIDTH - L))
            card_str.append('With Hotel ${}.'.format(self.rents[MAX_LEVEL]).center(CARD_WIDTH))
        elif self.category is 'railroad':
            L = len(' Rent                 ')
            card_str.append(' Rent                 ' + '${}. '.format(self.rents[0]).rjust(CARD_WIDTH - L))
            card_str.append(' If 2 R.R.\'s are owned' + '${}. '.format(self.rents[1]).rjust(CARD_WIDTH - L))
            card_str.append(' If 3  "      "   "   ' + '${}. '.format(self.rents[2]).rjust(CARD_WIDTH - L))
            card_str.append(' If 4  "      "   "   ' + '${}. '.format(self.rents[3]).rjust(CARD_WIDTH - L))
            card_str.append(''.center(CARD_WIDTH))
        elif self.category is 'utility':
            card_str.append('     If 1 Utility is owned'.ljust(CARD_WIDTH))
            card_str.append('  rent is {} x dice.'.format(self.rents[0]).ljust(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
            card_str.append('     If 2 Utilities are owned'.ljust(CARD_WIDTH))
            card_str.append('  rent is {} x dice.'.format(self.rents[1]).ljust(CARD_WIDTH))
        else:
            card_str.append(''.center(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
        card_str.append(''.center(CARD_WIDTH))
        if self.category in {'property', 'utility', 'railroad'}:
            card_str.append('Mortgage Value ${}.'.format(self.mortgage).center(CARD_WIDTH))
        else:
            card_str.append(''.center(CARD_WIDTH))
        if self.category is 'property':
            card_str.append('Houses Cost ${}. each'.format(self.cost).center(CARD_WIDTH))
            card_str.append('Hotels, ${}. Plus 4 Houses'.format(self.cost).center(CARD_WIDTH))
        else:
            card_str.append(''.center(CARD_WIDTH))
            card_str.append(''.center(CARD_WIDTH))
        card_str.append('-' * CARD_WIDTH)
        return '\n'.join('|{}|'.format(l) for l in card_str)

    def __repr__(self):
        return self.name
