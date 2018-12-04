#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import string
import operator
import json
import time
import binascii
import hashlib


# Script info
SCRIPTTITLE = 'Text statistics'
SCRIPTVERSION = '0.2.2'
SCRIPTINFO = 'Analyze text files'


############################################################
#
# Constants
#
############################################################

sentenceDelimiters = '.!?:"'
umlauts = 'öäüÖÄÜß'
vowels = 'aeiouy'
whitespaces = string.whitespace


resultLabels = {
    'paragraphs' : 'Number of paragraphs',
    'sentences'  : 'Number of sentences',
    'words'      : 'Number of words',
    'letters'    : 'Number of letters',
    'words-with-at-least-3-syllables' : 'Number of words with at least 3 syllables',
    'words-with-at-least-6-letters'   : 'Number of words with at least 6 letters',
    'words-with-only-1-syllable'      : 'Number of words with only 1 syllable',
    'words-per-sentence'      : 'Average words per sentence',
    'sentences-per-paragraph' : 'Average sentences per paragraph',
    'word-length'             : 'Average word length',
    'syllables-per-word'      : 'Average syllables per word',
    'fre-index'      : 'Flesch-Reading-Ease (DE) Index',
    'fre-assessment' : 'Flesch-Reading-Ease (DE) Assessment',
    'fgkl'           : 'Flesch-Kincaid Grade Level (US)',
    'gfi'            : 'Gunning-Fog Index (US)',
    'wstf-1'         : 'Erste Wiener Sachtextformel (DE)',
    'wstf-2'         : 'Zweite Wiener Sachtextformel (DE)',
    'wstf-3'         : 'Dritte Wiener Sachtextformel (DE)',
    'wstf-4'         : 'Vierte Wiener Sachtextformel (DE)',
    'word-frequencies' : 'Word frequencies',
    'count'       : 'Count',
    'average'     : 'Average',
    'readability' : 'Readability',
    'tables'      : 'Tables',
    'meta'        : 'Metadata',
    'crc32'       : 'Checksum CRC32',
    'md5'         : 'Checksum MD5',
    'sha1'        : 'Checksum SHA1',
    'filename'    : 'Filename'
}


############################################################
#
# Checksums
#
############################################################

# Simple CRC32 generator
class HashCRC32:
    content = ''

    def update(this, source):
        this.content += source

    def hexdigest(this):
        result = binascii.crc32(this.content) & 0xFFFFFFFF
        return "%08X" % result


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


# Write results dictionary to a JSON file
def write_results(results, filename, log):
    try:
        with open(filename, 'w') as jsonFile:
            jsonFile.write(json.dumps(results, indent=4, sort_keys=True))
            jsonFile.close()
    except:
        log.error('Couldn''t write file ' + filename)


# Inject label strings into results dictionary
def add_labels(results):
    for key in results:
        value = results[key]
        results[key] = [resultLabels[key], value]
        # Recurse into sub dictionaries
        if type(value) == dict:
            add_labels(value)


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
def print_results(log, results, excludeKeys=[]):
    # Prerun to determine max width of keys
    maxLen = 0
    for key in results.keys():
        maxLen = max(maxLen, len(resultLabels[key]))


    for key in sorted(results.keys()):
        if key in excludeKeys:
            continue

        result = results[key]
        label = resultLabels[key]
        if type(result) == dict:

            log.info(label + ':')
            print_results(log, result, excludeKeys)
        else:
            margin = maxLen - len(label)
            if type(result) == float:
                resultStr = "{:10.3f}".format(result)
            elif type(result) == int:
                resultStr = "%6o"% (result)
            else:
                resultStr = str(result)

            line = label + (" " * margin) + ': ' + resultStr
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

# Count letters in text, omitting anything that is not a letter or umlaut
def count_letters(text):
    pureText = ''.join(ch for ch in text if (ch in string.letters or ch in umlauts))
    return len(pureText)


# Count syllables in a word
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


# Average word length
def compute_average_word_length(words):
    wordLength = 0
    for word in words:
        wordLength += len(word)
    return float(wordLength) / float(len(words))


# Average number of words per string
def compute_average_wordcount_per_string(strings):
    wordCount = 0
    for s in strings:
        wordCount += len(split_into_words(s))
    return float(wordCount) / float(len(strings))


# Average number of sentences per string
def compute_average_sentencecount_per_string(strings):
    sentenceCount = 0
    for s in strings:
        sentenceCount += len(split_into_sentences(s))
    return float(sentenceCount) / float(len(strings))


# Average number of syllables per word
def compute_average_syllables_per_word(words):
    syllableCount = 0
    for word in words:
        syllableCount += count_syllables(word)
    return float(syllableCount) / float(len(words))


# Flesch-Reading-Eass Index (DE)
def compute_flesch_reading_ease(asl, asw):
    return 180.0 - asl - (58.5 * asw)


# Flasch-Reading-Ease Assessment
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


# Flesch-Kincaid Grade Level (US)
def compute_flesch_kincaid_grade_level(asl, asw):
    return (0.39 * asl) + (11.8 * asw) - 15.59


# Gunning-Fog Index (US)
def compute_gunning_fog_index(words, w, s, d):
    return ((w / s) + d) * 0.4


# Wiener Sachtextformel (DE)
def compute_wiener_sachtextformel(MS, SL, IW, ES):
    wstf1 = 0.1935 * MS + 0.1672 * SL + 0.1297 * IW - 0.0327 * ES - 0.875
    wstf2 = 0.2007 * MS + 0.1682 * SL + 0.1373 * IW - 2.779
    wstf3 = 0.2963 * MS + 0.1905 * SL - 1.1144
    wstf4 = 0.2656 * SL + 0.2744 * MS - 1.693
    return (wstf1, wstf2, wstf3, wstf4)


