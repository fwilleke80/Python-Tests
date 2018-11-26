#!/usr/bin/python
import random


# Script info
SCRIPTTITLE = 'Heads or Tails'
SCRIPTVERSION = '0.1.1'
SCRIPTINFO = 'Heads or Tails? Get help with your decision.'


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
# check_args(log, options)
#    Return True if main function can be run, depending on the command line arguments. If not dependent on any arguments, just return True
#    logger object and command line options dictionary are passed
#
# check_additional_args(log, options)
#    Return True if all arguments are not only set, but also make sense
#    logger object and command line options dictionary are passed
#
# run(log, options)
#    Main function where all the magic's happening.
#    logger object and command line options dictionary are passed


# Add command line arguments for this script to args parser
def setup_args(optGroup):
    optGroup.add_option('--headsortails', action='store_true', dest='headsortails', default=None, help='Heads or Tails?')


# Return True if args/options tell us to run this module
def check_args(log, options, args):
    return options.headsortails is not None and options.headsortails == True


# Checks additional arguments and prints error messages
def check_additional_args(log, options, args):
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
    headsortails = ['HEADS', 'TAILS']
    log.info(random.choice(headsortails))
    print('')
