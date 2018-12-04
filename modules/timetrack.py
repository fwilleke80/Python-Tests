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

SCRIPT_HELP = """
Usage:
  python test.py --timetrack [list|add|delete|help] args

list [filter]
    Lists all existing tracking points, optionally filtered by a string.

add TASKNAME [message]
    Adds a new tracking point for the current date and time. Use TASKNAME to
    associate this point with a task (e.g. cooking, reading, project, whatever).
    Optionally provide a message (e.g. "Trying indian curry", "name of the book", et cetera)

delete [all|hash|task|before|last] [filter]
    Delete either all tracking points, or filter by point hash or task name. You can also
    remove all points before a defined point, or simply the last point. For the modes
    hash, task, and before, you must provide a filter as an argument.

help
    Displays this help, so you propably already know this one.
"""


# Constants
dataFilename = 'documents/timetrack_data.json'
prefsFilename = 'documents/timetrack_prefs.json'
stopMarker = 'STOP__'


###############################################################
#
# Helpers
#
###############################################################

# Quick CRC32 implementation
class HashCRC32:
    content = ''

    def update(this, source):
        this.content += source

    def hexdigest(this):
        result = binascii.crc32(this.content) & 0xFFFFFFFF
        return "%08X" % result

###############################################################
#
# Data management
#
###############################################################

# Class that holds data of one tracking point
class TrackingPoint:
    datetime = ''
    taskname = ''
    message = ''
    hash = ''

    #
    def __init__(self, *args, **kwargs):
        if kwargs.get('src', None) is not None:
            self.copy_from(src)
        elif kwargs.get('dict', None) is not None:
            self.set_from_dict(kwargs.get('dict'))
        else:
            try:
                self.set(taskname=kwargs.get('taskname'), message=kwargs.get('message'))
            except:
                self.datetime = ''
                self.taskname = ''
                self.message = ''
                self.hash = ''

    #
    def __str__(self):
        return self.taskname + ' :: ' + self.datetime + ' :: ' + self.message

    # 
    def pretty_string(self):
        return self.hash + ' :: ' + self.taskname + ' :: ' + self.datetime + (('\n    ' + self.message) if self.message != '' else '')


    # Set data
    def set(self, taskname, message):
        # Set data
        self.taskname = taskname
        self.message = message

        # Set current datetime
        self.datetime = current_time()

        # Set Hash
        hashObject = HashCRC32()
        hashObject.update(str(self))
        self.hash = hashObject.hexdigest()


    def set_from_dict(self, d):
        self.taskname = d['taskname']
        self.message = d['message']
        self.datetime = d['datetime']
        self.hash = d['hash']


    # 
    def match(self, filterString, target='all', allowEmpty=False):
        if filterString == '':
            if allowEmpty:
                return True
            else:
                return False
        result = False
        if target == 'all':
            result = filterString in self.taskname \
                or filterString in self.message \
                or filterString in self.hash \
                or filterString in self.datetime
        elif 'taskname' in target:
            result = result or (filterString in self.taskname)
        elif 'message' in target:
            result = result or (filterString in self.message)
        elif 'hash' in target:
            result = result or (filterString in self.hash)
        elif 'datetime' in target:
            result = result or (filterString in self.datetime)
        return result


# Prepare empty data
def new_data():
    data = {
        'datapoints' : []
    }
    return data


# Prepare default preferences
def new_prefs():
    prefs = {
    }
    return prefs


###############################################################
#
# General stuff
#
###############################################################

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


# Get current time in standard format
def current_time():
    now = datetime.datetime.now()
    #print now
    return str(now)


###############################################################
#
# File operations
#
###############################################################

# Read data from file
def read_data(log):
    try:
        with open(dataFilename, 'r') as f:
            data = json.load(f)
        return data
    except:
       log.warning('Could not load data from ' + dataFilename + '; creating empty dataset.')
       data = new_data()
       write_json(log, dataFilename, data)
       return data


# Read data from file
def read_prefs(log):
    try:
        with open(prefsFilename, 'r') as f:
            prefs = json.load(f)
        return prefs
    except:
        log.warning('Could not load preferences from ' + prefsFilename + '; using default settings.')
        prefs = new_prefs()
        write_json(log, prefsFilename, prefs)
        return prefs


# Write data to file
def write_json(log, filename, data):
    try:
        with open(filename, 'w') as f:
            dataDump = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            f.write(dataDump)
    except:
        log.error('Could not write data to ' + dataFilename + '!')


###############################################################
#
# Entry points
#
###############################################################

