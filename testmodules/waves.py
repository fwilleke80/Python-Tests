#!/usr/bin/python
import logging
import os
import binascii
import time
import math
import sys
import random
import colorama
from colorama import Fore, Style


# Script info
SCRIPTTITLE = 'Waves'
SCRIPTVERSION = '0.4.6'


defaultParams = (15.0, 10.0, 0.1, 30.0)


def print_waveform_line(i, param1, param2, param3):
    # Chars to print in waveform
    waveChars = 'X$!?%'
    wave1Char = u'\u00B7'

    # Colors
    colColors =[Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA, Fore.BLUE] 

    # Basic sine wave values
    sin1 = math.sin(float(i) / param1)
    xPos1 = int(sin1 * 9.0 + 8.0)

    # Start line with something geeky
    sys.stdout.write(Style.BRIGHT)
    sys.stdout.write('%s' % Fore.WHITE)
    sys.stdout.write(("%02d" % xPos1) + 'x' + ("%02d" % random.randint(0, 9)) + '   ')
    sys.stdout.write(Style.NORMAL)

    for col in range(5):
        # Generate 16 random HEX chars
        colStr = binascii.b2a_hex(os.urandom(8))

        # Insert first sine wave into string
        colStr = colStr[:xPos1] + wave1Char + colStr[xPos1:]

        # Derived wave values for main waveform
        sin2 = math.sin((float(i) + (sin1 + float(col)) * param3 * float(col)) * param2)
        xPos2 = int((sin2 * 9.0) + 8.0)

        # Draw main waveform, switching colors
        sys.stdout.write('%s' % colColors[col])
        sys.stdout.write(Style.DIM)
        sys.stdout.write(colStr[:xPos2])
        sys.stdout.write(Style.NORMAL)
        sys.stdout.write(Style.BRIGHT)
        sys.stdout.write(waveChars[col])
        sys.stdout.write(Style.NORMAL)
        sys.stdout.write(colStr[xPos2:])
        sys.stdout.write('       ' if col < 4 else '')
        sys.stdout.write(Style.RESET_ALL)

    # Line break
    sys.stdout.write('\n')


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
    parser.add_option("-w", "--waves", action="store_true", dest="waves", default=None, help="Draw beautiful folded waveforms")
    parser.add_option("--wavesparams", type="float", dest="wavesparams", default=defaultParams, nargs=4, help="Custom parameters for folded waveforms: SPEED, SCALE1, SCALE2, and FOLD. Example: -w -- waveparams 15.0 10.0 0.1 30.0", metavar="SPEED SCALE1 SCALE2 FOLD")


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.waves is not None and check_additional_args(log, options)


# Checks additional arguments and prints error messages
def check_additional_args(log, options):
    if options.wavesparams is None:
        log.error('No wave parameters provided!')
        return False

    if type(options.wavesparams[0]) is not float or options.wavesparams[0] <= 0.0:
        log.error('SPEED must be a float value > 0.0')
        return False

    if type(options.wavesparams[1]) is not float or options.wavesparams[1] <= 0.0:
        log.error('SCALE1 must be a float value > 0.0')
        return False

    if type(options.wavesparams[2]) is not float or options.wavesparams[2] <= 0.0:
        log.error('SCALE2 must be a float value > 0.0')
        return False

    if type(options.wavesparams[3]) is not float or options.wavesparams[3] <= 0.0:
        log.error('FOLD must be a float value > 0.0')
        return False

    return True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Calculate prime numbers op to limit
def run(log, options):
    # Get arguments
    args = options.wavesparams
    argSpeed = args[0]
    argScale1 = args[1]
    argScale2 = args[2]
    argFold = args[3]

    speedFactor = 1.0 / max(argSpeed, 0.001)

    # Welcome
    log.info(get_name())
    log.debug('Args: ' + str(args))
    log.info('Preparing for waveform generation...')
    print(' ')
    print('Press CTRL+C to cancel!')
    time.sleep(1.5)
    colorama.init()

    startTime = time.time()
    timeUsedPure = 0.0
    lineCounter = 0

    try:
        while True:
            time1 = time.time()
            print_waveform_line(lineCounter, argScale1, argScale2, argFold)
            timeUsedPure += time.time() - time1
            lineCounter += 1
            time.sleep(speedFactor)

    except KeyboardInterrupt:
        print' '
        timeUsed = (time.time() - startTime)
        log.info('Finished! Been running for ' + ("%.3f" % timeUsed) + ' seconds and calculated ' + "{:,}".format(lineCounter) + ' steps!')
        log.info('Pure calculation time: ' + ("%.3f" % timeUsedPure) + ' seconds')
