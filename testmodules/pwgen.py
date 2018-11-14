#!/usr/bin/python
import logging
import string
import itertools
import random



# Script info
SCRIPTTITLE = 'Pronouncable Password Generator'
SCRIPTVERSION = '0.1'


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


# each syllable is consonant-vowel-consonant "pronounceable"
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
# check_args(options)
#    Return True if main function can be run, depending on the command line arguments. If not dependent on any arguments, just return True
#
# run(log, options)
#    Main function where all the magic's happening.
#    logger object and command line options dictionary are passed


# Add command line arguments for this script to args parser
def setup_args(parser):
    parser.add_option("--pwgen", action="store_true", dest="pwgen", default=None, help="Generate a pronouncable password")
    parser.add_option("--pwlen", type="int", dest="pwlen", default=0, help="Length of pronouncable password", metavar="LENGTH")


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.pwgen is not None and options.pwgen == True and check_additional_args(log, options)


# Checks additional arguments and prints error messages
def check_additional_args(log, options):
    if options.pwlen is None or options.pwlen < 1:
        log.error('LENGTH must be > 1')
        return False
    return True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Perform Encryption test
def run(log, options):
    # Welcome
    log.info(get_name())

    # Get args
    pwLen = options.pwlen

    if pwLen == 0:
      pwLen = random.randrange(3, 5)

    # Generate word
    log.info(gibberish(pwLen).title())
    