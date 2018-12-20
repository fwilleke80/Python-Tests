#!/usr/bin/python
import sys
import time
import random


# Script info
SCRIPTTITLE = 'German Name Generator'
SCRIPTVERSION = '1.5.5'
SCRIPTINFO = 'Generate a funny german name'
SCRIPT_HELP = """
Usage:
  --namegen [count=n] [gender=female|male|random] [stats] [help]
  --namegen [c=n] [g=female|male|random] [s] [help]

Examples:
  --namegen
      Generates a random name of random gender

  --namegen gender=female cuont=20
      Generated 20 random female names

count
    Provide a number n > 0 here and that many names will be generated

gender
    Specify a gender here

stats
    Display statistics about the number of possible name combinations

help
    Displays this help, so you propably already know this one.
"""


# Class that does all the name generation work
class NameGenerator:
    # Thresholds
    threshExtraFirstnameSyllable = 0.68
    threshDoubleLastName = 0.82
    threshLongerLastName = 0.7
    threshNobility = 0.7

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
                                    'stink', \
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
                                    'ru', \
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
                                    'beus', \
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
                                    'sack', \
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
                                        'ba', \
                                        'na', \
                                        'dani', \
                                        'ker', \
                                        'klara', \
                                        'ju', \
                                        'gud', \
                                        'su', \
                                        'i', \
                                        'a', \
                                        'e', \
                                        'o', \
                                        'u', \
                                        'her', \
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
                                        'lena', \
                                        'ol', \
                                        'na', \
                                        'cor', \
                                        'pene', \
                                        'mag', \
                                        'magda', \
                                        'jas', \
                                        'alex', \
                                        'bar', \
                                        'klo'], \
                                        \
                                    ['gata', \
                                        'beta', \
                                        'trabo', \
                                        'phe', \
                                        'ba', \
                                        'da', \
                                        'bumbo', \
                                        'braba', \
                                        'gret', \
                                        'ta', \
                                        'mi', \
                                        'bi'], \
                                        \
                                    ['gunde', \
                                        'tilde', \
                                        'lia', \
                                        'lena', \
                                        'rune', \
                                        'lope', \
                                        'bette', \
                                        'andra', \
                                        'tha', \
                                        'min', \
                                        'run', \
                                        'dora', \
                                        'ke', \
                                        'elle', \
                                        'ela', \
                                        'ella', \
                                        'scha', \
                                        'ga', \
                                        'na', \
                                        'ne', \
                                        'ra', \
                                        'bella', \
                                        'maria', \
                                        'nelia', \
                                        'stin', \
                                        'berta', \
                                        'scha', \
                                        'a', \
                                        'e', \
                                        'mine', \
                                        'bine', \
                                        'brina', \
                                        'sanne', \
                                        'gitte', \
                                        'lotte', \
                                        'grunde', \
                                        'lia', \
                                        'hilde']
                                ] \
                            }

    lastNameSyllables = ['knu', \
                            'per', \
                            'nagel', \
                            'rubbel', \
                            'helm', \
                            'malo', \
                            'zak', \
                            'sack', \
                            'abo', \
                            'wonk', \
                            'hag', \
                            'kovsky', \
                            'hump', \
                            'rid', \
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
                            'hausen', \
                            'weyhe', \
                            'wey', \
                            'he', \
                            'tr' + u'\u00f6' + 'del', \
                            'paff']

    nobilityPrefixes = {    'male' : \
                                [ \
                                    'von', \
                                    'zu',  \
                                    'Freiherr von', \
                                    'von und zu', \
                                    'Graf von', \
                                    'Erzherzog', \
                                    'Markgraf', \
                                    'F' + u'\u00fc' + 'rst'
                                ],
                            'female' : \
                                [ \
                                    'von', \
                                    'zu',  \
                                    'von und zu', \
                                    'Gr' + u'\u00e4' + 'fin von', \
                                    'Erzherzogin', \
                                    'Markgr' + u'\u00e4' + 'fin'
                                ]

    }

    # Compute number of possible names
    def compute_stats(this):
        # Number of possible male firstnames
        numberOfMaleFirstnames_short = len(this.firstNameSyllables['male'][0]) * len(this.firstNameSyllables['male'][2])
        numberOfMaleFirstnames_long = len(this.firstNameSyllables['male'][0]) * len(this.firstNameSyllables['male'][1]) * len(this.firstNameSyllables['male'][2])
        numberOfMaleFirstnames = numberOfMaleFirstnames_short + numberOfMaleFirstnames_long

        # Number of possible female firstnames
        numberOfFemaleFirstnames_short = len(this.firstNameSyllables['female'][0]) * len(this.firstNameSyllables['female'][2])
        numberOfFemaleFirstnames_long = len(this.firstNameSyllables['female'][0]) * len(this.firstNameSyllables['female'][1]) * len(this.firstNameSyllables['female'][2])
        numberOfFemaleFirstnames = numberOfFemaleFirstnames_short + numberOfFemaleFirstnames_long

        numberOfFirstNames = numberOfFemaleFirstnames + numberOfMaleFirstnames

        # Number of nobility titles
        numberOfFemaleNobilityTitles = len(this.nobilityPrefixes['female'])
        numberOfMaleNobilityTitles = len(this.nobilityPrefixes['male'])
        numberOfNobilityTitles = numberOfFemaleNobilityTitles + numberOfMaleNobilityTitles

        # Number of possible lastnames
        numberOfLastNames_short = len(this.lastNameSyllables) ** 2 * (numberOfNobilityTitles + 1)
        numberOfLastNames_long = len(this.lastNameSyllables) ** 3 * (numberOfNobilityTitles + 1)
        numberOfLastnames = numberOfLastNames_short + numberOfLastNames_long

        # Total number of firstname/lastname combinations
        numberOfMaleNames = numberOfMaleFirstnames * numberOfLastnames * (numberOfMaleNobilityTitles + 1)
        numberOfFemaleNames = numberOfFemaleFirstnames * numberOfLastnames * (numberOfFemaleNobilityTitles + 1)
        numberOfNames = numberOfMaleNames + numberOfFemaleNames

        # Now build dictionary
        resultStats = {
            'firstnames' : {
                'female' : {
                    'short' : numberOfFemaleFirstnames_short,
                    'long'  : numberOfFemaleFirstnames_long,
                    'total' : numberOfFemaleFirstnames
                },
                'male'   : {
                    'short' : numberOfMaleFirstnames_short,
                    'long'  : numberOfMaleFirstnames_long,
                    'total' : numberOfMaleFirstnames
                },
                'total'  : numberOfFirstNames
            },
            'lastnames' : {
                'short' : numberOfLastNames_short,
                'long'  : numberOfLastNames_long,
                'total' : numberOfLastnames
            },
            'nobility' : {
                'female' : numberOfFemaleNobilityTitles,
                'male'   : numberOfMaleNobilityTitles,
                'total'  : numberOfNobilityTitles
            },
            'female': numberOfFemaleNames,
            'male'  : numberOfMaleNames,
            'total' : numberOfNames
        }

        return resultStats


    # Print statistics from resultStats dictionary
    def print_statistics(this, log, stats):
        log.info('Database statistics')
        print('=========================')
        print('')
        log.info('Firstnames:')
        print('-----------------')
        log.info('Female short names   : ' + "{:8,}".format(stats['firstnames']['female']['short']))
        log.info('Female long names    : ' + "{:8,}".format(stats['firstnames']['female']['long']))
        log.info('Female names in total: ' + "{:8,}".format(stats['firstnames']['female']['total']))
        print('')
        log.info('Male short names     : ' + "{:8,}".format(stats['firstnames']['male']['short']))
        log.info('Male long names      : ' + "{:8,}".format(stats['firstnames']['male']['long']))
        log.info('Male names in total  : ' + "{:8,}".format(stats['firstnames']['male']['total']))
        print('')
        log.info('Firstnames in total  : ' + "{:8,}".format(stats['firstnames']['total']))
        print('')
        log.info('Lastnames:')
        print('----------------')
        log.info('Short lastnames         : ' + "{:8,}".format(stats['lastnames']['short']))
        log.info('Long lastnames          : ' + "{:8,}".format(stats['lastnames']['long']))
        log.info('Lastnames in total      : ' + "{:8,}".format(stats['lastnames']['total']))
        print('')
        log.info('Nobility titles:')
        print('----------------')
        log.info('Female nobility titles  : ' + "{:8,}".format(stats['nobility']['female']))
        log.info('Male nobility titles    : ' + "{:8,}".format(stats['nobility']['male']))
        log.info('Nobility titles in total: ' + "{:8,}".format(stats['nobility']['total']))
        print('')
        log.info('Total:')
        print('------------')
        log.info('Female name combinations  : ' + "{:15,}".format(stats['female']))
        log.info('Male name combinations    : ' + "{:15,}".format(stats['male']))
        log.info('Name combinations in total: ' + "{:15,}".format(stats['total']))


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
        # Determine lengh of lastname
        if random.random() > this.threshLongerLastName:
            numberOfSyllables = random.randrange(this.minLastnameSyllables, this.maxLastnameSyllables)
        else:
            numberOfSyllables = this.minLastnameSyllables

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


    # Get nobility title
    def get_nobility_prefix(this, gender='male'):
        return random.choice(this.nobilityPrefixes[gender])


    def safe_gender(this, log, theGender):
        # Support abbreviated genders
        if theGender == 'f':
            theGender = 'female'
        elif theGender == 'm':
            theGender = 'male'
        elif theGender == 'r':
            theGender = 'random'

        # Detect unsupported gender
        if theGender not in list(this.firstNameSyllables) and theGender != 'random':
            log.error('Gender "' + theGender + '" not implemented yet. Sorry about that. Using random gender instead.')
            log.info('Supported genders: ' + str(list(this.firstNameSyllables)) + '.')
            print('')
            theGender = 'random'

        # If random gender desired, pick an available one
        if theGender == 'random':
            theGender = random.choice(list(this.firstNameSyllables))

        return theGender


    def generate(this, log, theGender):
        # Detect unsupported gender
        theGender = this.safe_gender(log, theGender)

        log.debug('Gender: ' + theGender.title())

        firstName = this.generate_firstname(theGender)
        lastName = this.generate_lastname()

        # Double lastname?
        if random.random() > this.threshDoubleLastName:
            lastName += '-' + this.generate_lastname()

        # Nobility?
        if random.random() > this.threshNobility:
            lastName = this.get_nobility_prefix(theGender) + ' ' + lastName

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
# check_options(options)
#    Return True if main function can be run, depending on the command line arguments. If not dependent on any arguments, just return True
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
    optGroup.add_option('--namegen', action='store_true', dest='namegen', default=None, help=SCRIPTINFO)


# Return True if args/options tell us to run this module
def check_options(log, options, args):
    return options.namegen is not None and options.namegen == True


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

    # Create new NameGenerator object
    nameGen = NameGenerator()

    # Seed random generator
    random.seed(time.time())

    # Parse args
    nameGender = 'random'
    nameCount = 1
    for argIndex, arg in enumerate(args):
        arg = arg.upper()
        if (arg[0] == 'G' or arg[:6] == 'GENDER') and '=' in arg:
            # Set gender
            nameGender = arg.split('=')[1].lower()
        elif (arg[0] == 'C' or arg[:5] == 'COUNT') and '=' in arg:
            # Set name count
            nameCount = int(arg.split('=')[1])
        elif arg[0] =='S' or arg[:5] == 'STATS':
            # Print statistics
            nameGen.print_statistics(log, nameGen.compute_stats())
            print('')
        elif (arg == 'HELP'):
            print(SCRIPT_HELP)
        else:
            log.error('Unsupported argument: ' + arg)
            print('')

    # Generate name(s)
    for i in range(nameCount):
        log.info((str(i + 1) + '. ' if nameCount > 1 else '') + nameGen.generate(log, nameGender))
