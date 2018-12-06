#!/usr/bin/python
import sys

# Get googletrans here: https://pypi.org/project/googletrans/
import googletrans


# Script info
SCRIPTTITLE = 'Google Translate'
SCRIPTVERSION = '0.2'
SCRIPTINFO = 'Translate text from and to any language.'
SCRIPT_HELP = """
Usage:
  --translate TEXT [source=lang] [dest=lang]

Examples:
  --translate "Guten Tag, bitte geben Sie mir einen Regenschirm."
      Translate the provided sentence from any language to English.

  --translate "Guten Tag, bitte geben Sie mir einen Regenschirm." dest=it
      Translate the provided sentence from any language to the specified language (in this case Italian).

TEXT
    Any text to translate.

source
    Optionally, specify the source language here, if automatic recognition fails.

dest
    Optionally, specify teh destination language.

help
    Displays this help, so you propably already know this one.
"""


def validate_language(lang):
    return lang == 'auto' or (lang in googletrans.LANGUAGES.keys())


def google_translate(fromLang, toLang, text, log):
    translator = googletrans.Translator(service_urls=['translate.google.com'])

    if fromLang == 'auto':
        resultDetected = translator.detect(text)
        log.info('Source language: ' + resultDetected.lang + ' (Confidence: ' + str(resultDetected.confidence) + ')')
    else:
        log.info('Source language: ' + fromLang)

    log.info('Dest language:   ' + toLang)
    log.info('Original text:   ' + text)
    print('')

    resultTranslate = translator.translate(text, src=fromLang, dest=toLang)
    log.info(resultTranslate.text)


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
    optGroup.add_option('--translate', type='string', dest='googletranslate', default=None, help='Translate a text using Google Translate', metavar='TEXT')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.googletranslate is not None and options.googletranslate != ''


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
    return True


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

    # Parse args
    text = options.googletranslate
    fromLang = 'auto'
    toLang = 'en'
    for arg in args:
        arg = arg.upper()
        if (arg[0] == 'S' or arg[:6] == 'SOURCE') and '=' in arg:
            fromLang = arg.split('=')[1].lower()
        elif (arg[0] == 'D' or arg[:4] == 'DEST') and '=' in arg:
            toLang = arg.split('=')[1].lower()
        elif arg == 'HELP':
            print(SCRIPT_HELP)
            print('')
            sys.exit()

    if not validate_language(fromLang):
        log.error('Invalid source language!')
        sys.exit()

    if not validate_language(toLang):
        log.error('Invalid destination language!')
        sys.exit()

    google_translate(fromLang, toLang, text, log)
