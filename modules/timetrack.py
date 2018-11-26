#!/usr/bin/python
import sys
import time
import datetime
import json
import binascii


# Script info
SCRIPTTITLE = 'Time Tracker'
SCRIPTVERSION = '0.1'
SCRIPTINFO = 'Keep track of what you''re doing with your time'


# Constants
dataFilename = 'documents/timetrack_data.json'


# Quick CRC32 implementation
class HashCRC32:
    content = ''

    def update(this, source):
        this.content += source

    def hexdigest(this):
        result = binascii.crc32(this.content) & 0xFFFFFFFF
        return "%08X" % result


# Prepare empty data
def new_data():
    data = {
        'datapoints' : []
    }
    return data


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {'yes': True, 'y': True, 'ye': True,
             'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == "yes":
        prompt = ' [Y/n] '
    elif default == "no":
        prompt = ' [y/N] '
    else:
        raise ValueError('Invalid default answer: "%s"' % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Read data from file
def read_data(log):
    try:
        with open(dataFilename, 'r') as f:
            data = json.load(f)
        return data
    except:
        log.warning('Could not load data from ' + dataFilename + ', creating empty dataset')
        data = new_data()
        write_data(log, data)
        return data


# Write data to file
def write_data(log, data):
    try:
        with open(dataFilename, 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    except:
        log.error('Could not write data to ' + dataFilename + '!')


# Get current time in standard format
def current_time():
    now = datetime.datetime.now()
    #print now
    return str(now)


def create_trackingpoint_string(datetime, task, msg, nobreaks=False):
    return datetime + ' :: ' + task + ('\n    ' if nobreaks == False else ' :: ') + msg + ('\n' if msg != '' and nobreaks == False else '')


# Add a tracking point
def add_trackingpoint(log, data, options, args):
    currentTime = current_time()

    task = args[0]
    if len(args) > 1:
        msg = ' '.join(args[1:])
    else:
        msg = ''

    trackingPointString = create_trackingpoint_string(datetime=currentTime, task=task, msg=msg, nobreaks=True)
    hashObject = HashCRC32()
    hashObject.update(trackingPointString)
    trackingPointHash = hashObject.hexdigest()

    newPoint = {
        'datetime' : currentTime,
        'taskname' : task,
        'message'  : msg,
        'hash'     : trackingPointHash
    }
    data['datapoints'].append(newPoint)
    log.info('Added point [' + trackingPointString + ']')


# List tracking points, optionally filter by task
def list_trackingpoints(log, data, options, args):
    filterString = args[0].upper() if len(args) > 0 else ''
    log.info('Listing tracking points' + ((', filtering by ' + filterString + '...') if filterString != '' else '...'))
    print('')
    dataCount = 0
    for dataPoint in data['datapoints']:
        if filterString != '':
            if filterString.upper() not in dataPoint['taskname'].upper():
                continue
        dataString = dataPoint['hash'] + ' :: ' + create_trackingpoint_string(datetime=dataPoint['datetime'], task=dataPoint['taskname'], msg=dataPoint['message'])
        print(dataString)
        dataCount += 1
    log.info('Found ' + str(dataCount) + ' tracking points.')


# 
def delete_trackingpoint(log, data, options, args):
    clearModes = ['all', 'hash', 'task', 'before', 'last']

    if len(args) >= 1:
        if args[0] not in clearModes:
            log.error('Invalid clear parameter: ' + args[0])
            return

    clearMode = ''
    clearFilter = ''

    if len(args) == 0:
        log.error('Arguments are required!')
        sys.exit()
    elif len(args) > 0:
        clearMode = args[0]
        if len(args) > 1:
            clearFilter = args[1]

    log.debug('clearMode=' + clearMode + '; clearFilter=' + clearFilter)

    if query_yes_no('Do you really want to clear tracking point(s)?') == False:
        return

    if clearMode == 'all':
        data['datapoints'] = []
        log.info('All tracking points were deleted!')
        return

    for dataPoint in data['datapoints']:
        if clearMode == 'hash':
            dataCompare = dataPoint['hash'].upper()
        elif clearMode == 'task':
            dataCompare = dataPoint['taskname'].upper()
        else:
            log.error('Not implemented yet.')
            sys.exit()

        if dataCompare == clearFilter.upper():
            data['datapoints'].remove(dataPoint)
            log.info('Tracking point ' + clearFilter + ' deleted.')
            return

    log.info('Tracking point ' + clearFilter + ' not found!')


# Prepare tracking options
timeTrackOptions = {}
timeTrackOptions['add'] = add_trackingpoint
timeTrackOptions['list'] = list_trackingpoints
timeTrackOptions['delete'] = delete_trackingpoint


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
    optGroup.add_option('--timetrack', type='string', dest='timetrack', default=None, nargs=1, help='Use the time tracker (possible options: ' + str(timeTrackOptions.keys()) + ')', metavar='OPTION')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    # print options
    return options.timetrack is not None


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
    option = options.timetrack

    if option not in timeTrackOptions:
        log.error('Invalid track option ' + option + '!')
        sys.exit()

    if option == 'add' and len(args) < 1:
        log.error('What is it you want to add? Try "--timetrack add TASKNAME MESSAGE"')
        sys.exit()

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
    trackOption = options.timetrack

    # Load existing data
    data = read_data(log)
    #print data

    # Perform track option
    timeTrackOptions[trackOption](log, data, options, args)

    # Write data
    #print data
    write_data(log, data)
