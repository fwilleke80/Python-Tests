#!/usr/bin/python
from itertools import cycle, izip


# Script info
SCRIPTTITLE = 'XOR Encryption'
SCRIPTVERSION = '0.2.1'
SCRIPTINFO = 'Encrypt or decrypt a string using XOR encryption'


# Encrypt msg with key using XOR
def xor_encrypt(msg, key):
    return ''.join(chr(ord(c)^ord(k)) for c,k in izip(msg, cycle(key)))


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
    optGroup.add_option('--xor', type='string', dest='encrypt_xor', nargs=2, help='Encrypt MSG with KEY using XOR encryption', metavar='MSG KEY')


# Return True if args/options tell us to run this module
def check_args(log, options, args):
    return options.encrypt_xor is not None and options.encrypt_xor[0] != '' and options.encrypt_xor[1] != ''


# Checks additional arguments and prints error messages
def check_additional_args(log, options, args):
    return True


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Return module info
def get_info():
    return SCRIPTINFO


# Perform Encryption test
def run(log, options, args):
    # Welcome
    log.info(get_name())

    # Get arguments
    args = options.encrypt_xor
    inputStr = args[0]
    keyStr = args[1]
    print('Msg:       ' + inputStr)
    print('Key:       ' + keyStr)
    print('')

    # Encrypt
    encryptedStr = xor_encrypt(inputStr, keyStr)
    print('Encrypted: ' + encryptedStr)

    # Decrypt
    decryptedStr = xor_encrypt(encryptedStr, keyStr)
    print('Decrypted: ' + decryptedStr)

    # Check results
    if decryptedStr == inputStr:
        log.debug('Test passed! Decrypted string equals input msg!')
    else:
        log.error('Test failed! Decrypted string does not equal input msg!!')
