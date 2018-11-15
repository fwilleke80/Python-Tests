#!/usr/bin/python

import optparse
import logging

from modules import primenumbers
from modules import waves
from modules import encrypt_xor
from modules import encrypt_caesar
from modules import location
from modules import eightball
from modules import dice
from modules import headsortails
from modules import pwgen
from modules import namegen
from modules import fractiontests
from modules import artworkprice


# Script info
SCRIPTTITLE = 'Tool Script Launcher'
SCRIPTVERSION = '0.2.5'
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
def SetupArgs(parser):
    optGroup = optparse.OptionGroup(parser, 'General options', 'Not specific to any module')
    optGroup.add_option('-o', '--output', action='store_true', dest='printoutput', default=False, help='Print outputs (not relevant for all modules)')
    optGroup.add_option('--listmodules', action='store_true', dest='listmodules', default=False, help='List registered test modules')
    parser.add_option_group(optGroup)


# Parse provided command line arguments
def ParseArgs(parser):
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
    registeredModules.append(encrypt_caesar)
    registeredModules.append(location)
    registeredModules.append(eightball)
    registeredModules.append(dice)
    registeredModules.append(headsortails)
    registeredModules.append(pwgen)
    registeredModules.append(namegen)
    registeredModules.append(fractiontests)
    registeredModules.append(artworkprice)

    # Setup args for all modules, then parse
    parser = optparse.OptionParser()
    SetupArgs(parser)
    for m in registeredModules:
        m.setup_args(parser)
    options, args = ParseArgs(parser)
    log.debug('options: ' + str(options))

    # List modules
    if options.listmodules is not None and options.listmodules == True:
        log.info('Listing ' + str(len(registeredModules)) + ' registered tool modules:')
        print('')
        for m in registeredModules:
            log.info(m.get_name())
            log.info('        ' + m.get_info())
            print('')
        return

    # Run modules
    for m in registeredModules:
        if m.check_args(options=options, log=log):
            m.run(options=options, log=log)
            return

    # If no module was used, print help
    parser.print_help()

# Kick off the shit...
if __name__=='__main__':
    try:
        print ''
        main()
        print ''
    except KeyboardInterrupt:
        log.error('Cancelled')
