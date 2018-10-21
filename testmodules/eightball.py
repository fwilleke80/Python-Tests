#!/usr/bin/python
import logging
import random


# Script info
SCRIPTTITLE = 'Magic Eightball'
SCRIPTVERSION = '0.2'


def magic_eightball():
    replies = ["IT IS CERTAIN",
                "AS I SEE IT YES",
                "REPLY HAZY, TRY AGAIN",
                "DON'T COUNT ON IT",
                "IT IS DECODEDLY SO",
                "MOST LIKELY",
                "ASK AGAIN LATER",
                "MY REPLY IS NO",
                "WHITHOUT A DOUBT",
                "OUTLOOK GOOD",
                "BETTER NOT TELL YOU NOW",
                "MY SOURCES SAY NO",
                "YES - DEFINITELY",
                "YES",
                "CANNOT PREDICT NOW",
                "OUTLOOK NOT SO GOOD",
                "YOU MAY RELY ON IT",
                "SIGN POINTS TO YES",
                "CONCENTRATE AND ASK AGAIN",
                "VERY DOUBTFUL"]

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
