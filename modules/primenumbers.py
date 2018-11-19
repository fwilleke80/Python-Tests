#!/usr/bin/python
import time
import math


# Script info
SCRIPTTITLE = 'Sieve of Eratosthenes'
SCRIPTVERSION = '0.2.6'
SCRIPTINFO = 'Calculate prime numbers using an ancient technique'


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
# check_args(options)
#    Return True if main function can be run, depending on the command line arguments
#
# run(log, options)
#    Main function where all the magic's happening.
#    logger object and command line options dictionary are passed


# Add command line arguments for this script to args parser
def setup_args(parser):
    parser.add_option('-p', '--primenumbers', type='int', dest='primenumbers', default=None, help='Perform prime number test up to LIMIT', metavar='LIMIT')


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.primenumbers is not None and check_additional_args(log, options)


# Checks additional arguments and prints error messages
def check_additional_args(log, options):
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
def run(log, options):
    # Get arguments
    limit = options.primenumbers
    printPrimes = options.printoutput

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
