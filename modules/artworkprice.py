#!/usr/bin/python


# Script info
SCRIPTTITLE = 'Artwork price calculator'
SCRIPTVERSION = '0.1.1'
SCRIPTINFO = 'Calculate a reasonable price for selling an artwork (painting or photo print)'


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
# check_args(options)
#    Return True if main function can be run, depending on the command line arguments. If not dependent on any arguments, just return True
#
# run(log, options)
#    Main function where all the magic's happening.
#    logger object and command line options dictionary are passed


# Add command line arguments for this script to args parser
def setup_args(optGroup):
    optGroup.add_option('--artworkprice', action='store_true', dest='artworkprice', help=SCRIPTINFO)
    optGroup.add_option('--dimensions', type='string', dest='artworkdimensions', help='Size of the artwork (e.g. ''29x21'' or ''A3'')', metavar='DIMENSIONS')
    optGroup.add_option('--artfactor', type='float', dest='artworkfactor', default='6.0', help='Artwork price factor (beginners: 5..10, )', metavar='FACTOR')


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.artworkprice is not None and options.artworkprice == True \
            and check_additional_args(log, options)


# Checks additional arguments and prints error messages
def check_additional_args(log, options):
    if options.artworkdimensions is None or options.artworkdimensions == '':
        log.error('Need artwork dimensions!')
        return False
    if options.artworkfactor is None or options.artworkfactor < 1.0:
        log.error('Need art factor!')
        return False
    return True


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

    # Get args
    artFactor = options.artworkfactor
    (artWidth, artHeight) = get_dimensions(log, options.artworkdimensions)
    sizeStr = options.artworkdimensions
    if is_din_a_format(sizeStr):
        sizeStr = sizeStr + ' (' + str(artWidth) + ' x ' + str(artHeight) + ' cm)'

    # Here we go
    log.info('Calculating sales price for artwork of size ' + sizeStr + ' with factor ' + str(options.artworkfactor))
    print('')
    log.info('Sell the artwork for ' + str(calculate_price(log, artWidth, artHeight, artFactor)) + ' EUR')
    print('')
