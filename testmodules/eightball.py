#!/usr/bin/python
import logging
import random


# Script info
SCRIPTTITLE = 'Magic Eightball'
SCRIPTVERSION = '0.1'


def magic_eightball():
    replies = ["MY REPLY IS NO", "AS I SEE IT YES", "DON'T COUNT ON IT", "MY SOURCES SAY NO", "IT IS CERTAIN", "YES"]

    reply = random.choice(replies)

    return reply


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
    parser.add_option("-m", "--magiceightball", type="string", dest="magic_eightball", help="Ask the Magic Eightball a QUESTION!", metavar="QUESTION")


# Return True if args/options tell us to run this module
def check_args(options):
    return options.magic_eightball is not None and options.magic_eightball != ''


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Perform Encryption test
def run(log, options):
    # Welcome
    log.info(SCRIPTTITLE + ' ' + SCRIPTVERSION)

    # Get arguments
    inputStr = options.magic_eightball
    log.info('Question: ' + inputStr)
    print('')
    log.info(magic_eightball())
    print('')
