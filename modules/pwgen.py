#!/usr/bin/python
import string
import itertools
import random
import time


# Script info
SCRIPTTITLE = 'Pronouncable Password Generator'
SCRIPTVERSION = '0.1.3'
SCRIPTINFO = 'Generate a pronouncable password'
SCRIPT_HELP = """
Usage:
  --pwgen [length=n] [help]

Examples:
  --pwgen
      Generates a password of default length 4.

  --pwgen length=8
      Generates a password of length 8.

length
    Optionally define a password length. Default is 4.

help
    Displays this help, so you propably already know this one.
"""


# Initial consonants
initial_consonants = (set(string.ascii_lowercase) - set('aeiou')
                      # remove those easily confused with others
                      - set('qxc')
                      # add some crunchy clusters
                      | set(['bl', 'br', 'cl', 'cr', 'dr', 'fl',
                             'fr', 'gl', 'gr', 'pl', 'pr', 'sk',
                             'sl', 'sm', 'sn', 'sp', 'st', 'str',
                             'sw', 'tr', 'kn', 'shn'])
                      )

# Final consonants
final_consonants = (set(string.ascii_lowercase) - set('aeiou')
                    # confusable
                    - set('qxcsj')
                    # crunchy clusters
                    | set(['ct', 'ft', 'mp', 'nd', 'ng', 'nk', 'nt',
                           'pt', 'sk', 'sp', 'ss', 'st', 'per'])
                    )

# Vowels
vowels = 'aeiou' # we'll keep this simple


# each syllable is consonant-vowel-consonant 'pronounceable'
syllables = map(''.join, itertools.product(initial_consonants, 
                                           vowels, 
                                           final_consonants))


# Generate function
def gibberish(wordcount, wordlist=syllables):
    return ''.join(random.sample(wordlist, wordcount))


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
    optGroup.add_option('--pwgen', action='store_true', dest='pwgen', default=None, help=SCRIPTINFO)


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.pwgen is not None and options.pwgen == True


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

    # Parse args
    pwLen = 4
    for arg in args:
      arg = arg.upper()
      if (arg[0] == 'L' or arg[:6] == 'LENGTH') and '=' in arg:
        pwLen = int(arg.split('=')[1])
      elif arg == 'HELP':
        print(SCRIPT_HELP)
      else:
        log.error('Unsupported argument: ' + arg)
        print('')

    # Seed random generator
    random.seed(time.time())

    if pwLen == 0:
      pwLen = random.randrange(3, 5)

    # Generate word
    log.info(gibberish(pwLen).title())
    