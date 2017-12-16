"""
Constants.py - Monopoly constants.
"""

# Game min/max and cost defaults
MAX_DOUBLES = 3
NUM_PROPERTIES = 40
NUM_CHANCE = 16
NUM_COMMUNITY_CHEST = 16
JAIL_COST = 50.0
MAX_HOUSE_LEVEL = 4
MAX_LEVEL = 5
MAX_HOUSES = 32
MAX_HOTELS = 12
INIT_CASH = 1500.0

# Game Space locations
# pylint:disable=bad-whitespace
SPACE = {
    0:  (                   'Go',          None),
    1:  ( 'Mediterranean Avenue', 'Dark Purple'),
    2:  (      'Community Chest',          None),
    3:  (        'Baltic Avenue', 'Dark Purple'),
    4:  (           'Income Tax',          None),
    5:  (     'Reading Railroad',    'Railroad'),
    6:  (      'Oriental Avenue',  'Light Blue'),
    7:  (               'Chance',          None),
    8:  (       'Vermont Avenue',  'Light Blue'),
    9:  (   'Connecticut Avenue',  'Light Blue'),
    10: (                 'Jail',          None),
    11: (    'St. Charles Place',        'Pink'),
    12: (     'Electric Company',     'Utility'),
    13: (        'States Avenue',        'Pink'),
    14: (      'Virginia Avenue',        'Pink'),
    15: ('Pennsylvania Railroad',    'Railroad'),
    16: (      'St. James Place',      'Orange'),
    17: (      'Community Chest',          None),
    18: (     'Tennessee Avenue',      'Orange'),
    19: (      'New York Avenue',      'Orange'),
    20: (         'Free Parking',          None),
    21: (      'Kentucky Avenue',         'Red'),
    22: (               'Chance',          None),
    23: (       'Indiana Avenue',         'Red'),
    24: (      'Illinois Avenue',         'Red'),
    25: (         'B&O Railroad',    'Railroad'),
    26: (      'Atlantic Avenue',      'Yellow'),
    27: (       'Ventnor Avenue',      'Yellow'),
    28: (          'Water Works',     'Utility'),
    29: (        'Marvin Garden',      'Yellow'),
    30: (           'Go To Jail',          None),
    31: (       'Pacific Avenue',       'Green'),
    32: ('North Carolina Avenue',       'Green'),
    33: (      'Community Chest',          None),
    34: (  'Pennsylvania Avenue',       'Green'),
    35: (           'Short Line',    'Railroad'),
    36: (               'Chance',          None),
    37: (           'Park Place',        'Blue'),
    38: (           'Luxury Tax',          None),
    39: (            'Boardwalk',        'Blue')
}
# pylint:enable=bad-whitespace

# Game space constants for ease
GO = 0
INCOME_TAX = 4
READING = 5
JAIL = 10
ST_CHARLES = 11
FREE_PARKING = 20
ILLINOIS = 25
GO_TO_JAIL = 30
LUXURY_TAX = 38
BOARDWALK = 39
CHANCE = (7, 22, 36)
COMMUNITY_CHEST = (2, 17, 33)
UTILITIES = (12, 28)
RAILROADS = (5, 15, 25, 35)

# Game Momey Constants
MONEY = {
    1   : 40,
    5   : 40,
    10  : 40,
    20  : 50,
    50  : 30,
    100 : 20,
    500 : 20
}
TOTAL_MONEY = sum([float(k) * float(v) for k, v in MONEY.iteritems()])

# Define Display constant
CARD_WIDTH = 32

