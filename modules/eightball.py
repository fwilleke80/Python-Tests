#!/usr/bin/python
import random


# Script info
SCRIPTTITLE = 'Magic Eightball'
SCRIPTVERSION = '0.2.1'
SCRIPTINFO = 'Need advice? Ask the Magic Eightball!'


ascii_eightball = \
    '        ____' + '\n' + \
    '    ,dP9CGG88@b,' + '\n' +  \
    '  ,IP  _   Y888@@b,' + '\n' + \
    ' dIi  (_)   G8888@b' + '\n' + \
    'dCII  (_)   G8888@@b' + '\n' + \
    'GCCIi     ,GG8888@@@' + '\n' + \
    'GGCCCCCCCGGG88888@@@' + '\n' + \
    'GGGGCCCGGGG88888@@@@...' + '\n' + \
    'Y8GGGGGG8888888@@@@P.....' + '\n' + \
    ' Y88888888888@@@@@P......' + '\n' + \
    ' `Y8888888@@@@@@@P"......' + '\n' + \
    '    `@@@@@@@@@P".......' + '\n' + \
    '        ''........'



def magic_eightball():
    replies = ['IT IS CERTAIN',
                'AS I SEE IT YES',
                'REPLY HAZY, TRY AGAIN',
                'DON''T COUNT ON IT',
                'IT IS DECODEDLY SO',
                'MOST LIKELY',
                'ASK AGAIN LATER',
                'MY REPLY IS NO',
                'WHITHOUT A DOUBT',
                'OUTLOOK GOOD',
                'BETTER NOT TELL YOU NOW',
                'MY SOURCES SAY NO',
                'YES - DEFINITELY',
                'YES',
                'CANNOT PREDICT NOW',
                'OUTLOOK NOT SO GOOD',
                'YOU MAY RELY ON IT',
                'SIGN POINTS TO YES',
                'CONCENTRATE AND ASK AGAIN',
                'VERY DOUBTFUL']

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
    optGroup.add_option('--magiceightball', type='string', dest='magic_eightball', help='Ask the Magic Eightball a QUESTION!', metavar='QUESTION')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.magic_eightball is not None and options.magic_eightball != ''


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
    print(ascii_eightball)
    print('')

    # Here we go
    log.info('Question: ' + options.magic_eightball)
    print('')
    log.info(magic_eightball())
    print('')
