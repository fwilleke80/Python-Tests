#!/usr/bin/python
import sys

# Get googletrans here: https://pypi.org/project/googletrans/
import googletrans


# Script info
SCRIPTTITLE = 'Google Translate'
SCRIPTVERSION = '0.1'
SCRIPTINFO = 'Translate text from and to any language.'


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
    optGroup.add_option('--source', type='string', dest='googletranslate_source', default='auto', help='Source language (default=auto; examples: de, en, fr, ...)', metavar='SOURCE')
    optGroup.add_option('--dest', type='string', dest='googletranslate_dest', default='en', help='Destination language (default=en', metavar='DEST')


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

    # Get args
    fromLang = options.googletranslate_source
    toLang = options.googletranslate_dest
    text = options.googletranslate

    if not validate_language(fromLang):
        log.error('Invalid source language!')
        sys.exit()

    if not validate_language(toLang):
        log.error('Invalid destination language!')
        sys.exit()

    google_translate(fromLang, toLang, text, log)
