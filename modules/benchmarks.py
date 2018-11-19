#!/usr/bin/python
import time
import random
import math
import multiprocessing as mp


# Script info
SCRIPTTITLE = 'Benchmarks'
SCRIPTVERSION = '0.3.2'
SCRIPTINFO = 'Yield the full power of your machine and perform some multithreaded benchmarks!'


# Generate MP speedup message
def speedup_msg(countSingle, countMulti):
    if countSingle == 0:
        return 'MP speedup: [INFINITE]'

    speedupVal = float(countMulti) / float(countSingle)
    if speedupVal <= 1.0:
        assessment = "performance *LOSS*"
    else:
        assessment = "performance *GAIN*"
    return 'MP speedup: ' + "%1.4f" % (speedupVal) + 'x ' + assessment


# Benchmark integer counting performance
def test_count(log, threadCount, timeLimit, testIntensity=100):
    def workerCount(timeLimit, count):
        startTime = time.time()
        i = 1
        keepRunning = True
        while keepRunning:
            for n in range(testIntensity):
                i += 1
                if time.time() - startTime >= timeLimit.value:
                    keepRunning = False
                    break
        count.value += i


    log.info('Count test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerCount, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Counted ' + "{:,}".format(singleCount) + ' values in ' + str(timeLimit) + ' seconds')

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

    log.info('Counted ' + "{:,}".format(multiCount) + ' values in ' + str(timeLimit) + ' seconds (' + "{:,}".format(multiCount / threadCount) + ' per thread)')
    log.info(speedup_msg(singleCount, multiCount))


# Benchmark random() performance
def test_random(log, threadCount, timeLimit, testIntensity=100):
    def workerRandom(timeLimit, count):
        startTime = time.time()
        i = 1
        keepRunning = True
        while keepRunning:
            for n in range(testIntensity):
                x = random.random()
                i += 1
                if time.time() - startTime >= timeLimit.value:
                    keepRunning = False
                    break
        count.value += i


    log.info('Random test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerRandom, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Calculated ' + "{:,}".format(singleCount) + ' random numbers in ' + str(timeLimit) + ' seconds')

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

    log.info('Calculated ' + "{:,}".format(multiCount) + ' random numbers in ' + str(timeLimit) + ' seconds (' + "{:,}".format(multiCount / threadCount) + ' per thread)')
    log.info(speedup_msg(singleCount, multiCount))


# Benchmark integer counting performance
def test_float(log, threadCount, timeLimit, testIntensity=100):
    def workerFloat(timeLimit, count):
        startTime = time.time()
        i = 1
        keepRunning = True
        while keepRunning:
            for n in range(testIntensity):
                y = math.pi / float(i)
                i += 1
                if time.time() - startTime >= timeLimit.value:
                    keepRunning = False
                    break
        count.value += i


    log.info('Float test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerFloat, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Divided ' + "{:,}".format(singleCount) + ' float values in ' + str(timeLimit) + ' seconds')

    if threadCount <= 1:
        return

    log.info('Float test: ' + str(threadCount) + ' threads...')
    processes = []
    values = []
    multiCount = 0
    for t in range(threadCount):
        count = mp.Value('i', 0)
        values.append(count)
        proc = mp.Process(target=workerFloat, args=(timeLimitVal, count))
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

    log.info('Divided ' + "{:,}".format(multiCount) + ' float values in ' + str(timeLimit) + ' seconds (' + "{:,}".format(multiCount / threadCount) + ' per thread)')
    log.info(speedup_msg(singleCount, multiCount))


# Benchmark sin() performance
def test_sin(log, threadCount, timeLimit, testIntensity=100):
    def workerSin(timeLimit, count):
        startTime = time.time()
        i = 1
        keepRunning = True
        while keepRunning:
            x = 1.234567
            for n in range(testIntensity):
                x = math.sin(x)
                i += 1
                if time.time() - startTime >= timeLimit.value:
                    keepRunning = False
                    break
        count.value += i


    log.info('Sin() test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerSin, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Calculated ' + "{:,}".format(singleCount) + ' sine values in ' + str(timeLimit) + ' seconds')

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

    log.info('Calculated ' + "{:,}".format(multiCount) + ' sine values in ' + str(timeLimit) + ' seconds (' + "{:,}".format(multiCount / threadCount) + ' per thread)')
    log.info(speedup_msg(singleCount, multiCount))


