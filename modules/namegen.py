#!/usr/bin/python
import random


# Script info
SCRIPTTITLE = 'German Name Generator'
SCRIPTVERSION = '1.3.3'
SCRIPTINFO = 'Generate a funny german name'


class NameGenerator:
    # Thresholds
    threshExtraFirstnameSyllable = 0.7
    threshDoubleLastName = 0.82

    # Limits / Ranges
    minLastnameSyllables = 2
    maxLastnameSyllables = 4

    # Syllable lists
    firstNameSyllables = { 'male' : \
                            [ \
                                ['kno', \
                                    'ro', \
                                    'hu', \
                                    'schnurr', \
                                    'knurr', \
                                    'bern', \
                                    'rein', \
                                    'bro', \
                                    'hab', \
                                    'brot', \
                                    'bratz', \
                                    'knack', \
                                    'her', \
                                    'brumm', \
                                    'volk', \
                                    'ha', \
                                    'lad', \
                                    'brat', \
                                    'atz', \
                                    'horst', \
                                    'christ', \
                                    'det', \
                                    'krumm', \
                                    'pups', \
                                    'knall', \
                                    'ekko', \
                                    'mal', \
                                    'mar', \
                                    'gram', \
                                    'dussel', \
                                    'd'+u'\u00fc'+'mpel', \
                                    'gronko', \
                                    'gro', \
                                    'jan', \
                                    'bums', \
                                    'niete', \
                                    'brom', \
                                    'brumm', \
                                    'step', \
                                    'ali', \
                                    'schno', \
                                    'sack', \
                                    'kack', \
                                    'jo', \
                                    'det', \
                                    'ost', \
                                    'nord', \
                                    'trelle', \
                                    'wern'], \
                                \
                                ['bol', \
                                    'bul', \
                                    'bom', \
                                    'bart', \
                                    'o', \
                                    'ba', \
                                    'bo', \
                                    'bu', \
                                    'bi', \
                                    'is', \
                                    'see', \
                                    'stump', \
                                    'honk', \
                                    'parz', \
                                    'a', \
                                    'stu', \
                                    'hann'], \
                                \
                                ['bert', \
                                    'bart', \
                                    'hahn', \
                                    'hardt', \
                                    'ald', \
                                    'bald', \
                                    'rald', \
                                    'tav', \
                                    'lav', \
                                    'mann', \
                                    'er', \
                                    'ius', \
                                    'kus', \
                                    'os', \
                                    'lev', \
                                    'belli', \
                                    'zahn', \
                                    'gar', \
                                    'bold', \
                                    'trutz', \
                                    'fried', \
                                    'bi', \
                                    'en', \
                                    'rich', \
                                    'er'] \
                            ], \
                            \
                            'female' : \
                                [ \
                                    ['kuni',
                                        'berta', \
                                        'her', \
                                        'da', \
                                        'dani', \
                                        'ker', \
                                        'klara', \
                                        'gud', \
                                        'su', \
                                        'i', \
                                        'a', \
                                        'e', \
                                        'o', \
                                        'u', \
                                        'sa', \
                                        'bri', \
                                        'lau', \
                                        'chris'
                                        'eva', \
                                        'lise', \
                                        'frau', \
                                        'wieb', \
                                        'manu', \
                                        'emanu', \
                                        'theo', \
                                        'na', \
                                        'cor', \
                                        'pene', \
                                        'jas', \
                                        'kuni', \
                                        'klo'], \
                                        \
                                    ['gata', \
                                        'beta', \
                                        'trabo', \
                                        'phe', \
                                        'bumbo', \
                                        'gret', \
                                        'ta', \
                                        'bi'], \
                                        \
                                    ['gunde', \
                                        'tilde', \
                                        'lia', \
                                        'rune', \
                                        'lope', \
                                        'tha', \
                                        'min', \
                                        'run', \
                                        'dora', \
                                        'ke', \
                                        'elle', \
                                        'ela', \
                                        'ella', \
                                        'na', \
                                        'ra', \
                                        'bella', \
                                        'nelia', \
                                        'stin', \
                                        'berta', \
                                        'scha', \
                                        'a', \
                                        'mine', \
                                        'bine', \
                                        'brina', \
                                        'sanne', \
                                        'gitte', \
                                        'lotte', \
                                        'grunde', \
                                        'hilde']
                                ] \
                            }

    lastNameSyllables = ['knu', \
                            'per', \
                            'helm', \
                            'malo', \
                            'zak', \
                            'sack', \
                            'abo', \
                            'wonk', \
                            'kovsky', \
                            'hump', \
                            'ski', \
                            'mann', \
                            'boff', \
                            'woll', \
                            'wolle', \
                            'wulle', \
                            'k'+u'\u00f6'+'l', \
                            'ratz', \
                            'wicz', \
                            'bert', \
                            'horst', \
                            'kotte', \
                            'tab', \
                            'trabo', \
                            'grump', \
                            'porn', \
                            'bl' + u'\u00fc' + 'mel', \
                            'k' + u'\u00fc' + 'l', \
                            'k' + u'\u00fc' + 'bl', \
                            'b' + u'\u00f6' + 'ck', \
                            'g' + u'\u00f6' + 'bel', \
                            'k' + u'\u00e4' + 's', \
                            'k' + u'\u00e4' + 'se', \
                            'trump', \
                            'niete', \
                            'zing', \
                            'koc', \
                            'will', \
                            'eke', \
                            'merkel', \
                            'kohl', \
                            'bums', \
                            'ak', \
                            'krach', \
                            'kel', \
                            'hel', \
                            'sin', \
                            'ra', \
                            'tu', \
                            'meier', \
                            'meyer',  \
                            'mayer', \
                            'bronko' \
                            'trelle', \
                            'born', \
                            'fan', \
                            'ler', \
                            'bumper', \
                            'schlimper', \
                            'schiefel', \
                            'bein', \
                            'kug', \
                            'te', \
                            'le', \
                            'pan', \
                            'piese', \
                            'pampel', \
                            'burg', \
                            'hans', \
                            'tr' + u'\u00f6' + 'del', \
                            'paff']


    # Generate random firstname
    def generate_firstname(this, gender='male'):
        # Add first syllable
        newName = random.choice(this.firstNameSyllables[gender][0])

        # Add extra syllable
        if random.random() > this.threshExtraFirstnameSyllable:
            newName += random.choice(this.firstNameSyllables[gender][1])

        # Add last syllable
        newName += random.choice(this.firstNameSyllables[gender][2])

        # Return name with capitalized first letter
        return newName.title()


    # Generate random lastname
    def generate_lastname(this):
        numberOfSyllables = random.randrange(this.minLastnameSyllables, this.maxLastnameSyllables)
        lastSyllableIndex = -1
        newName = ''

        # Chain up syllables
        for i in range(0, numberOfSyllables):
            newSyllableIndex = -1

            # Make sure the same syllable isn't used twice in a row
            while True:                
                newSyllableIndex = random.randrange(0, len(this.lastNameSyllables) - 1)
                if newSyllableIndex != lastSyllableIndex:
                    break;

            newName += this.lastNameSyllables[newSyllableIndex]
            lastSyllableIndex = newSyllableIndex

        # Return name with capitalized first letter
        return newName.title()


    def safe_gender(this, log, gender):
        # Detect unsupported gender
        theGender = gender.lower()
        if theGender not in list(this.firstNameSyllables) and theGender != 'random':
            log.error('Gender '' + gender + '' not implemented yet. Using random gender instead.')
            theGender = 'random'

        # If random gender desired, pick an available one
        if theGender == 'random':
            theGender = random.choice(list(this.firstNameSyllables))

        return theGender


    def generate(this, log, gender):
        # Detect unsupported gender
        theGender = this.safe_gender(log, gender)

        log.debug('Gender: ' + theGender.title())

        firstName = this.generate_firstname(theGender)
        lastName = this.generate_lastname()

        # Double lastname?
        if random.random() > this.threshDoubleLastName:
            lastName += '-' + this.generate_lastname()

        return firstName + ' ' + lastName



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
def setup_args(optGroup):
    optGroup.add_option('--namegen', action='store_true', dest='namegen', default=None, help=SCRIPTINFO)
    optGroup.add_option('--gender', type='string', dest='namegen_gender', default='random', help='Specify gender of firstname (''male'' or ''female'' or ''random'')', metavar='GENDER')
    optGroup.add_option('--namecount', type='int', dest='namegen_count', default=1, help='Specify how many names should be generated with COUNT', metavar='COUNT')


# Return True if args/options tell us to run this module
def check_args(log, options):
    return options.namegen is not None and options.namegen == True and check_additional_args(log, options)


# Checks additional arguments and prints error messages
def check_additional_args(log, options):
    if options.namegen_gender is None or options.namegen_count is None or options.namegen_count < 1:
        log.error('Invalid name generator arguments!')
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

    nameGen = NameGenerator()

    for i in range(options.namegen_count):
        log.info((str(i + 1) + '. ' if options.namegen_count > 1 else '') + nameGen.generate(log, options.namegen_gender))
