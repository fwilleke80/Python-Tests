#!/usr/bin/env python
import os
import sys
import time
import shutil


# Script info
SCRIPTTITLE = 'FileSort'
SCRIPTVERSION = '1.0'
SCRIPTINFO = 'Sort files into subfolders by date'
SCRIPT_HELP = """
Usage:
  --sortfiles [sourcefolder] [targetfolder] [filepattern] [dry]
  --sortfiles [source=sourcefolder] [target=targetfolder] [pattern=filepattern] [dry]

Examples:
  --sortfiles
      Moves all images and movies in the current working directory to sorted folders.

  --sortfiles dry
      Simulated moving all images and movies in the current working directory to sorted folders.

  --sortfiles /Users/somebody/Desktop/newImages /Users/somebody/Pictures pattern=images
      Moves all image files from ~/Desktop/newImages to sorted folders in ~/Pictures.

source
    Defines the source folder where the files that should be sorted are located.
    If is either used with "source=" or "src=", or it's simply the first argument without "=".
    If undefined, the current working directory is used.

target
    Defines the target folder where the new subfolders should be created.
    It is either used with "target=" or "t=", or it's simply the second argument without "=".
    If undefined, the current working directory is used.

filepattern
    Defines which files should be moved, based on their file extension.
    It is either used with "pattern=" or it's simple the third argument without "=".
    Either provide a comma-separated list of file extensions here (e.g. ".jpg,.tif,.bmp"),
    or use the keywords "images", "movies", or "default" to use standard extension lists.
    If undefined, the "default" extension list will be used, that combines all other lists.

dry
    Performs a dry run. No folder are actually created, and no files are moved.
    Instead, for each file that would be moved, a message is printed.

help
    Displays this help, so you propably already know this one.
"""


# Constants
PATTERNS = {
    'images' : ('.bmp', '.BMP', '.PNG', '.png', '.JPG', '.jpg', '.jpeg', '.JPEG', '.TIF', '.tif', '.tiff', '.TIFF', '.CR2', '.cr2', '.aae', '.AAE', '.xmp', '.XMP'),
    'movies' : ('.MP4', '.mp4', '.MOV', '.mov', '.avi', '.AVI', '.mpg', '.MPG', '.mpeg', '.mpeg'),
    'default' : ('.bmp', '.BMP', '.PNG', '.png', '.JPG', '.jpg', '.jpeg', '.JPEG', '.TIF', '.tif', '.tiff', '.TIFF', '.CR2', '.cr2', '.aae', '.AAE', '.xmp', '.XMP', '.MP4', '.mp4', '.MOV', '.mov', '.avi', '.AVI', '.mpg', '.MPG', '.mpeg', '.mpeg')
}
DRY_RUN = False


# Do stuff with a file
def handle_file(log, file, sourceFolder, targetFolder, folderList, errorList, dryRun):
    file = os.path.join(sourceFolder, file)
    log.debug('Handling file ' + str(file) + ' in ' + str(sourceFolder) + '...')

    # 1. Get file modification date
    fileDate = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(file)))
    log.debug('-> Date: ' + str(fileDate))

    # Create target folder name
    targetFolder = os.path.join(targetFolder, fileDate)
    log.debug('-> Target folder: ' + str(targetFolder))

    # Add target folder to list, if it's not already in there
    if fileDate not in folderList:
        folderList.append(fileDate)

    # 2. Check if targetFolder already exists
    if not os.path.exists(targetFolder):
        # Create it, if necessary
        log.debug('-> -> Creating folder')
        try:
            if dryRun == False:
                os.makedirs(targetFolder)
        except Exception:
            errorList.append('Could not create folder: ' + str(targetFolder))
            return folderList, False, errorList

    # 3. Move file to target folder
    log.debug('-> Moving file...')
    if dryRun:
        log.info('DRY RUN: Moving ' + str(file) + ' --> ' + str(targetFolder))
    try:
        if dryRun == False:
            shutil.move(file, targetFolder)
    except Exception:
        errorList.append('File already exists: ' + os.path.join(targetFolder, file))
        return folderList, False, errorList
    return folderList, True, errorList


# Iterate over all files in a folder
def iterate_files(log, sourceFolder, targetFolder, filePattern, dryRun):
    fileCount = 0
    folderList = []
    errorList = []
    log.debug('Iterating: ' + str(sourceFolder) + '...')

    # Iterate files in folder
    for file in os.listdir(sourceFolder):
        if file.endswith(filePattern):
            # Process file
            folderlist, fileMoved, errorList = handle_file(log, file, sourceFolder, targetFolder, folderList, errorList, dryRun)
            # Set counter of processed files
            fileCount += (1 if fileMoved else 0)

    if dryRun:
        print('')

    return fileCount, folderList, errorList


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
    optGroup.add_option('--sortfiles', action='store_true', dest='sortfiles', default=None, help='Sort files into folders')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    # print options
    return options.sortfiles is not None and options.sortfiles == True


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

    # Default args
    filePattern = PATTERNS['default']
    sourceFolder = os.getcwd()
    targetFolder = ''
    dryRun = DRY_RUN

    # Parse args
    if len(args) > 0:
        for argIndex, arg in enumerate(args):
            if (arg[:3].upper() == 'SRC' or arg[:6].upper() == 'SOURCE') and '=' in arg:
                sourceFolder = arg.split('=')[1]
            elif (arg[0].upper() == 'T' or arg[:6].upper() == 'TARGET') and '=' in arg:
                targetFolder = arg.split('=')[1]
            elif (arg[0].upper() == 'P' or arg[:7].upper() == 'PATTERN') and '=' in arg:
                patternString = arg.split('=')[1]
                if patternString.lower() in PATTERNS.keys():
                    filePattern = PATTERNS[patternString]
                else:
                    filePattern = patternString.split(',')
            elif (arg.upper() == 'DRY'):
                dryRun = True
            elif (arg.upper() == 'HELP'):
                print(SCRIPT_HELP)
                sys.exit()
            elif '=' in arg:
                log.error('Invalid argument syntax!')
                sys.exit()
            else:
                if argIndex == 0:
                    sourceFolder = arg
                elif argIndex == 1:
                    targetFolder = arg
                elif argIndex == 2:
                    patternString = arg
                    if patternString.lower() in PATTERNS.keys():
                        filePattern = PATTERNS[patternString]
                    else:
                        filePattern = patternString.split(',')

    if targetFolder == '':
        targetFolder = sourceFolder

    # Make filePattern a tuple, in case it's a list
    if type(filePattern) == list:
        filePattern = tuple(filePattern)

    # Print settings
    log.info('Source folder: ' + sourceFolder)
    log.info('Target folder: ' + targetFolder)
    log.info('File Extensions: ' + str(filePattern))
    if dryRun:
        log.info('Performing DRY RUN, not actually moving or creating anything!')
    print('')

    # Iterate files in folder
    fileCount, folderList, errorList = iterate_files(log, sourceFolder, targetFolder, filePattern, dryRun)

    # Print summary
    log.info(str(fileCount) + ' files moved into ' + str(len(folderList)) + ' folders.')
    if len(folderList) > 0:
        for folder in folderList:
            print folder

    if len(errorList) > 0:
        log.error(str(len(errorList)) + ' errors have occurred')
        print('')
        for errorString in errorList:
            log.error(errorString)
    else:
        log.info('No errors occurred.')
