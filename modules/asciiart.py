#!/usr/bin/python
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
# check_args(log, options)
#    Return True if main function can be run, depending on the command line arguments. If not dependent on any arguments, just return True
#    logger object and command line options dictionary are passed
#
# check_additional_args(log, options)
#    Return True if all arguments are not only set, but also make sense
#    logger object and command line options dictionary are passed
#
# run(log, options)
#    Main function where all the magic's happening.
#    logger object and command line options dictionary are passed


# Add command line arguments for this script to args parser
def setup_args(optGroup):
    optGroup.add_option('--asciiart', type='string', dest='asciiart', default=None, help=SCRIPTINFO, metavar='INPUTFILE')
    optGroup.add_option('--asciifile', type='string', dest='asciifile', default=None, help='Write ASCII art to this file', metavar='OUTPUTFILE')


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.asciiart is not None and options.asciiart != ''


# Checks additional arguments and prints error messages
def check_additional_args(log, options):
    if options.asciifile is not None and options.asciifile == '':
        log.error('When using --asciifile, you need to specify a filename!')
        return False
    return True


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
    print('')

    fileName = options.asciiart
    outputFile = options.asciifile

    log.info('Creating ASCII art from ' + fileName)

    resultImage = handle_image_conversion(fileName)
    if resultImage != None and resultImage != '':
        print(resultImage)

        if outputFile is not None and outputFile != '':
            log.info('Writing ASCII output to ' + outputFile)
            WriteOutputFile(outputFile, resultImage, log)
    else:
        log.error('Could not create ASCII art from ' + fileName)
