#!/usr/bin/python
import os
import sys
import platform

# Library dependency!
import pyttsx


# Script info
SCRIPTTITLE = 'Text-to-Speech'
SCRIPTVERSION = '0.1'
SCRIPTINFO = 'Speak text out loud'
SCRIPT_HELP = """
Usage:
  --speak [file/text] [property=value] [voices] [help]

Examples:
  --speak "Hello World"
      Speaks "Hello World"

  --speak /Users/somebody/Desktop/some_text.txt
      Speaks the contents of a plain text file

  --speak "Hello World" voice=Vicki rate=50
      Speaks "Hello World" with Vicki's voice, and very slow

  --speak voices
      Lists all supported voices and their properties

file/text
    Either a full path to a plain text file, or the text to speak.
    Enclose text in quotation marks if it contains spaces.

property=value
    Change engine properties.
    Supported properties:
        rate
        voice
        volume

voices
    Print a list of all supported voices and their properties.

help
    Displays this help, so you propably already know this one.
"""


drivers = {
    'osx' : 'nsss',
    'win' : 'sapi5',
    'linux' : 'espeak'
}


def open_textfile(log, filename):
    with open(filename, 'r') as textFile:
        text = textFile.read()
    return text


def get_os():
    syst = platform.system()
    if syst == 'Darwin':
        return 'osx'
    elif syst == 'Windows':
        return 'win'
    elif syst == 'Linux':
        return 'linux'
    else:
        raise ValueError('Unknown platform: ' + syst)


def get_engine_properties(engine):
    properties = {
        'voices' : engine.getProperty('voices'),
        'voice'  : engine.getProperty('voice'),
        'rate'   : engine.getProperty('rate'),
        'volume' : engine.getProperty('volume')
    }
    return properties

def set_engine_properties(engine, properties):
    for prop in properties:
        if prop == 'voices':
            continue
        engine.setProperty(prop, properties[prop])


def parse_engine_properties(engine, args):
    properties = get_engine_properties(engine)
    for arg in args[1:]:
        # We're only looking for args containing '='
        if '=' not in arg or ('=' in arg and '"' in arg):
            continue

        # Split arg in key and value
        k, v = arg.split('=')

        # We're only looking for args that correspond to a key in the engine properties
        if k not in properties:
            continue

        # Some properties have to be float
        if k == 'rate' or k == 'volume':
            v = float(v)

        # Voice property: find the correct voice, without the reverse domain crap
        # NOTE: Not tested on Windows and Linux yet!
        if k == 'voice':
            # Iterate all voices
            for voice in properties['voices']:
                # If current voice ends with v
                if voice.id.endswith(v):
                    # Set v to current voice id, then cancel loop
                    v = voice.id
                    break

        # Set property
        properties[k] = v

    return properties


def speak(engine, text):
    """
    """
    # Speak
    engine.say(text)
    engine.runAndWait()


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
    optGroup.add_option('--speak', action='store_true', dest='speak', default=None, help=SCRIPTINFO)


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.speak is not None


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
    if len(args) == 0:
        log.error('You have to provide a sentence to speak')
        sys.exit()
    return len(args) > 0


# Return module name
def get_name():
    return SCRIPTTITLE + ' ' + SCRIPTVERSION


# Return module info
def get_info():
    return SCRIPTINFO


# Calculate prime numbers op to limit
def run(log, options, args):
    # Welcome
    log.info(get_name())

    # Init engine
    ttsEngine = pyttsx.init(driverName=drivers[get_os()])

    # Parse args
    for arg in args:
        if arg.upper() == 'HELP':
            print(SCRIPT_HELP)
            sys.exit()
        elif arg.upper() == 'VOICES':
            voices = ttsEngine.getProperty('voices')
            print('Listing engine voices...')
            for voice in voices:
                print(voice.name + ' (age=' + str(voice.age) + '; gender=' + str(voice.gender) + '; languages=' + str(voice.languages) + ')')
            print('')
            sys.exit()

    if os.path.exists(args[0]):# and os.path.isfile(arg[0]):
        # First argument is filename of file to open and speak
        text = open_textfile(log, args[0])
        log.info('Speaking contents of ' + args[0] + '...')
    else:
        # First argument is the text to speak
        text = args[0]
        log.info('Speaking ' + text + '...')

    # Set engine properties according to args
    engineProperties = parse_engine_properties(ttsEngine, args)
    set_engine_properties(ttsEngine, engineProperties)

    # Speak
    speak(ttsEngine, text)
