#!/usr/bin/python
import optparse
import logging
import pkgutil
import importlib


# Script info
SCRIPTTITLE = 'Tool Script Launcher'
SCRIPTVERSION = '0.3'
SCRIPTCOPYRIGHT = '2018 by Frank Willeke'


# Logging
LOGLEVEL = logging.INFO
LOGFILE = 'test.log'
LOGFORMAT = '%(levelname)s: %(message)s'
LOGFILEFORMAT = '%(asctime)s: %(levelname)s: %(message)s'
log = logging.getLogger('log')


# Import modules from "modules" package folder
registeredModules = []
def ImportModules(log):
    import modules
    log.debug('Loading ' + str(len(modules.__all__)) + ' modules...')
    if len(modules.excludedModules) > 0:
        log.debug('Excluded modules: ' + str(modules.excludedModules))
    for m in modules.__all__:
        try:
            registeredModules.append(importlib.import_module(m))
            log.debug('Imported module ' + m)
        except:
            log.error('Could not import module ' + m + '!')


# Set up command line argument options for main script
def SetupArgs(parser):
    parser.add_option('-o', '--output', action='store_true', dest='printoutput', default=False, help='Print outputs (not relevant for all modules)')
    parser.add_option('-l', '--listmodules', action='store_true', dest='listmodules', default=False, help='List registered test modules')


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

    # Import modules
    ImportModules(log)

    # Setup args for all modules, then parse
    parser = optparse.OptionParser()
    SetupArgs(parser)
    for module in registeredModules:
        log.debug(str(module))
        optGroup = optparse.OptionGroup(parser, module.get_name(), module.get_info())
        module.setup_args(optGroup)
        parser.add_option_group(optGroup)
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