# Add a tracking point
def add_trackingpoint(log, data, options, args):
    task = args[0]
    if len(args) > 1:
        msg = ' '.join(args[1:])
    else:
        msg = ''

    newPoint = TrackingPoint()
    newPoint.set(taskname=task, message=msg)

    # Try to get list of existing datapoints
    try:
        dataPoints = data['datapoints']
    except KeyError:
        dataPoints = []

    # Append new datapoints
    dataPoints.append(newPoint.__dict__)
    data['datapoints'] = dataPoints

    log.info('Added point [' + str(newPoint) + ']')


# List tracking points, optionally filter by task
def list_trackingpoints(log, data, options, args):
    filterString = args[0].upper() if len(args) > 0 else ''
    log.info('Listing tracking points' + ((', filtering by "' + filterString + '"...') if filterString != '' else '...'))
    print('')
    dataCount = 0
    for dp in data['datapoints']:
        dataPoint = TrackingPoint(dict=dp)
        if not dataPoint.match(filterString, allowEmpty=True):
            continue
        dataString = dataPoint.pretty_string()
        print(dataString)
        print('')
        dataCount += 1
    log.info('Found ' + str(dataCount) + ' tracking points.')


# 
def delete_trackingpoint(log, data, options, args):
    clearModes = ['all', 'hash', 'task', 'before', 'last']

    if len(args) >= 1:
        if args[0] not in clearModes:
            log.error('Invalid clear parameter: ' + args[0])
            log.error('Possible parameters are: ' + str(clearModes))
            sys.exit()

    clearMode = ''
    clearFilter = ''

    if len(args) == 0:
        log.error('Arguments are required!')
        log.error('Possible parameters are: ' + str(clearModes))
        sys.exit()
    elif len(args) > 0:
        clearMode = args[0]
        if len(args) > 1:
            clearFilter = args[1]

        if (clearMode == 'hash' or clearMode == 'task' or clearMode == 'before') and clearFilter == '':
            log.error('Arguments are required for this clear mode!')
            sys.exit()

    log.debug('clearMode=' + clearMode + '; clearFilter=' + clearFilter)

    if query_yes_no('Do you really want to clear tracking point(s)?') == False:
        return

    if clearMode == 'all':
        data['datapoints'] = []
        log.info('All tracking points were deleted!')
        return
    elif clearMode == 'last':
        del data['datapoints'][-1]
        log.info('Last tracking point was deleted!')
        return

    deleteCount = 0

    for dp in data['datapoints']:
        dataPoint = TrackingPoint(dict=dp)
        if clearMode == 'hash':
            dataCompare = dataPoint.hash.upper()
        elif clearMode == 'task':
            dataCompare = dataPoint.taskname.upper()
        else:
            log.error('Not implemented yet.')
            sys.exit()

        if dataCompare == clearFilter.upper():
            data['datapoints'].remove(dp)
            log.info('Tracking point ' + clearFilter + ' deleted.')
            deleteCount += 1

    if deleteCount == 0:
        log.info('Tracking point ' + clearFilter + ' not found!')
    else:
        log.info('Deleted ' + str(deleteCount) + ' tracking points.')


# Add a tracking point that stops currently running task
def stop_task(log, data, options, args):
    ldp = data['datapoints'][-1]
    if ldp is None or stopMarker in ldp['taskname']:
        log.info('Nothing to stop here.')
        sys.exit()
    lastDataPoint = TrackingPoint(dict=ldp)

    newPoint = TrackingPoint()
    newPoint.set(taskname=stopMarker + lastDataPoint.hash, message='')

    # Try to get list of existing datapoints
    try:
        dataPoints = data['datapoints']
    except KeyError:
        dataPoints = []

    # Append new datapoint
    dataPoints.append(newPoint.__dict__)
    data['datapoints'] = dataPoints

    log.info('Stopped task ' + str(lastDataPoint))

# 
def print_help(log, data, options, args):
    print get_name()
    print SCRIPT_HELP


###############################################################
#
# Prepare tracking options
#
###############################################################

timeTrackOptions = {}
timeTrackOptions['add'] = add_trackingpoint
timeTrackOptions['list'] = list_trackingpoints
timeTrackOptions['delete'] = delete_trackingpoint
timeTrackOptions['stop'] = stop_task
timeTrackOptions['help'] = print_help


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

    # Get preferences
    preferences = read_prefs(log)

    # Load existing data
    data = read_data(log)

    # Perform track option
    timeTrackOptions[trackOption](log, data, options, args)

    # Write data
    write_json(log, dataFilename, data)
