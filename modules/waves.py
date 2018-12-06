#!/usr/bin/python
import os
import sys
import time
import math
import binascii
import random

# Dependency library!
import colorama
from colorama import Fore, Style


# Script info
SCRIPTTITLE = 'Waves'
SCRIPTVERSION = '0.4.6'
SCRIPTINFO = 'Draw colorful folded waveforms'
SCRIPT_HELP = """
Usage:
  --waves [speed=n] [scale1=n] [scale2=n] [fold=n]
  --waves [n1] [n2] [n3] [n4]

Examples:
  --waves
      Draw waves with default parameters

  --waves speed=30
      Draw waves with default parameters, but a speed of 30

  --waves 17 8 0.2 25
      Draw waves with specific parameters

  --waves speed=15 scale1=10 scale2=0.1 fold=30
      Draw waves with specific parameters

speed
    Drawing speed. Higher values draw faster

scale1
    Scale factor 1

scale2
    Scale factor 2

fold
    Fold value (higher values create additional details in derived curves)

help
    Displays this help, so you propably already know this one.
"""




# Default parameters
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
    sys.stdout.write(('%02d' % xPos1) + 'x' + ('%02d' % random.randint(0, 9)) + '   ')
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
    optGroup.add_option('--waves', action='store_true', dest='waves', default=None, help=SCRIPTINFO)
    #optGroup.add_option('--wavesparams', type='float', dest='wavesparams', default=defaultParams, nargs=4, help='Custom parameters for folded waveforms: SPEED, SCALE1, SCALE2, and FOLD. Example: -w -- waveparams 15.0 10.0 0.1 30.0', metavar='SPEED SCALE1 SCALE2 FOLD')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.waves is not None


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
    return True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Return module info
def get_info():
    return SCRIPTINFO


# Calculate prime numbers op to limit
def run(log, options, args):
    # Parse args
    argSpeed = defaultParams[0]
    argScale1 = defaultParams[1]
    argScale2 = defaultParams[2]
    argFold = defaultParams[3]
    for argIndex, arg in enumerate(args):
        arg = arg.upper()
        if (arg[:2] == 'SP' or arg[:5] == 'SPEED') and '=' in arg:
            argSpeed = float(arg.split('=')[1])
        elif (arg[:2] == 'S1' or arg[:6] == 'SCALE1') and '=' in arg:
            argScale1 = float(arg.split('=')[1])
        elif (arg[:2] == 'S2' or arg[:6] == 'SCALE2') and '=' in arg:
            argScale2 = float(arg.split('=')[1])
        elif (arg[0] == 'F' or arg[:4] == 'FOLD') and '=' in arg:
            argFold = float(arg.split('=')[1])
        elif arg == 'HELP':
            print(SCRIPT_HELP)
            print('')
            sys.exit()
        else:
            if argIndex == 0:
                argSpeed = float(arg)
            elif argIndex == 1:
                argScale1 = float(arg)
            elif argIndex == 2:
                argScale2 = float(arg)
            elif argIndex == 3:
                argFold = float(arg)

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
        log.info('Finished! Been running for ' + ('%.3f' % timeUsed) + ' seconds and calculated ' + '{:,}'.format(lineCounter) + ' steps!')
        log.info('Pure calculation time: ' + ('%.3f' % timeUsedPure) + ' seconds')
