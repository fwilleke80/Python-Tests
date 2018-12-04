#!/usr/bin/python
from itertools import cycle, izip


# Script info
SCRIPTTITLE = 'Caesar Cypher'
SCRIPTVERSION = '0.1.1'
SCRIPTINFO = 'Encrypt a string using the ancient Caesar cypher'


L2I = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ',range(26)))
I2L = dict(zip(range(26),'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

# Encrypt msg with shiftVal using Caesar
def caesar_encrypt(msg, shiftVal):
    cyptherText = ''
    for c in msg.upper():
        if c.isalpha(): cyptherText += I2L[ (L2I[c] + shiftVal)%26 ]
        else: cyptherText += c
    return cyptherText

# Decrypt msg with shiftVal using Caesar
def caesar_decrypt(msg, shiftVal):
    cyptherText = ''
    for c in msg.upper():
        if c.isalpha(): cyptherText += I2L[ (L2I[c] - shiftVal)%26 ]
        else: cyptherText += c
    return cyptherText


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
    optGroup.add_option('--caesar', type='string', dest='encrypt_caesar', nargs=2, help='Encrypt MSG with SHIFT using Caesar encryption', metavar='MSG SHIFT')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.encrypt_caesar is not None and options.encrypt_caesar[0] != '' and options.encrypt_caesar[1] != ''


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
    shiftVal = unicode(options.encrypt_caesar[1], 'utf-8')
    if shiftVal.isnumeric() == False:
        log.error('SHIFT must be a number!')
        return False
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
    args = options.encrypt_caesar
    inputStr = args[0].upper()
    shiftVal = int(args[1])
    print('Msg:       ' + inputStr)
    print('Shift:     ' + args[1])
    print('')

    # Encrypt
    encryptedStr = caesar_encrypt(inputStr, shiftVal)
    print('Encrypted: ' + encryptedStr)

    # Decrypt
    decryptedStr = caesar_decrypt(encryptedStr, shiftVal)
    print('Decrypted: ' + decryptedStr)

    # Check results
    if decryptedStr == inputStr:
        log.debug('Test passed! Decrypted string equals input msg!')
    else:
        log.error('Test failed! Decrypted string does not equal input msg!!')
