#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import string


# Script info
SCRIPTTITLE = 'Readability statistics'
SCRIPTVERSION = '0.1'
SCRIPTINFO = 'Analyze texts for readability'


############################################################
#
# Constants
#
############################################################

sentenceDelimiters = ['.', '!', '?', ':', '"'] # , '\n']
umlauts = ['ö', 'ä', 'ü', 'Ö', 'Ä', 'Ü', 'ß']
whitespaces = string.whitespace
vowels = 'aeiouy'


############################################################
#
# File operations
#
############################################################

# Load a file and return its content
def load_file(log, path):
    try:
        path = os.path.abspath(path)
        with open(path, 'r') as file:
            content = file.read() 
            file.close()
        log.info('Loaded content from file ' + path)

    except:
        log.error('Could not load file ' + path)
        sys.exit()

    return content


############################################################
#
# Custom print functions
#
############################################################

# Print a list, one line per element
def print_list(lst):
    for l in lst:
        print l


# Print results dictionary
def print_results(log, results):
    # Prerun to determine max width of keys
    maxLen = 0
    for key in results.keys():
        maxLen = max(maxLen, len(key))

    for key in sorted(results.keys()):
        result = results[key]
        margin = maxLen - len(key)
        if type(result) == float:
            resultStr = "{:10.3f}".format(result)
        elif type(result) == int:
            resultStr = "%6o"% (result)
        else:
            resultStr = str(result)

        line = key + (" " * margin) + ': ' + resultStr
        log.info(line)


############################################################
#
# Basic string operations
#
############################################################

# Remove leading non-alphanumerics from string
def trim_leading_nonalphanumerics(s):
    while s[0] not in string.letters:
        s = s[1:]
        if len(s) == 0:
            break
    return s


# Remove leading and trailing whitespaces,
# leading non-alphanumerics, and line breaks from string
def cleanup_string(s):
    s = s.strip()
    s = trim_leading_nonalphanumerics(s)
    s = s.replace('\n', '')
    return s


# Find, but with a list of strings to find
def find_nearest(text, findList, beg=0):
    pos = -1
    for s in findList:
        posOfThisItem = text.find(s, beg)
        if posOfThisItem != -1:
            if pos == -1:
                pos = posOfThisItem
            else:
                pos = min(pos, posOfThisItem)
    return pos


# Split a text into sentences, return as list of strings
def split_into_sentences(text):
    sentences = []
    previousPos = -1
    pos = -1
    while pos < len(text):
        # Find end of next sentence, starting after previously found position
        pos = find_nearest(text, sentenceDelimiters, previousPos + 1)

        # Found a valid position for end of next sentence
        if pos >= 0:
            sentence = text[previousPos+1:pos+1]
            sentence = cleanup_string(sentence)
            if len(sentence) > 2:
                sentences.append(sentence)
            previousPos = pos
        else:
            break
    return sentences


# Split a text into words, return as list of strings
def split_into_words(text):
    words = []
    for word in text.split(" "):
        word = cleanup_string(word)
        if word != '':
            words.append(word)
    return words


# Split a text into paragraphs, return as list of strings
def split_into_paragraphs(text):
    paragraphs = [paragraph for paragraph in text.split('\n')]
    return paragraphs


############################################################
#
# Text analysis
#
############################################################

# 
def compute_average_word_length(words):
    wordLength = 0
    for word in words:
        wordLength += len(word)
    return float(wordLength) / float(len(words))


# 
def compute_average_wordcount_per_string(strings):
    wordCount = 0
    for s in strings:
        wordCount += len(split_into_words(s))
    return float(wordCount) / float(len(strings))


# 
def compute_average_sentencecount_per_string(strings):
    sentenceCount = 0
    for s in strings:
        sentenceCount += len(split_into_sentences(s))
    return float(sentenceCount) / float(len(strings))


#
def compute_average_syllables_per_word(words):
    syllableCount = 0
    for word in words:
        syllableCount += count_syllables(word)
    return float(syllableCount) / float(len(words))


# 
def compute_flesch_reading_ease(asl, asw):
    return 180.0 - asl - (58.5 * asw)


