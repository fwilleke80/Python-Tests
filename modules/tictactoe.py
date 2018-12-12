#!/usr/bin/python
import os
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
            self.set_type(kwargs.get('type', TicTacToeEngine.Player.types[0]))
            self.set_name(kwargs.get('name', ''))
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


        # Return player letter
        def get_letter(self):
            return self._letter


        # Set player type
        def set_type(self, playertype):
            if playertype.lower() not in TicTacToeEngine.Player.types:
                raise ValueError('Unknow player type: ' + playertype.lower())
            self._type = playertype.lower()


        # Set player score
        def set_score(self, score):
            self._score = score


        # Set player name
        def set_name(self, name):
            self._name = name


        # Set player letter
        def set_letter(self, letter):
            if letter.upper() not in TicTacToeEngine.Player.letters:
                raise ValueError('Invalid player letter: ' + letter.upper())
            self._letter = letter.uper()


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
            self.clear()


        # Clear board
        def clear(self):
            self._board = [None] * 9    

        # Get copy        
        def get_copy(self):
            newBoard = TicTacToeEngine.Board()
            for i, field in enumerate(self._board):
                newBoard._board[i] = field
            return newBoard

        # Set a field
        def set_field(self, fieldId, playerId):
            if type(playerId) != int:
                raise TypeError('Invalid type for "playerId": ' + str(type(playerId)))
            if fieldId < 0 or fieldId > len(self._board):
                raise ValueError('Invalid field number: ' + str(fieldId))
            if playerId < 0 or playerId > 2:
                raise ValueError('Invalid playerId: ' + str(playerId))
            board[fieldId] = playerId

        # Set a field, if empty
        def set_field_safe(self, fieldId, playerId):
            if self.is_empty_field(fieldId):
                self.set_field(fieldId, playerId)
                return True
            else:
                return False


        # Get board state
        def get_state(self):
            return self._board


        # Get contents of a field
        def get_field_str(self, fieldId):
            if fieldId < 0 or fieldId > len(self._board):
                raise ValueError('Invalid field number: ' + str(fieldId))
            if self._board[fieldId] is None:
                return ' '
            else:
                return self._board[fieldId]


        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        def get_winner_id(self):
            # Game is not over yet
            if not self.is_full():
                return None

            # Winning combinations
            winning_combinations = [[0, 1, 2],    # Horizontal top
                                    [3, 4, 5],    # Horizontal middle
                                    [6, 7, 8],    # Horizontal bottom

                                    [0, 3, 6],    # Vertical left
                                    [1, 4, 7],    # Vertical middle
                                    [2, 5, 8],    # Vertical right

                                    [0, 4, 8],    # Diagonal down
                                    [6, 4, 2]]    # Diagonal up

            # Check winning combinations
            for combination in winning_combinations:
                # If all fields in a combination are owned by the same player
                if self._board[combination[0]] == self._board[combination[1]] and \
                    self._board[combination[0]] == self._board[combination[2]]:
                    # Return ID of player who owns the combination
                    return self._board[combination[0]]

            # No winner found, it's a tie
            return None

        # Return True if specified field is empty
        def is_empty_field(self, fieldId):
            if self._board[fieldId] is None:
                return True
            else:
                return False


        # Return True if all fields in the board are owned by one of the players
        def is_full(self):
            for field in self._board:
                if field is None:
                    return False
            return True


        # Draw board
        def draw(self):
            print('   A   B   C')
            print('')
            print('     |   |')
            print('1  ' + self.get_field_str(0) + ' | ' + self.get_field_str(1) + ' | ' + self.get_field_str(2))
            print('     |   |')
            print('  ---+---+---')
            print('     |   |')
            print('2  ' + self.get_field_str(3) + ' | ' + self.get_field_str(4) + ' | ' + self.get_field_str(5))
            print('     |   |')
            print('  ---+---+---')
            print('     |   |')
            print('3  ' + self.get_field_str(6) + ' | ' + self.get_field_str(7) + ' | ' + self.get_field_str(8))
            print('     |   |')


    # Choose the player who goes first
    # Returns player ID
    @staticmethod
    def decide_start_player(playerId = None):
        if playerId < -1 or playerId > 1:
            raise ValueError('Invalid playerId: ' + str(playerId))

        if playerId is None:
            return random.randint(0, 1)
        else:
            return playerId


    @ staticmethod
    def other_player_id(playerId):
        if playerId == 0:
            return 1
        else:
            return 0


    # Initialize game
    def __init__(self):
        self._players = [None] * 2
        self._board = TicTacToeEngine.Board()


    # Add a player
    def add_player(self, player, playerId):
        if playerId < 0 or playerId > 1:
            raise ValueError('Invalid player id')
        self._players[playerId] = player


    # Suggest a move
    # TODO: Only create board copy if necessary
    def suggest_move(self, playerId):
        # Check if we can win in the next move
        # Iterate all fields
        for fieldId in range(0, 9):
            # Create a copy of the board, to try out moves
            tmpBoard = self._board.get_copy()
            # Is the current field empty?
            if tmpBoard.is_empty_field(fieldId):
                # Make a move on this field
                tmpBoard.set_field(playerId, fieldId)
                # Check if we win with this move
                if tmpBoard.get_winner_id() == playerId:
                    return fieldId

        # Check if the human player could win with his next move, and screw it up for them
        for fieldId in range(0, 9):
            # Create a copy of the board, to try out moves
            tmpBoard = self._board.get_copy()
            if tmpBoard.is_empty_field(fieldId):
                tmpBoard.set_field(playerId, fieldId)
                if tmpBoard.get_winner_id() == TicTacToeEngine.other_player_id(playerId):
                    return fieldId

        # Use one of the corner fields if free, then try the center field
        tmpBoard = self._board.get_copy()
        for fieldId in [0, 2, 6, 8, 4]:
            if tmpBoard.set_field_safe(fieldId, playerId):
                return fieldId

        # Take one of the side fields
        tmpBoard = self._board.get_copy()
        for fieldId in [1, 3, 5, 7]:
            if tmpBoard.is_empty_field(fieldId):
                return fieldId


    # Have the user set up the game
    def setup_game(self, log, auto=False):
        log.info('Setting up game...')
        if auto:
            newPlayer = TicTacToeEngine.Player(type='human', name='Player', letter='X')
            self.add_player(newPlayer, 0)

            newPlayer = TicTacToeEngine.Player(type='computer', name='Computer', letter='O')
            self.add_player(newPlayer, 1)
        else:
            playerName = raw_input('Your name: ')
            while True:
                playerLetter = raw_input('Your letter ("X" or "O"): ').upper()
                if playerLetter in TicTacToeEngine.Player.letters:
                    break
            newPlayer = TicTacToeEngine.Player(type='human', name=playerName, letter=playerLetter)

            if playerLetter == 'X':
                playerLetter = 'O'
            else:
                playerLetter = 'X'
            newPlayer = TicTacToeEngine.Player(type='human', name='Computer', letter=playerLetter)

        return True


    # Run the game
    def run_game(self, log):
        log.info('Starting game...')

        # Prepare
        self._board.clear()

        # Game loop
        gameRunning = True
        while gameRunning:
            gameRunning = False

        log.info('Player 1: ' + str(self._players[0]))
        log.info('Player 2: ' + str(self._players[1]))
        self._board.draw()

        log.info('Game over')


def run_tictactoe(log):
    game = TicTacToeEngine()

    if game.setup_game(log, auto=True):
        game.run_game(log)
    else:
        log.error('Game setup not successful!')


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
