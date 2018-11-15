#!/usr/bin/python
import logging
import threading
import time
import random
import math


# Script info
SCRIPTTITLE = 'Multithreading Test'
SCRIPTVERSION = '0.1'
SCRIPTINFO = 'Yield the full power of your machine and perform some multithreading benchmarks!'


# Benchmark time limit in seconds
timeLimit = 5


def test_random(log):

    class workerRandom(threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter

        def run(self):
            log.info('Starting ' + self.name)
            calc_random(self.name, timeLimit, self.counter)
            log.info('Exiting ' + self.name + ', calculated ' + str(counter) + ' random values')

    def print_time(threadName, timeLimit, counter):
        startTime = time.time()

        while (time.time() - startTime) < timeLimit:
            if exitFlag:
                threadName.exit()
            rndVal = random.random()
            counter += 1

    workerThread = workerRandom(1, 'Worker: Random', 1)
    workerThread.start()




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
    parser.add_option("--threading", action="store_true", dest="threadingtest", default=None, help="Perform some multithreading tests")


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.threadingtest is not None and options.threadingtest == True


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
    perform_tests(log)
    print('')
