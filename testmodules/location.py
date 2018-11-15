#!/usr/bin/python
import logging
import sys
import urllib

# Dependency library!
import geocoder
 

# Script info
SCRIPTTITLE = 'Location'
SCRIPTVERSION = '0.1.1'
SCRIPTINFO = 'Get information about your current location'



def print_geolocation(log):
    geo = geocoder.ip('me')

    try:
        log.info('IP:          ' + geo.ip)
        log.info('GPS:         ' + str(geo.latlng))
        log.info('Street:      ' + geo.street)
        log.info('Housenumber: ' + geo.housenumber)
        log.info('Postal:      ' + geo.postal)
        log.info('City:        ' + geo.city)
        log.info('State:       ' + geo.state)

    except AttributeError as err:
        log.error("Unexpected error:" + str(err))


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
def setup_args(parser):
    parser.add_option("-l", "--location", action="store_true", dest="location", default=None, help=SCRIPTINFO)


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.location is not None and options.location == True


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
    log.info('Getting geolocation info...')
    print('')
    print_geolocation(log)