# 
def assess_flesch_reading_ease(fre):
    if fre < 0.0:
        return 'Invalid FRE index'
    elif fre <= 30.0:
        return 'very difficult'
    elif fre <= 50.0:
        return 'difficult'
    elif fre <= 60.0:
        return 'medium difficult'
    elif fre <= 70.0:
        return 'medium'
    elif fre <= 80.0:
        return 'medium easy'
    elif fre <= 90.0:
        return 'easy'
    elif fre <= 100.0:
        return 'very easy'


# 
def compute_flesch_kincaid_grade_level(asl, asw):
    return (0.39 * asl) + (11.8 * asw) - 15.59


#
def compute_gunning_fog_index(words, w, s, d):
    return ((w / s) + d) * 0.4


# Erste Wiener Sachtextformel
def compute_wiener_sachtextformel(MS, SL, IW, ES):
    wstf1 = 0.1935 * MS + 0.1672 * SL + 0.1297 * IW - 0.0327 * ES - 0.875
    wstf2 = 0.2007 * MS + 0.1682 * SL + 0.1373 * IW - 2.779
    wstf3 = 0.2963 * MS + 0.1905 * SL - 1.1144
    wstf4 = 0.2656 * SL + 0.2744 * MS - 1.693
    return (wstf1, wstf2, wstf3, wstf4)


# Count letters in text, omitting anything that is not a letter or umlaut
def count_letters(text):
    pureText = ''.join(ch for ch in text if (ch in string.letters or ch in umlauts))
    return len(pureText)


#
def count_syllables(word):
#referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    count = 0
    word = word.lower()

    if word[0] in vowels:
        count +=1

    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1

    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1

    if count == 0:
        count +=1

    return count


# Analyze a text, return dictionary with results
def analyze_text(log, text):
    results = {}

    # Get separate paragraphs
    paragraphs = split_into_paragraphs(text)

    # Get separate sentences
    sentences = split_into_sentences(text)

    # Get separate words
    words = split_into_words(text)

    # Build results dictionary
    results['Total paragraphs'] = len(paragraphs)
    results['Total sentences'] = len(sentences)
    results['Total words'] = len(words)
    results['Total letters'] = count_letters(text)

    asl = compute_average_wordcount_per_string(sentences)
    asw = compute_average_syllables_per_word(words)

    results['Average words p. sentence'] = asl
    results['Average sentences p. paragraph'] = compute_average_sentencecount_per_string(paragraphs)
    results['Average word length'] = compute_average_word_length(words)
    results['Average syllables p. word'] = asw

    fre = compute_flesch_reading_ease(asl=asl, asw=asw)
    results['Flesch-Reading-Ease (DE) Index'] = fre
    results['Flesch-Reading-Ease (DE) Assessment'] = assess_flesch_reading_ease(fre).upper()

    fkgl = compute_flesch_kincaid_grade_level(asl=asl, asw=asw)
    results['Flesch-Kincaid-Grade-Level (US)'] = fkgl

    # Count words with at least 3 syllables
    words_with_at_least_3_syllables = 0
    for word in words:
        if count_syllables(word) >= 3:
            words_with_at_least_3_syllables += 1


    gfi = compute_gunning_fog_index(words, w=len(words), s=len(sentences), d=words_with_at_least_3_syllables)
    results['Gunning-Fog-Index (US)'] = gfi

    words_with_at_least_6_letters = 0
    for word in words:
        if count_letters(word) >= 6:
            words_with_at_least_6_letters += 1

    words_with_only_one_syllable = 0
    for word in words:
        if count_syllables(word) == 1:
            words_with_only_one_syllable += 1

    ms = (len(words) / words_with_at_least_3_syllables)
    iw = (len(words) / words_with_at_least_6_letters)
    es = (len(words) / words_with_only_one_syllable)
    wsf = compute_wiener_sachtextformel(MS=ms, SL=asl, IW=iw, ES=es)

    results['Wiener Sachtextformel 1'] = wsf[0]
    results['Wiener Sachtextformel 2'] = wsf[1]
    results['Wiener Sachtextformel 3'] = wsf[2]
    results['Wiener Sachtextformel 4'] = wsf[3]

    return results


############################################################
#
# Module integration
#
############################################################
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
    optGroup.add_option('--readability', type="string", dest='readability', default=None, help='Analyze a text file for readability.', metavar='FILE')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.readability is not None and options.readability != ''


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
    filename = options.readability

    # Load file
    text = load_file(log, filename)
    print('')

    results = analyze_text(log, text)

    print_results(log, results)
