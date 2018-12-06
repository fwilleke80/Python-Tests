#!/usr/bin/python
import time
import math


# Script info
SCRIPTTITLE = 'Sieve of Eratosthenes'
SCRIPTVERSION = '0.3'
SCRIPTINFO = 'Calculate prime numbers using an ancient technique'
SCRIPT_HELP = """
Usage:
  --primenumbers COUNT [print] [help]

Examples:
  --primenumbers 50000 print
      Calculate prime numbers up to 50000 and print them on screen

  --primenumbers 1000000
      Silently calculate prime number up to 1000000

print
    All found prime numbers will be printed on screen

help
    Displays this help, so you propably already know this one.
"""


def sieve_of_eratosthenes(limit):
    '''Prime number generator. Yields the series
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29 ...
    using Sieve of Eratosthenes.
    '''
    yield 2
    sub_limit = int(limit**0.5)
    flags = [True, True] + [False] * (limit - 2)
    # Step through all the odd numbers
    for i in range(3, limit, 2):
        if flags[i]:
            continue
        yield i
        # Exclude further multiples of the current prime number
        if i <= sub_limit:
            for j in range(i*i, limit, i<<1):
                flags[j] = True


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
    optGroup.add_option('--primenumbers', type='int', dest='primenumbers', default=None, help='Perform prime number test up to LIMIT', metavar='LIMIT')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.primenumbers is not None


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
    if options.primenumbers <= 2:
        log.error('LIMIT must be > 2')
        return False
    return True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Return module info
def get_info():
    return SCRIPTINFO


# Calculate prime numbers op to limit
def run(log, options, args):
    # Get arguments
    limit = options.primenumbers
    printPrimes = False

    # Parse args
    for arg in args:
        arg = arg.upper()
        if arg == 'HELP':
            print(SCRIPT_HELP)
        elif arg == 'PRINT':
            printPrimes = True
        else:
            log.error('Unsupported argument: ' + arg)
            print('')

    # Welcome
    log.info(get_name())
    log.info('Calculating prime numbers up to ' + '{:,}'.format(limit) + '...')

    # Perform sieve and measure time
    timeStart = time.time()
    primeNumbers = list(sieve_of_eratosthenes(limit))
    timePassed = time.time() - timeStart

    # Print prime numbers
    if printPrimes:
        print(' ')
        print('Prime numbers:')
        print(str(primeNumbers))
        print(' ')

    # Diagnostic information
    log.info('Found ' + '{:,}'.format(len(primeNumbers)) + ' prime numbers!!!')
    if timePassed > 1.5:
        log.info('Finished in ' + str(timePassed) + ' sec')
    else:
        log.info('Finished in ' + str(timePassed * 1000) + ' msec')
