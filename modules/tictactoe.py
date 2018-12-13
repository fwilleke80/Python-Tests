#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import random
import platform


# Script info
SCRIPTTITLE = 'Tic Tac Toe'
SCRIPTVERSION = '0.9.3'
SCRIPTINFO = 'Play a round of classic Tic Tac Toe'
SCRIPT_HELP = """
Usage:
  --tictactoe [playername] [playerletter] [player2name] [help]

Examples:
  --tictactoe
      Starts a game against the computer with default names and letters

  --tictactoe John O
      Starts a game against the computer, you are named "John" and have the letter "O"

  --tictactoe John X Kevin
      Starts a 2 player game. You are named "John" and have the letter "X",
      your opponent is named "Kevin", and automatically gets the letter "O"  

playername
    Optionally provide your name here

playerletter
    Optionally provide your letter here ("X" or "O")

player2name
    Optionally provide a name for player 2 here. If provided, player 2 will be human.
    Otherwise it's a computer opponent.

help
    Displays this help, so you propably already know this one.
"""


# Constants
CLEARSCREEN = True
PLATFORM = platform.system().upper()
SCRIPTPATH = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
HIGHSCOREFILE = 'tictactoe_highscores.json'


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
            return ((self._name + ' ') if self._name != '' else 'PLAYER ') + '[type=' + self._type + ', score=' + str(self._score) + ', letter=' + self._letter + ']'

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
                raise ValueError('Unknown player type: ' + playertype.lower())
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
                if field is None:
                    newBoard._board[i] = None
                else:
                    newBoard._board[i] = int(field)
            return newBoard

        # Set a field
        def set_field(self, fieldId, playerId):
            if type(playerId) != int:
                raise TypeError('Invalid type for "playerId": ' + str(type(playerId)))
            if fieldId < 0 or fieldId > len(self._board):
                raise ValueError('Invalid field number: ' + str(fieldId))
            if playerId < 0 or playerId > 2:
                raise ValueError('Invalid playerId: ' + str(playerId))
            self._board[fieldId] = playerId

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
        def get_field_str(self, fieldId, players):
            if fieldId < 0 or fieldId > len(self._board):
                raise ValueError('Invalid field number: ' + str(fieldId))
            if self._board[fieldId] is None:
                return ' '
            else:
                return players[self._board[fieldId]].get_letter()

        # Return True if given combination (list of 3 fieldIds) is owned
		# by one single player. Otherwise return False
        def check_combination(self, combination):
            checkResult = self._board[combination[0]] == self._board[combination[1]] and \
                          self._board[combination[0]] == self._board[combination[2]] and \
                          self._board[combination[0]] is not None
            return checkResult

        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        def get_winner_id(self):
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
                if self.check_combination(combination):
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
        def draw(self, players):
            print('   A   B   C')
            print('')
            print('     |   |')
            print('1  ' + self.get_field_str(0, players) + ' | ' + self.get_field_str(1, players) + ' | ' + self.get_field_str(2, players))
            print('     |   |')
            print('  ---+---+---')
            print('     |   |')
            print('2  ' + self.get_field_str(3, players) + ' | ' + self.get_field_str(4, players) + ' | ' + self.get_field_str(5, players))
            print('     |   |')
            print('  ---+---+---')
            print('     |   |')
            print('3  ' + self.get_field_str(6, players) + ' | ' + self.get_field_str(7, players) + ' | ' + self.get_field_str(8, players))
            print('     |   |')

    # Choose the player who goes first
    # Returns player ID
    @staticmethod
    def decide_start_player(playerId = None):
        if playerId is None:
            return random.randint(0, 1)
        if playerId < -1 or playerId > 1:
            raise ValueError('Invalid playerId: ' + str(playerId))
        return playerId

    # Gives the ID of the player that was *not* specified
    @staticmethod
    def other_player_id(playerId):
        if playerId == 0:
            return 1
        else:
            return 0

    # Parses the input of a player (e.g. "B3")
    # Returns field ID (e.g. 7)
    @staticmethod
    def parse_player_input(playerInput):
        # Abort if invalid input
        if TicTacToeEngine.validate_player_input(playerInput) == False:
            return None

        # Calculate fieldId
        playerInput = playerInput.upper()
        return (int(playerInput[1]) - 1) * 3 + (ord(playerInput[0]) - 65)

    # 
    @staticmethod
    def fieldid_to_fieldname(fieldId):
        if fieldId < 0 or fieldId > 9:
            return 'Invalid fieldId: ' + str(fieldId)

        row = 'ABC'[fieldId % 3]
        col = (fieldId / 3) + 1

        return row + str(col)

    # Checks if the player has made a valid input (e.g. "A1 or C2")
    # Returns True if valid, otherwise False
    @staticmethod
    def validate_player_input(playerInput):
        # Check input type
        if type(playerInput) != str:
            return False
        # Check input length
        if len(playerInput) != 2:
            return False
        # Check for letter
        if playerInput[0].upper() not in 'ABC':
            return False
        # Check for number
        if playerInput[1] not in '123':
            return False
        return True

    # Write highscores
    @staticmethod
    def write_highscores(log, highscores):
        path = os.path.join(SCRIPTPATH, HIGHSCOREFILE)
        try:
            with open(path, 'w') as highscoreFile:
                highscoreDump = json.dumps(highscores, indent=4, separators=(',',': '))
                highscoreFile.write(highscoreDump)
                highscoreFile.close()
        except:
            log.error('Could not write highscore file: ' + path)
            return False

        return True

    # Load highscores
    @staticmethod
    def load_highscores(log):
        path = os.path.join(SCRIPTPATH, HIGHSCOREFILE)
        try:
            with open(path, 'r') as highscoreFile:
                highscores = json.load(highscoreFile)
                highscoreFile.close()
        except:
            log.info('Could not load highscores. Creating new file at ' + path)
            highscores = []
            TicTacToeEngine.write_highscores(log, highscores)

        return highscores

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
            # Is the current field empty?
            if self._board.is_empty_field(fieldId):
                # Create a copy of the board, to try out moves
                tmpBoard = self._board.get_copy()
                # Make a move on this field
                tmpBoard.set_field(fieldId, playerId)
                # Check if we win with this move
                if tmpBoard.get_winner_id() == playerId:
                    return fieldId

        # Check if the human player could win with his next move, and screw it up for them
        otherPlayerId = TicTacToeEngine.other_player_id(playerId)
        for fieldId in range(0, 9):
            # Is the current field empty?
            if self._board.is_empty_field(fieldId):
                # Create a copy of the board, to try out moves
                tmpBoard = self._board.get_copy()
                # Make a test move on this field
                tmpBoard.set_field(fieldId, otherPlayerId)
                # Check if other player would win
                winnerId = tmpBoard.get_winner_id()
                if winnerId == otherPlayerId:
                    return fieldId

        # Use one of the corner fields if free, then try the center field
        possibleFields = []
        for fieldId in [0, 2, 6, 8, 4]:
            if self._board.is_empty_field(fieldId):
                possibleFields.append(fieldId)
        if len(possibleFields) > 0:
            fieldId = random.choice(possibleFields)
            return fieldId

        # Take one of the side fields
        possibleFields = []
        for fieldId in [1, 3, 5, 7]:
            if self._board.is_empty_field(fieldId):
                possibleFields.append(fieldId)
        if len(possibleFields) > 0:
            fieldId = random.choice(possibleFields)
            return fieldId

    # Update highscores data with new game results
    def update_highscores(self, highscores, playerHasWon, activePlayerId):
        for playerId, player in enumerate(self._players):
            found = False

            # Look for existing entry
            for entry in highscores:
                if entry['name'] == player.get_name():
                    found = True
                    entry['played'] = int(entry['played']) + 1
                    if playerId == activePlayerId and playerHasWon:
                        entry['won'] = int(entry['won']) + 1

            # If not found, create new entry
            if found == False:
                entry = {
                    'name' : player.get_name(),
                    'played' : 1,
                    'won' : 1 if (playerId == activePlayerId and playerHasWon) else 0
                }
                highscores.append(entry)


    # Have the user set up the game
    def setup_game(self, log, playerName='', playerLetter='', player2Name=''):
        log.info('Setting up game...')
        if playerName == '' and playerLetter == '':
            newPlayer = TicTacToeEngine.Player(type='human', name='Player', letter='X')
            self.add_player(newPlayer, 0)

            newPlayer = TicTacToeEngine.Player(type='computer', name='Computer', letter='O')
            self.add_player(newPlayer, 1)
        else:
            if playerLetter not in TicTacToeEngine.Player.letters:
                log.error('Invalid player letter: ' + playerLetter)
                sys.exit()

            # Create player 1
            newPlayer = TicTacToeEngine.Player(type='human', name=playerName, letter=playerLetter)
            self.add_player(newPlayer, 0)

            # Get letter for player 2
            player2LetterIndex = TicTacToeEngine.other_player_id(TicTacToeEngine.Player.letters.index(playerLetter))
            player2Letter = TicTacToeEngine.Player.letters[player2LetterIndex]

            # Create player 2
            if player2Name == '':
                newPlayer = TicTacToeEngine.Player(type='computer', name='Computer', letter=player2Letter)
            else:
                newPlayer = TicTacToeEngine.Player(type='human', name=player2Name, letter=player2Letter)
            self.add_player(newPlayer, 1)

        return True

    # Run the game
    def run_game(self, log):
        log.info('Starting game...')
        print('')

        # Prepare
        self._board.clear()

        # Print players
        log.info('Player 1: ' + str(self._players[0]))
        log.info('Player 2: ' + str(self._players[1]))

        # Set initial state
        activePlayerId = TicTacToeEngine.decide_start_player()
        playerHasWon = False
        previousField = 'Nothing'
        turnCount = 0

        log.info(self._players[activePlayerId].get_name() + ' will go first!')
        print('')
        _ = raw_input('Press ENTER to start the game...')

        # Game loop
        startTime = time.time()
        while True:
            clear_screen()
            if turnCount > 0:
                print(self._players[TicTacToeEngine.other_player_id(activePlayerId)].get_name() + ' played: ' + str(previousField))
            else:
                print('')
            print('It´s ' + self._players[activePlayerId].get_name() + '´s turn!')
            print('')

            # Draw board state
            self._board.draw(self._players)
            print('')

            # Get what the player wants to do
            if self._players[activePlayerId].get_type() == 'computer':
                fieldId = self.suggest_move(activePlayerId)
                previousField = TicTacToeEngine.fieldid_to_fieldname(fieldId)
            else:
                inputOk = False
                while inputOk == False:
                    playerInput = raw_input(self._players[activePlayerId].get_name() + ', which field do you want to play: ').upper()
                    if TicTacToeEngine.validate_player_input(playerInput):
                        fieldId = TicTacToeEngine.parse_player_input(playerInput)
                        if self._board.is_empty_field(fieldId):
                            previousField = playerInput
                            inputOk = True
                        else:
                            print('Field ' + playerInput + ' is already taken!')
                    else:
                        print('Invalid input: ' + playerInput)

            # Now that we have the fieldId the player wants to play, apply it on the board
            self._board.set_field(fieldId, activePlayerId)

            # Check if player has won the game
            winnerId = self._board.get_winner_id()
            if winnerId is not None and winnerId == activePlayerId:
                # Player has won!
                playerHasWon = True
                break
            elif self._board.is_full():
                # It's a tie!
                break
            else:
                # Game is not over yet
                # Next player's turn
                activePlayerId = TicTacToeEngine.other_player_id(activePlayerId)
                turnCount += 1

        # The game is over
        # Did the active player win?
        clear_screen()
        if playerHasWon:
            log.info(self._players[activePlayerId].get_name() + ' has won the game!!')
        else:
            log.info('It´s a tie! Noboy has won.')
        timeMin, timeSec = divmod(round(time.time() - startTime), 60)
        log.info('The game lasted for ' + str(turnCount) + ' turns, and took ' + "%02d:%02d"%(timeMin, timeSec) + ' minutes.')
        print('')

        # Draw final board state
        self._board.draw(self._players)
        print('')

        # Highscores
        highscores = TicTacToeEngine.load_highscores(log)
        self.update_highscores(highscores, playerHasWon, activePlayerId)
        TicTacToeEngine.write_highscores(log, highscores)

        # That's all, folks!
        log.info('Game over')

