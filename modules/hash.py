#!/usr/bin/python
import os
import sys
import hashlib
import binascii

# Script info
SCRIPTTITLE = 'Hash'
SCRIPTVERSION = '0.1'
SCRIPTINFO = 'Hashing stuff'


# Quick CRC32 implementation
class HashCRC32:
    content = ''

    def update(this, source):
        this.content += source

    def hexdigest(this):
        result = binascii.crc32(this.content) & 0xFFFFFFFF
        return "%08X" % result


# List of available hashing algorithms
hashModes = {}
hashModes['md5'] = hashlib.md5
hashModes['sha1'] = hashlib.sha1
hashModes['sha224'] = hashlib.sha224
hashModes['sha256'] = hashlib.sha256
hashModes['sha384'] = hashlib.sha384
hashModes['sha512'] = hashlib.sha512
hashModes['crc32'] = HashCRC32


# Return True if source is the path of an existing file
def is_file(source):
    path = os.path.abspath(source)
    if os.path.exists(path):
        if os.path.isfile(path):
            return True
        return False
    else:
        return False


# Load a file and return its content
def load_file(log, path):
    try:
        path = os.path.abspath(path)
        with open(path, 'r') as file:
            content = file.read() 
            file.close()
        log.info('Loaded content from file ' + path)

    except:
        log.error('Could not load file ' + path)
        sys.exit()

    return content


# Calculate hash
def do_hash(log, mode, source):
    if is_file(source):
        hashSource = load_file(log, source)
        sourceType = 'file'
    else:
        hashSource = source
        sourceType = 'string'

    log.info('Computing ' + mode.upper() + ' hash of ' + sourceType + ' "' + source + '"...')

    hashObject = hashModes[mode]()
    hashObject.update(hashSource)

    return hashObject.hexdigest()


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
# check_args(log, options)
#    Return True if main function can be run, depending on the command line arguments. If not dependent on any arguments, just return True
#    logger object and command line options dictionary are passed
#
# check_additional_args(log, options)
#    Return True if all arguments are not only set, but also make sense
#    logger object and command line options dictionary are passed
#
# run(log, options)
#    Main function where all the magic's happening.
#    logger object and command line options dictionary are passed


# Add command line arguments for this script to args parser
def setup_args(optGroup):
    optGroup.add_option('--hash', type="string", dest='hash', default=None, nargs=2, help='Compute hash from SOURCE (either the path of an existing file, or just some string). Possible values for MODE: ' + str(hashModes.keys()) + '.', metavar='MODE SOURCE')


# Return True if args/options tell us to run this module
def check_args(log, options, args):
    return options.hash is not None and len(options.hash) == 2


# Checks additional arguments and prints error messages
def check_additional_args(log, options, args):
    if options.hash[0] not in hashModes.keys():
        log.error('Mode ' + options.hash[0] + ' is not supported!')
        log.error('Use one of the following modes: ' + str(hashModes.keys()))
        sys.exit()
    return options.hash[0] in hashModes.keys()


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Return module info
def get_info():
    return SCRIPTINFO


# Perform
def run(log, options, args):
    # Welcome
    log.info(get_name())
    print('')

    # Get args
    hashMode = options.hash[0]
    hashSource = options.hash[1]

    hashResult = do_hash(log, hashMode, hashSource)

    log.info(hashResult)
