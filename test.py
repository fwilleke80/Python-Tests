#!/usr/bin/python

import optparse
import logging

from testmodules import primenumbers
from testmodules import waves
from testmodules import encrypt_xor
from testmodules import location
from testmodules import eightball
from testmodules import dice
from testmodules import headsortails
from testmodules import pwgen
from testmodules import namegen
from testmodules import fractiontests


# Script info
SCRIPTTITLE = 'Test Script Launcher'
SCRIPTVERSION = '0.2.4'
SCRIPTCOPYRIGHT = '2018 by Frank Willeke'

# Logging
LOGLEVEL = logging.INFO
LOGFILE = 'test.log'
LOGFORMAT = '%(levelname)s: %(message)s'
LOGFILEFORMAT = '%(asctime)s: %(levelname)s: %(message)s'
log = logging.getLogger('log')

# List of registered module
registeredModules = []


# Set up command line argument options for main script
def ParseArgs(parser):
    parser.add_option("-o", "--output", action="store_true", dest="printoutput", default=False, help="Print outputs (not relevant for all modules)")
    parser.add_option("--listmodules", action="store_true", dest="listmodules", default=False, help="List registered test modules")
    options, args = parser.parse_args()
    return options, args


# Set log preferences
def SetupLogging():
    log.setLevel(LOGLEVEL)

    logHandler = logging.StreamHandler()
    logHandler.setLevel(LOGLEVEL)
    logFormat = logging.Formatter(LOGFORMAT)
    logHandler.setFormatter(logFormat)
    log.addHandler(logHandler)

    logFileHandler = logging.FileHandler(LOGFILE)
    logFileHandler.setLevel(LOGLEVEL)
    logFormat = logging.Formatter(LOGFILEFORMAT)
    logFileHandler.setFormatter(logFormat)
    log.addHandler(logFileHandler)


def main():
    # Title
    print('+-----------------------------')
    print('| ' + SCRIPTTITLE + ' ' + SCRIPTVERSION)
    print('|')
    print('| ' + SCRIPTCOPYRIGHT)
    print('+-----------------------------')
    print(' ')

    # Setup logger and modules
    SetupLogging()
    registeredModules.append(primenumbers)
    registeredModules.append(waves)
    registeredModules.append(encrypt_xor)
    registeredModules.append(location)
    registeredModules.append(eightball)
    registeredModules.append(dice)
    registeredModules.append(headsortails)
    registeredModules.append(pwgen)
    registeredModules.append(namegen)
    registeredModules.append(fractiontests)

    # Setup args for all modules, then parse
    parser = optparse.OptionParser()
    for m in registeredModules:
        m.setup_args(parser)
    options, args = ParseArgs(parser)
    log.debug("options: " + str(options))

    # List modules
    if options.listmodules is not None and options.listmodules == True:
        log.info('Listing ' + str(len(registeredModules)) + ' registered test modules:')
        print('')
        for m in registeredModules:
            log.info(m.get_name())
        print('')
        log.info('End of list.')
        return

    # Run modules
    for m in registeredModules:
        if m.check_args(options=options):
            m.run(options=options, log=log)
            return


# Kick off the shit...
if __name__=='__main__':
    try:
        print ''
        main()
        print ''
    except KeyboardInterrupt:
        log.error('Cancelled')