# Build table of word frequency
def build_word_frequency_table(words):
    wordFrequencies = {}
    defaultValuePair = [0, 0.0]

    # Count word frequency
    for word in words:
        wordFrequency = wordFrequencies.get(word, defaultValuePair)[0] + 1
        valuePair = [wordFrequency, 0.0]
        wordFrequencies[word] = valuePair

    # Compute relative word frequencies
    wordCount = len(words)
    for item in wordFrequencies.itervalues():
        item[1] = float(item[0]) / float(wordCount)

    return wordFrequencies


# Generate general metadata about input file
def GenerateMetadata(log, filename, text):
    metaData = {}
    metaData['filename'] = filename
    crc = HashCRC32()
    crc.update(text)
    metaData['crc32'] = str(crc.hexdigest())
    md5 = hashlib.md5()
    md5.update(text)
    metaData['md5'] = str(md5.hexdigest())
    sha1 = hashlib.sha1()
    sha1.update(text)
    metaData['sha1'] = str(sha1.hexdigest())

    return metaData


# Analyze a text, return dictionary with results
def analyze_text(log, text):
    # Results dictionaries
    results = {}
    countResults = {}
    averageResults = {}
    readabilityResults = {}
    tableResults = {}

    # Get token lists
    paragraphs = split_into_paragraphs(text)
    sentences = split_into_sentences(text)
    words = split_into_words(text)

    # Count
    countResults['paragraphs'] = len(paragraphs)
    countResults['sentences'] = len(sentences)
    countResults['words'] = len(words)
    countResults['letters'] = count_letters(text)

    # Compute averages
    asl = compute_average_wordcount_per_string(sentences)
    asw = compute_average_syllables_per_word(words)
    averageResults['words-per-sentence'] = asl
    averageResults['sentences-per-paragraph'] = compute_average_sentencecount_per_string(paragraphs)
    averageResults['word-length'] = compute_average_word_length(words)
    averageResults['syllables-per-word'] = asw

    # Compute Flesch-Reading-Ease
    fre = compute_flesch_reading_ease(asl=asl, asw=asw)
    readabilityResults['fre-index'] = fre
    readabilityResults['fre-assessment'] = assess_flesch_reading_ease(fre).upper()

    # Compute Flesch-Kincaid Grade Level
    fkgl = compute_flesch_kincaid_grade_level(asl=asl, asw=asw)
    readabilityResults['fgkl'] = fkgl

    # Count words with at least 3 syllables
    words_with_at_least_3_syllables = 0
    for word in words:
        if count_syllables(word) >= 3:
            words_with_at_least_3_syllables += 1
    countResults['words-with-at-least-3-syllables'] = words_with_at_least_3_syllables

    # Compute Gunning-Fog Index
    gfi = compute_gunning_fog_index(words, w=len(words), s=len(sentences), d=words_with_at_least_3_syllables)
    readabilityResults['gfi'] = gfi

    # Count words with at least 6 letters
    words_with_at_least_6_letters = 0
    for word in words:
        if count_letters(word) >= 6:
            words_with_at_least_6_letters += 1
    countResults['words-with-at-least-6-letters'] = words_with_at_least_6_letters

    # Count words with only one syllable
    words_with_only_one_syllable = 0
    for word in words:
        if count_syllables(word) == 1:
            words_with_only_one_syllable += 1
    countResults['words-with-only-1-syllable'] = words_with_only_one_syllable

    # Compute Wiener Sachtextformel
    ms = len(words) / words_with_at_least_3_syllables
    iw = len(words) / words_with_at_least_6_letters
    es = len(words) / words_with_only_one_syllable
    wsf = compute_wiener_sachtextformel(MS=ms, SL=asl, IW=iw, ES=es)
    readabilityResults['wstf-1'] = wsf[0]
    readabilityResults['wstf-2'] = wsf[1]
    readabilityResults['wstf-3'] = wsf[2]
    readabilityResults['wstf-4'] = wsf[3]

    # Compute word frequency table
    wordFrequencies = build_word_frequency_table(words)
    sortedWordFrequencies = sorted(wordFrequencies.items(), key=operator.itemgetter(1))
    sortedWordFrequencies.reverse()
    tableResults['word-frequencies'] = sortedWordFrequencies

    # Assemble complete results dictionary
    results['count'] = countResults
    results['average'] = averageResults
    results['readability'] = readabilityResults
    results['tables'] = tableResults

    # Return results dictionary
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
    optGroup.add_option('--analysetext', type="string", dest='analysetext', default=None, help='Analyze a text file', metavar='FILE')
    optGroup.add_option('--writemetadata', action='store_true', dest='analysetext_writemetadata', default=None, help='Write analysis results to JSON file')


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.analysetext is not None and options.analysetext != ''


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
    filename = options.analysetext
    if options.analysetext_writemetadata is not None and options.analysetext_writemetadata == True:
        writeMetadata = True
    else:
        writeMetadata = False

    # Load text file
    text = load_file(log, filename)
    if writeMetadata:
        log.info('Will write metadata file.')
    print('')

    # Analyze text
    startTime = time.time()
    results = analyze_text(log, text)
    timePassed = time.time() - startTime

    # Add general text information
    results['meta'] = GenerateMetadata(log, filename, text)

    # Output results
    print_results(log, results, excludeKeys=['tables'])
    print('')
    log.info('Analysis finished in ' + "{:0.3f}".format(timePassed) + ' msec')

    # Write JSON file
    print('')
    add_labels(results)
    pre, ext = os.path.splitext(filename)
    jsonFilename = pre + '.json'
    log.info('Writing metadata to: ' + jsonFilename)
    write_results(results, jsonFilename, log)
