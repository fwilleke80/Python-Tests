#!/usr/bin/python
import sys
import time
import random


# Script info
SCRIPTTITLE = 'Tic Tac Toe'
SCRIPTVERSION = '0.1'
SCRIPTINFO = 'Play a round of classic Tic Tac Toe'
SCRIPT_HELP = """
Usage:
  --tictactoe [help]

help
    Displays this help, so you propably already know this one.
"""


# The game engine
class TicTacToeEngine():

    # A player
    class Player():
        types = ['human', 'computer']
        letters =['X', 'O'] 

        # Initialize player
        def __init__(self, *args, **kwargs):
            self._score = 0
            self._type = kwargs.get('type', TicTacToeEngine.Player.types[0])
            self._name = kwargs.get('name', '')
            self._letter = kwargs.get('letter', TicTacToeEngine.Player.letters[0])

        def __str__(self):
            return ((self._name + ' ') if self._name != '' else 'PLAYER ') + '[type=' + self._type + ', score=' + str(self._score) + ']'

        # Return player type
        def get_type(self):
            return self._type

        # Return player score
        def get_score(self):
            return self._score

        # Return player name
        def get_name(self):
            return self._name

        # Set player type
        def set_type(self, playertype):
            if playertype.lower() not in Player.types:
                raise ValueError('Unknow player type: ' + playertype.lower())
            _type = playertype.lower()

        # Set player score
        def set_score(self, score):
            self._score = score

        # Set player name
        def set_name(self, name):
            self._name = name

        # Make a move
        def make_move(self, board):
            # Human player
            if self._type == Player.types[0]:
                pass

            # Computer player
            else:
                pass


    # The game board
    class Board():

        # Initialize board
        def __init__(self):
            self._board = [None] * 9

        # Set a field
        def set_field(self, fieldNo, value):
            if fieldNo < 0 or fieldNo > len(self._board):
                raise ValueError('Invalid field number: ' + str(fieldNo))
            if value < 0 or value > 2:
                raise ValueError('Invalid value: ' + str(value))
            board[fieldNo] = value

        # Draw board
        def draw(self):
            pass


    # Initialize game
    def __init__(self):
        self._players = [None] * 2
        self._board = TicTacToeEngine.Board()

    # Add a player
    def add_player(self, player, id):
        if id < 0 or id > 1:
            raise ValueError('Invalid player id')
        self._players[id] = player


def run_tictactoe(log):
    game = TicTacToeEngine()

    newPlayer = TicTacToeEngine.Player(type='human', name='Player', letter='X')
    game.add_player(newPlayer, 0)

    newPlayer = TicTacToeEngine.Player(type='computer', name='Computer', letter='O')
    game.add_player(newPlayer, 1)


#####################################
#
# Module integration
#
#####################################
#
# Functions
# ---------
#
# setup_args(parser)
#    Adds arguments to the args parser
#
# get_name()
#    Return the module's name
#
# get_info()
#    Return the module's info string
#
# check_options(log, options)
#    Return True if main function can be run, depending on the command line arguments. If not dependent on any arguments, just return True
#    logger object and command line options dictionary are passed
#
# check_additional_options(log, options)
#    Return True if all arguments are not only set, but also make sense
#    logger object and command line options dictionary are passed
#
# run(log, options)
#    Main function where all the magic's happening.
#    logger object and command line options dictionary are passed


# Add command line arguments for this script to args parser
def setup_args(optGroup):
    optGroup.add_option('--tictactoe', action='store_true', dest='tictactoe', help=SCRIPTINFO)


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.tictactoe is not None and options.tictactoe == True


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
    return True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Return module info
def get_info():
    return SCRIPTINFO


# Perform Encryption test
def run(log, options, args):
    # Welcome
    log.info(get_name())
    print('')

    run_tictactoe(log)
