#!/usr/bin/python
import logging
import random


# Script info
SCRIPTTITLE = 'Heads or Tails'
SCRIPTVERSION = '0.1'


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
    parser.add_option("-t", "--headsortails", action="store_true", dest="headsortails", default=None, help="Heads or Tails?")


# Return True if args/options tell us to run this module
def check_args(options):
    return options.headsortails is not None and options.headsortails == True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Perform Encryption test
def run(log, options):
    # Welcome
    log.info(get_name())

    print('')
    headsortails = ["HEADS", "TAILS"]
    log.info(random.choice(headsortails))
    print('')