# Clears the terminal screen
def clear_screen():
    if CLEARSCREEN:
        if PLATFORM == 'NT':
            # Call 'CLS' on Windows
            os.system('cls')
        else:
            # Call 'CLEAR' on OSX and Linux
            os.system('clear')

# Create & kick off game
def run_tictactoe(log, args):
    playerName = ''
    playerLetter = ''
    player2Name = ''
    if len(args) > 0:
        if len(args) < 2 or len(args) > 3:
            log.error('If you choose to provide args, you *have* to provide exactly 2 or 3!')
            return

        # Get player name
        playerName = args[0]

        # Get player letter
        playerLetter = args[1].upper()
        if playerLetter not in TicTacToeEngine.Player.letters:
            log.error('Only "X" or "O" are allowed as player letters!')
            return

        # Get 2nd player name, if specified
        if len(args) == 3:
            player2Name = args[2]

    # Set up game
    game = TicTacToeEngine()
    if game.setup_game(log, playerName=playerName, playerLetter=playerLetter, player2Name=player2Name):
        # Start game
        game.run_game(log)
    else:
        log.error('Game setup not successful!')

# Print highscores to screen
def print_highscores(log, highscores):
    if len(highscores) == 0:
        print('No highscores yet. Play some rounds!')
        return

    sortedHighscores = sorted(highscores, key=lambda k: k['won'])
    sortedHighscores.reverse()

    print '{:15}'.format('NAME') + '{:>6}'.format('PLAYED') + '{:>6}'.format('WON')
    print '=' * 27
    for item in sortedHighscores:
        print '{:15}'.format(item['name']) + '{:6d}'.format(item['played']) + '{:6d}'.format(item['won'])
    print ''


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

# run the module
def run(log, options, args):
    # Welcome
    log.info(get_name())
    print('')

    for arg in args:
        if arg.upper() == 'HELP':
            print(SCRIPT_HELP)
            sys.exit()
        elif arg.upper() == 'HIGHSCORES':
            highscores = TicTacToeEngine.load_highscores(log)
            print_highscores(log, highscores)
            sys.exit()

    run_tictactoe(log, args)
