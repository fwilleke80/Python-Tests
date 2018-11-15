#!/usr/bin/python
import logging
import time
import random
import math
import optparse
import multiprocessing as mp


# Script info
SCRIPTTITLE = 'Multithreading Test'
SCRIPTVERSION = '0.2.4'
SCRIPTINFO = 'Yield the full power of your machine and perform some multithreading benchmarks!'


# Generate MP speedup message
def speedup_msg(countSingle, countMulti):
    if countSingle == 0:
        return 'MP speedup: [INFINITE]'

    speedupVal = float(countMulti) / float(countSingle)
    if speedupVal <= 1.0:
        assessment = "performance LOSS"
    else:
        assessment = "performance gain"
    return 'MP speedup: ' + "%1.4f" % (speedupVal) + 'x ' + assessment


# Benchmark integer counting performance
def test_count(log, threadCount, timeLimit, testIntensity=100):
    def workerCount(timeLimit, count):
        startTime = time.time()
        i = 1
        while time.time() - startTime < timeLimit.value:
            for n in range(testIntensity):
                i += 1
        count.value += i


    log.info('Count test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerCount, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Counted ' + str(count.value) + ' values in ' + str(timeLimit) + ' seconds')

    if threadCount <= 1:
        return

    log.info('Count test: ' + str(threadCount) + ' threads...')
    processes = []
    values = []
    multiCount = 0
    for t in range(threadCount):
        count = mp.Value('i', 0)
        values.append(count)
        proc = mp.Process(target=workerCount, args=(timeLimitVal, count))
        processes.append(proc)

    # Start all
    for proc in processes:
        proc.start()
        log.debug('Started process ' + str(proc.pid))

    # End all
    for i, proc in enumerate(processes):
        proc.join()
        val = values[i].value
        multiCount += val
        log.debug('Process ' + str(proc.pid) + ' calculated ' + str(val) + ' values')

    log.info('Counted ' + str(multiCount) + ' values in ' + str(timeLimit) + ' seconds')
    log.info(speedup_msg(singleCount, multiCount))


# Benchmark random() performance
def test_random(log, threadCount, timeLimit, testIntensity=100):
    def workerRandom(timeLimit, count):
        startTime = time.time()
        i = 1
        while time.time() - startTime < timeLimit.value:
            for n in range(testIntensity):
                x = random.random()
                i += 1
        count.value += i


    log.info('Random test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerRandom, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Calculated ' + str(count.value) + ' random numbers in ' + str(timeLimit) + ' seconds')

    if threadCount <= 1:
        return

    log.info('Random test: ' + str(threadCount) + ' threads...')
    processes = []
    values = []
    multiCount = 0
    for t in range(threadCount):
        count = mp.Value('i', 0)
        values.append(count)
        proc = mp.Process(target=workerRandom, args=(timeLimitVal, count))
        processes.append(proc)

    # Start all
    for proc in processes:
        proc.start()
        log.debug('Started process ' + str(proc.pid))

    # End all
    for i, proc in enumerate(processes):
        proc.join()
        val = values[i].value
        multiCount += val
        log.debug('Process ' + str(proc.pid) + ' calculated ' + str(val) + ' values')

    log.info('Calculated ' + str(multiCount) + ' random numbers in ' + str(timeLimit) + ' seconds')
    log.info(speedup_msg(singleCount, multiCount))


# Benchmark sin() performance
def test_sin(log, threadCount, timeLimit, testIntensity=100):
    def workerSin(timeLimit, count):
        startTime = time.time()
        i = 1
        while time.time() - startTime < timeLimit.value:
            x = 1.234567
            for n in range(testIntensity):
                x = math.atan(math.tan(math.cos(math.sin(x))))
                i += 1
        count.value += i


    log.info('Sin() test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerSin, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Calculated ' + str(count.value) + ' sine values in ' + str(timeLimit) + ' seconds')

    if threadCount <= 1:
        return

    log.info('Sin() test: ' + str(threadCount) + ' threads...')
    processes = []
    values = []
    multiCount = 0
    for t in range(threadCount):
        count = mp.Value('i', 0)
        values.append(count)
        proc = mp.Process(target=workerSin, args=(timeLimitVal, count))
        processes.append(proc)

    # Start all
    for proc in processes:
        proc.start()
        log.debug('Started process ' + str(proc.pid))

    # End all
    for i, proc in enumerate(processes):
        proc.join()
        val = values[i].value
        multiCount += val
        log.debug('Process ' + str(proc.pid) + ' calculated ' + str(val) + ' values')

    log.info('Calculated ' + str(multiCount) + ' sine values in ' + str(timeLimit) + ' seconds')
    log.info(speedup_msg(singleCount, multiCount))


# List of available tests
# Associated test function name(s) to test stage
tests = {}
tests['random'] = [test_random]
tests['sin'] = [test_sin]
tests['count'] = [test_count]
tests['all'] = [test_count, test_random, test_sin]


def perform_tests(log, threadCount, timeLimit, performTests, testIntensity=100):
    log.info('Performing multiprocessing tests...')
    log.info('Available threads: ' + str(threadCount))
    log.info('Set time limit   : ' + str(timeLimit) + ' sec')
    print('')

    # Iterate specified test stages
    for test in performTests:
        funcs = tests[test]
        # Execute tests for each test stage
        for func in funcs:
            func(log, threadCount, timeLimit, testIntensity)
            print('')


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
    optGroup = optparse.OptionGroup(parser, SCRIPTTITLE + ' options', 'Benchmark parameters')
    optGroup.add_option("--threading", action="store_true", dest="threadingtest", default=None, help="Perform some multithreading tests")
    optGroup.add_option("--threadcount", type="int", dest="threadcount", default=0, help="Force number of threads to COUNT", metavar="COUNT")
    optGroup.add_option("--timelimit", type="float", dest="timelimit", default=2.0, help="Set time limit for benchmarks to LIMIT", metavar="LIMIT")
    optGroup.add_option("--tests", type="string", dest="threadingtests", default="all", help="Specify comma-separated list of tests to perform (possible values: " + str(tests.keys()) + ")", metavar="LIST")
    optGroup.add_option("--testintensity", type="int", dest="testintensity", default=100, help="Test intensity", metavar="INTENSITY")
    parser.add_option_group(optGroup)


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.threadingtest is not None \
            and options.threadingtest == True \
            and check_additional_args(log, options)


# Checks additional arguments and prints error messages
def check_additional_args(log, options):
    if options.threadcount is None or options.threadcount < 0:
        log.error('Invalid threadcount specified!')
        return False

    if options.timelimit is None or options.timelimit <= 0.0:
        log.error('Invalid time limit specified!')
        return False

    if options.threadingtests is None or options.threadingtests == '':
        log.error('Invalid tests specified!')
        return False

    if options.testintensity is None or options.testintensity < 1:
        log.error('Invalid test intensity specified!')
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

    threadCount = options.threadcount
    if threadCount == 0:
        threadCount = mp.cpu_count()

    timeLimit = options.timelimit
    if timeLimit <= 0.0:
        timeLimit = 2.0

    if options.threadingtests.lower() == 'all':
        performTests = ['all']
    else:
        performTests = options.threadingtests.split(',')

    testIntensity = options.testintensity

    print('')
    perform_tests(log, threadCount, timeLimit, performTests, testIntensity)
    print('')
