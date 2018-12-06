#!/usr/bin/python
import sys
import optparse
from PIL import Image


################################################################################
# Taken from:
# https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# by Praveen Kumar
################################################################################


# Script info
SCRIPTTITLE = 'ASCII Art Generator'
SCRIPTVERSION = '0.1.1'
SCRIPTINFO = 'Generate ASCII Art from an image file'
SCRIPT_HELP = """
Usage:
  --asciiart INPUTFILE [outputfile]

Examples:
  --asciiart /Users/somebody/Desktop/portrait.jpg
      Generate ASCII art from the specified JPG file.

  --asciiart /Users/somebody/Desktop/portrait.jpg /Users/somebody/Desktop/portrait_ascii.txt
      Generate ASCII art from the specified JPG file, and store it in the specified TXT file

INPUTFILE
    You must provide the full absolute path to an image file to generate ASCII art from.

outputfile
    Optionally, specify a full absolute path to write a text file with the generated ascii art.

help
    Displays this help, so you propably already know this one.
"""


ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[pixel_value/range_width] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            xrange(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception, e:
        print "Unable to open image file {image_filepath}.".format(image_filepath=image_filepath)
        print e
        return

    image_ascii = convert_image_to_ascii(image)
    return image_ascii


def WriteOutputFile(filename, ascii, log):
    try:
        with open(filename, 'w') as f:
            f.write(ascii)
            f.close()
    except:
        log.error('Could not write file ' + filename)


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
    optGroup.add_option('--asciiart', type='string', dest='asciiart', default=None, help=SCRIPTINFO, metavar='INPUTFILE')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.asciiart is not None and options.asciiart != ''


# Checks additional arguments and prints error messages
def check_additional_options(log, options, args):
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
    print('')

    # Parse args
    fileName = options.asciiart
    outputFile = None
    for arg in args:
        if arg.upper() == 'HELP':
            print(SCRIPT_HELP)
            print('')
            sys.exit()
        outputFile = arg

    log.info('Creating ASCII art from ' + fileName)

    resultImage = handle_image_conversion(fileName)
    if resultImage != None and resultImage != '':
        print(resultImage)

        if outputFile is not None and outputFile != '':
            log.info('Writing ASCII output to ' + outputFile)
            WriteOutputFile(outputFile, resultImage, log)
    else:
        log.error('Could not create ASCII art from ' + fileName)
