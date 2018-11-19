#!/usr/bin/python
import random


# Script info
SCRIPTTITLE = 'Dice'
SCRIPTVERSION = '0.1.1'
SCRIPTINFO = 'Use this to throw a W6.'


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
def setup_args(optGroup):
    optGroup.add_option('--dice', action='store_true', dest='dice', default=None, help='Roll a W6!')


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.dice is not None and options.dice == True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Return module info
def get_info():
    return SCRIPTINFO


# Perform Encryption test
def run(log, options):
    # Welcome
    log.info(get_name())

    print('')
    log.info(random.randint(1, 6))
    print('')
