#!/usr/bin/env python
import os
import sys
import time
import fnmatch
import shutil


# Script info
SCRIPTTITLE = 'FileSort'
SCRIPTVERSION = '1.0'
SCRIPTINFO = 'Sort files into subfolders by date'


# Constants
fileextensions = (".PNG",".png",".JPG",".jpg",".jpeg",".TIF",".tif",".CR2",".cr2",".aae",".AAE",".xmp",".XMP")#,".MP4",".mp4",".MOV",".mov")
verboseoutput = False


"""
Do stuff with file
"""
def HandleFile(file, parentfolder, folderlist, errorlist):
	if verboseoutput:
		print "\nHandling file", file, "in", parentfolder, "..."

	# 1. Get file modification date
	created_date = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(file)))
	if verboseoutput:
		print "-> Date: ", created_date

	# Create target folder name
	targetfolder = os.path.join(parentfolder, created_date)
	if verboseoutput:
		print "-> Target folder: ", targetfolder

	# Add target folder to list, if it's not already in there
	if created_date not in folderlist:
		folderlist.append(created_date)

	# 2. Check if targetfolder already exists
	if not os.path.isdir(targetfolder):
		# Create it, if necessary
		if verboseoutput:
			print "-> -> Creating folder"
		try:
			os.mkdir(targetfolder)
		except Exception:
			errorstring = "Could not create folder: " + targetfolder
			errorlist.append(errorstring)
			return folderlist, 0, errorlist

	# 3. Move file to target folder
	if verboseoutput:
		print "-> Moving file..."
	try:
		shutil.move(file, targetfolder)
	except Exception:
		errorstring = "File already exists: " + os.path.join(targetfolder, file)
		errorlist.append(errorstring)
		return folderlist, 0, errorlist

	return folderlist, 1, errorlist


"""
Iterate over all files in a folder
"""
def IterateFiles(folder, mask):
	count_files = 0
	file_moved = 0
	folderlist = []
	errorlist = []
	if verboseoutput:
		print "Iterating: ", folder, "..."

	# Iterate files in folder
	for file in os.listdir(folder):
		if file.endswith(mask):
			if verboseoutput:
				print "File found: ", file

			# Process file
			folderlist, file_moved, errorlist = HandleFile(file, folder, folderlist, errorlist)
			count_files += file_moved

	return count_files,folderlist,errorlist


"""
Kick off the shit!
"""
def main():
	# Current directory
	folder = os.getcwd()

	# Print settings
	errorlist = []
	print versionstring, "\n"
	print "File Extensions:", fileextensions, "\n"

	# Iterate files in folder
	count_files,folderlist,errorlist = IterateFiles(folder, fileextensions)

	# Print summary
	print "\n", count_files, "files moved into", len(folderlist), "folders."
	if len(folderlist) > 0:
		for folder in folderlist:
			print folder

	if len(errorlist) > 0:
		print "\n", len(errorlist), " errors have occurred:"
		for errorstring in errorlist:
			print errorstring
	else:
		print "\nNo errors occurred.\n"


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

    sourceFolder = os.getcwd()
    targetFolder = ''

    if len(args) > 0:
        for argIndex, arg in enumerate(args):
            if (arg[:3].upper() == 'SRC' or arg[:6].upper() == 'SOURCE') and '=' in arg:
                sourceFolder = arg.split('=')[1]
            elif (arg[0].upper() == 'T' or arg[:6].upper() == 'TARGET') and '=' in arg:
                targetFolder = arg.split('=')[1]
            elif '=' in arg:
                log.error('Invalid argument syntax!')
                sys.exit()
            else:
                if argIndex == 0:
                    sourceFolder = arg
                if argIndex == 1:
                    targetFolder = arg

    if targetFolder == '':
        targetFolder = sourceFolder

    log.info('Source folder: ' + sourceFolder)
    log.info('Target folder: ' + targetFolder)

    # Get args
    return