# Benchmark sin() performance
def test_matrixmultiplication(log, threadCount, timeLimit, testIntensity=100):

    matrixX = [[1.2, 2.3, 3.4], [4.5, 5.6, 6.7], [7.8, 8.9, 9.1], [10.2, 11.3, 12.4]]
    matrixY = [[1.9, 2.8, 7.6], [1.7, 2.6, 4.2], [3.5, 4.4, 7.3], [15.1, 52.2, 73.2]]

    def matmult(a, b):
        zip_b = zip(*b)
        # uncomment next line if python 3 : 
        # zip_b = list(zip_b)
        return [[sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b)) 
                 for col_b in zip_b] for row_a in a]

    def workerMatrixMultiplication(timeLimit, count):
        startTime = time.time()
        i = 1
        keepRunning = True
        while keepRunning:
            for n in range(testIntensity):
                mRes = matmult(matrixX, matrixY)
                i += 1
                if time.time() - startTime >= timeLimit.value:
                    keepRunning = False
                    break
        count.value += i

    # Create matrices
    log.info('Preparing matrix multiplication test...')

    log.info('Matrix multiplication test: 1 thread...')
    timeLimitVal = mp.Value('d', timeLimit)
    count = mp.Value('i', 0)
    proc = mp.Process(target=workerMatrixMultiplication, args=(timeLimitVal, count))
    proc.start()
    proc.join()
    singleCount = count.value
    log.info('Multiplied ' + "{:,}".format(singleCount) + ' matrices in ' + str(timeLimit) + ' seconds')

    if threadCount <= 1:
        return

    log.info('Matrix multiplication test: ' + str(threadCount) + ' threads...')
    processes = []
    values = []
    multiCount = 0
    for t in range(threadCount):
        count = mp.Value('i', 0)
        values.append(count)
        proc = mp.Process(target=workerMatrixMultiplication, args=(timeLimitVal, count))
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

    log.info('Multiplied ' + "{:,}".format(multiCount) + ' matrices in ' + str(timeLimit) + ' seconds (' + "{:,}".format(multiCount / threadCount) + ' per thread)')
    log.info(speedup_msg(singleCount, multiCount))


# List of available tests
# Associated test function name(s) to test stage
tests = {}
tests['count'] = [test_count]
tests['random'] = [test_random]
tests['sin'] = [test_sin]
tests['float'] = [test_float]
tests['matrix'] = [test_matrixmultiplication]
tests['all'] = [test_count, test_random, test_sin, test_float, test_matrixmultiplication]


def perform_benchmarks(log, threadCount, timeLimit, performTests, testIntensity=100):
    # Calculate number of tests to perform
    testCount = 0
    for testStage in performTests:
        testCount += len(tests[testStage])

    print('=========================================')
    log.info('Performing benchmarks...')
    print('-----------------------------------------')
    log.info('Available threads: ' + str(threadCount))
    log.info('Set time limit   : ' + str(timeLimit) + ' sec per test')
    log.info('Test intensity   : ' + str(testIntensity))
    log.info('Test stages      : ' + str(performTests))
    log.info('Approx. duration : ' + str(timeLimit * testCount * 2) + ' sec')
    print('=========================================')
    print('')

    # Iterate specified test stages
    for testStage in performTests:
        funcs = tests[testStage]
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
def setup_args(optGroup):
    optGroup.add_option("--benchmarks", action="store_true", dest="benchmarks", default=None, help="Perform some multithreading tests")
    optGroup.add_option("--threadcount", type="int", dest="threadcount", default=0, help="Force number of threads to COUNT", metavar="COUNT")
    optGroup.add_option("--timelimit", type="float", dest="timelimit", default=2.0, help="Set time limit for benchmarks to LIMIT", metavar="LIMIT")
    optGroup.add_option("--tests", type="string", dest="threadingtests", default="all", help="Specify comma-separated list of tests to perform (possible values: " + str(tests.keys()) + ")", metavar="LIST")
    optGroup.add_option("--testintensity", type="int", dest="testintensity", default=100, help="Test intensity", metavar="INTENSITY")


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.benchmarks is not None \
            and options.benchmarks == True \
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
    perform_benchmarks(log, threadCount, timeLimit, performTests, testIntensity)
