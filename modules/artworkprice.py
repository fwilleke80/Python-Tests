#!/usr/bin/python
import sys


# Script info
SCRIPTTITLE = 'Artwork price calculator'
SCRIPTVERSION = '0.1.1'
SCRIPTINFO = 'Calculate a reasonable price for selling an artwork (painting or photo print)'
SCRIPT_HELP = """
Usage:
  --artworkprice [d] [f] [help]
  --artworkprice [dimensions=n] [factor=n] [help]

Examples:
  --artworkprice A4 6.5
      Calculate the price for an artwork in A4 format with factor 6.5

  --artworkprice 40x30
      Calculate the price for an artwork in 40x30 cm with default factor

  --artworkprice dimensions=90x180 factor=8
      Calculate the price for an artwork in 90x180 cm with factor 8

dimensions
    You must define the dimensions of the artwork in order to calculate its sale price.
    Either use a DIN A format (A0, A1, A2, ... A10) or specify size in centimeters (e.g. 40x30, 90x100).

factor
    This factor kind of defines how good/famous/hip/deluded you are as an artist.
    For a good artist, 5 is quite ok. 1 is really expensive, and 1 is rediculously cheap.

help
    Displays this help, so you propably already know this one.
"""


din_a_formats = { 'A00' : (118.9, 168.2), \
                  'A0'  : (84.1,  118.9), \
                  'A1'  : (59.4,  84.1), \
                  'A2'  : (42.0,  59.4), \
                  'A3'  : (29.7,  42.0), \
                  'A4'  : (21.0,  29.7), \
                  'A5'  : (14.8,  21.0), \
                  'A6'  : (10.5,  14.8), \
                  'A7'  : (7.4,   10.5), \
                  'A8'  : (5.2,   7.4), \
                  'A9'  : (3.7,   5.2), \
                  'A10' : (2.6,   3.7) }


def get_din_a_dimensions(dimensionStr):
    # Look up and return dimensions
    return din_a_formats[dimensionStr.upper()]


def is_din_a_format(dimensionStr):
    # Check for valid DIN A format
    return 'A' in dimensionStr.upper() and \
            len(dimensionStr) >= 2 and \
            len(dimensionStr) <= 3


def is_dimension_definition(dimensionStr):
    # Check for valid dimension definition format
    return 'X' in dimensionStr.upper() and \
            len(dimensionStr) >= 3


def parse_dimensions(dimensionStr):
    dimensionStr = dimensionStr.strip()
    dimensionStr = dimensionStr.replace(' ', '')
    res = (dimensionStr.upper().split('X'))
    return (float(res[0]), float(res[1]))

def get_dimensions(log, dimensionStr):
    # Check for valid DIN A format
    isDinA = is_din_a_format(dimensionStr)
    isDimension = is_dimension_definition(dimensionStr)

    if not isDinA and not isDimension:
        errorMsg = dimensionStr + ' is not a valid dimension format!'
        log.error(errorMsg)
        raise ValueError(errorMsg)
    elif isDinA:
        return get_din_a_dimensions(dimensionStr)
    else:
        return parse_dimensions(dimensionStr)


def calculate_price(log, width, height, factor):
    log.debug('Width: ' + str(width))
    log.debug('Height: ' + str(height))
    log.debug('Factor: ' + str(factor))

    price = (width + height) * factor

    return price


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
    optGroup.add_option('--artworkprice', action='store_true', dest='artworkprice', help=SCRIPTINFO)


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.artworkprice is not None and options.artworkprice == True


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
    artFactor = 6.0
    artworkDimensions = ''

    for argIndex, arg in enumerate(args):
        arg = arg.upper()

        if (arg[0] == 'D' or arg[:10] == 'DIMENSIONS') and '=' in arg:
            artworkDimensions = arg.split('=')[1]
        elif (arg[0] == 'F' or arg[:6] == 'FACTOR') and '=' in arg:
            artFactor = float(arg.split('=')[1])
        elif arg == 'HELP':
            print(SCRIPT_HELP)
            print('')
        else:
            if argIndex == 0:
                artworkDimensions = arg
            elif argIndex == 1:
                artFactor = float(arg)

    # Cancel if no size specified
    if artworkDimensions == '':
        log.error('You have to specify a size for the artwork (e.g. "A4" or "40x30")!')
        print('')
        sys.exit()

    # Make sure we have a valid dimensions definition
    (artWidth, artHeight) = get_dimensions(log, artworkDimensions)
    sizeStr = artworkDimensions
    if is_din_a_format(sizeStr):
        sizeStr = sizeStr + ' (' + str(artWidth) + ' x ' + str(artHeight) + ' cm)'

    # Here we go
    log.info('Calculating sales price for artwork of size ' + sizeStr + ' with factor ' + str(artFactor))
    print('')
    log.info('Sell the artwork for ' + str(calculate_price(log, artWidth, artHeight, artFactor)) + ' EUR')
    print('')