# Property Definitions
# pylint:disable=bad-whitespace
PROPERTY_INDX = [     'name',       'color', 'loc', 'price',                          'rents', 'mortgage', 'cost']
PROPERTY_DEFS = [
    [ 'Mediterranean Avenue', 'Dark Purple',     1,      60,        [2, 10, 30, 90, 160, 250],         30,     50],
    [        'Baltic Avenue', 'Dark Purple',     3,      60,       [2, 20, 60, 180, 320, 450],         30,     50],
    [     'Reading Railroad',    'Railroad',     5,     200,               [25, 50, 100, 200],        100,   None],
    [      'Oriental Avenue',  'Light Blue',     6,     100,       [6, 30, 90, 270, 400, 550],         50,     50],
    [       'Vermont Avenue',  'Light Blue',     8,     100,       [6, 30, 90, 270, 400, 550],         50,     50],
    [   'Connecticut Avenue',  'Light Blue',     9,     120,      [8, 40, 100, 300, 450, 600],         60,     50],
    [    'St. Charles Place',        'Pink',    11,     140,     [10, 50, 150, 450, 625, 750],         70,    100],
    [     'Electric Company',     'Utility',    12,     150,                          [4, 10],         75,   None],
    [        'States Avenue',        'Pink',    13,     140,     [10, 50, 150, 450, 625, 750],         70,    100],
    [      'Virginia Avenue',        'Pink',    14,     160,     [12, 60, 180, 500, 700, 900],         80,    100],
    ['Pennsylvania Railroad',    'Railroad',    15,     200,               [25, 50, 100, 200],        100,   None],
    [      'St. James Place',      'Orange',    16,     180,     [14, 70, 200, 550, 750, 950],         90,    100],
    [     'Tennessee Avenue',      'Orange',    18,     180,     [14, 70, 200, 550, 750, 950],         90,    100],
    [      'New York Avenue',      'Orange',    19,     200,     [16, 80, 220, 600, 800,1000],        100,    100],
    [      'Kentucky Avenue',         'Red',    21,     220,    [18, 90, 250, 700, 875, 1050],        110,    150],
    [       'Indiana Avenue',         'Red',    23,     220,    [18, 90, 250, 700, 875, 1050],        110,    150],
    [      'Illinois Avenue',         'Red',    24,     240,   [20, 100, 300, 750, 925, 1100],        120,    150],
    [         'B&O Railroad',    'Railroad',    25,     200,               [25, 50, 100, 200],        100,   None],
    [      'Atlantic Avenue',      'Yellow',    26,     260,   [22, 110, 330, 800, 975, 1150],        130,    150],
    [       'Ventnor Avenue',      'Yellow',    27,     260,   [22, 110, 330, 800, 975, 1150],        130,    150],
    [          'Water Works',     'Utility',    28,     150,                          [4, 10],         75,   None],
    [        'Marvin Garden',      'Yellow',    29,     280,  [24, 120, 360, 850, 1025, 1200],        140,    150],
    [       'Pacific Avenue',       'Green',    31,     300,  [26, 130, 390, 900, 1100, 1275],        150,    200],
    ['North Carolina Avenue',       'Green',    32,     300,  [26, 130, 390, 900, 1100, 1275],        150,    200],
    [  'Pennsylvania Avenue',       'Green',    34,     320, [28, 150, 450, 1000, 1200, 1400],        160,    200],
    [           'Short Line',    'Railroad',    35,     200,               [25, 50, 100, 200],        100,   None],
    [           'Park Place',        'Blue',    37,     350, [35, 175, 500, 1100, 1300, 1500],        175,    200],
    [            'Boardwalk',        'Blue',    39,     400, [50, 200, 600, 1400, 1700, 2000],        200,    200]
]
# pylint:enable=bad-whitespace

# Create Property look up variables
PROPERTY_PRICES = {loc: price for _, _, loc, price, _, _, _ in PROPERTY_DEFS}
PROPERTY_NAMES = {loc: name for name, _, loc, _, _, _, _ in PROPERTY_DEFS}
PROPERTY_COLOR = {loc: color for _, color, loc, _, _, _, _ in PROPERTY_DEFS}
COLOR_COUNTS = {}
for _, color, _, _, _, _, _ in PROPERTY_DEFS:
    if color not in COLOR_COUNTS:
        COLOR_COUNTS[color] = 1
    elif color:
        COLOR_COUNTS[color] += 1
COLOR_PROPERTIES = {}
for _, color, loc, _, _, _, _ in PROPERTY_DEFS:
    if color not in COLOR_PROPERTIES:
        COLOR_PROPERTIES[color] = [loc]
    elif color:
        COLOR_PROPERTIES[color].append(loc)
