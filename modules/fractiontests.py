#!/usr/bin/python
import fractions


# Script info
SCRIPTTITLE = 'Fraction Tests'
SCRIPTVERSION = '0.2.1'
SCRIPTINFO = 'Perform fraction calculations'


def lcm(a, b):
   return (a * b) // fractions.gcd(a, b)


SIMPLIFYRESULT_UNCHANGED = 0
SIMPLIFYRESULT_WHOLENUMBER = 1
SIMPLYFYRESULT_NEW = 2


def simplify(a, b):
    if b == 0:
        return 'Division by 0 - result undefined'

    # Remove greatest common divisor:
    gcd = fractions.gcd(a, b)
    (reduced_num, reduced_den) = (a / gcd, b / gcd)
    # Note that reduced_den > 0 as documented in the gcd function.

    if reduced_den == 1:
        return (SIMPLIFYRESULT_WHOLENUMBER, '(%d / %d) is simplified to %d' % (a, b, reduced_num), reduced_num)
    elif gcd == 1:
        return (SIMPLIFYRESULT_UNCHANGED, '(%d / %d) is already at most simplified state.' % (a, b), a, b)
    else:
        return (SIMPLYFYRESULT_NEW, '(%d / %d) is simplified to (%d / %d)' % (a, b, reduced_num, reduced_den), reduced_num, reduced_den)


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
    parser.add_option('--fraction', type='string', dest='fraction', nargs=3, default=None, help='Calculate F from a fraction (A / B). Possible values for F: [gcd, lcm, simplify]', metavar='F A B')


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.fraction is not None and len(options.fraction) == 3


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
    fractFunc, a, b = options.fraction
    try:
        a = float(a)
        b = float(b)
    except:
        log.error('Could not convert A or B into a float value!')
        raise AttributeError()
    log.debug('Calculating ' + fractFunc + ' of (' + str(a) + '/' + str(b) + ')...')

    fractFunc = fractFunc.lower()
    if fractFunc == 'gcd':
        result = fractions.gcd(a, b)
    elif fractFunc == 'lcm':
        result = lcm(a, b)
    elif fractFunc == 'simplify':
        simplifyResult = simplify(a, b)
        log.info(simplifyResult[1])
        return
    else:
        log.error('Unknown fraction function: ' + fractFunc)
        return

    log.info(fractFunc + '(' + str(a) + ' / ' + str(b) + ') = ' + '{0:.5f}'.format(result))
