# Python-Tests
Some test scripts to get me to like Python

## Usage
Run it like this:  
`python test.py [options]`

Use this to get help for all the command line options:  
`python test.py -h`

Use this to list all available modules:  
`python test.py --listmodules`

## Modules
The whole project is grouped into a launcher (test.py) and modules that are wrapped in a Python package (folder "modules"). The launcher script is set up in a way that it does not have to be changed when adding a new module to the package.

Here is a list of the included modules:

### analysetext
Analyzes a plain text file and computes some statistics about it, including different readability indices, and word frequency table.

Example:  
`python test.py --analysetext /Users/somebody/Desktop/haensel_und_gretel.txt --writemetadata`

### artworkprice
Calculate a suitable price if you want to sell a painting you made

Examples:  
`python test.py --artworkprice A4`  
`python test.py --artworkprice 46x60 5`  
`pytohn test.py --artworkprice dimensions=A3 factor=7`

### asciiart
Generate ASCII art from image files

This module is dependend on the *Pillow* library!  
Get it here: https://python-pillow.org  
Or install via pip: `sudo pip install Pillow`

Examples:  
`python test.py --asciiart /Users/somebody/Desktop/my_portrait.jpg`  
`python test.py --asciiart /Users/somebody/Desktop/my_portrait.jpg /Users/somebody/Desktop/my_portrait.txt`

### benchmarks
Perform different benchmarks single- and multithreaded, get results, see multiprocessing speedup factor.

Examples:  
`python test.py --benchmarks`  
`python test.py --benchmarks intensity=50000 timelimit=10 tests=sin,matrix threads=4`

### dice
Throw a W6!

Example:  
`python test.py --dice`

### eightball
Ask the Magic Eightball a question!

Example:  
`python test.py --magiceightball "Should I buy a new synthesizer tomorrow?"`

### encrypt_caesar
Simple implementation of the Caesar string encryption

Example:  
`python test.py --caesar "This is just some text" 2`

### encrypt_xor
Simple implementation of an XOR string encryption

Example:  
`python test.py --xor "This is just some text" "Passphrase1234"`

### fractiontest
Perform fraction calculations

Example:  
`python test.py --fraction simplify 6 24`

### googletranslate
Translate texts from one language to another.

This module is dependend on the *googletrans* library!  
Get it here: https://pypi.org/project/googletrans/  
Or install via pip: `sudo pip install googletrans`

Example:  
`python test.py --translate "Guten Tag, ich hätte gerne ein Steak."`

### hash
Compute different hashes from strings or files.

Examples:  
`python test.py --hash md5 "Hello World"`  
`python test.py --hash sha256 "/Users/somebody/Desktop/testfile.txt"`

### headsortails
Throws a coin and tells you whether it's heads or tails.

Example:  
`python test.py --headsortails`

### location
Retrieves and prints geolocation information based on current IP

This module is dependend on the *geocoder* library!  
Get it here: https://geocoder.readthedocs.io/api.html?highlight=street#installation  
Or install via pip: `sudo pip install geocoder`

Examples:  
`python test.py --location me`  
`python test.py --location 216.58.223.9`

### namegen
A funny module that I originally wrote in JS and now ported to Python.  
It generates interesting and totally unexceptional male and female names.

The names will sound funniest to german ears, I suppose.

Examples:  
`python test.py --namegen`  
`python test.py --namegen gender=female --count=20`

### primenumbers
Calculates all prime numbers up to a given limit

Example:  
`python test.py --primenumbers 100000 print`

### pwgen
Generates a pronouncable password of variable length

Examples:  
`python test.py --pwgen`  
`python test.py --pwgen length=8`

### sortfiles
A handy tool to sort multiple files into subfolders, based on their modification date.  
Especially useful, e.g. to sort imported images from your phone or camera.  
It also supports dry run, to simulate the result without actually changing anything.  
Call with "help" argument to get detailled usage instructions.

Examples:  
`python test.py --sortfiles`  
`python test.py --sortfiles /Users/somebody/Desktop/newImages /Users/somebody/Pictures pattern=images`  
`python test.py --sortfiles help`

### tictactoe
A simple implementation of a classic game. Play against the computer or against a friend!
Keep track of played and won games using the highscore feature! Careful, the computer plays well!

Examples:  
`python test.py --tictactoe`  
`python test.py --tictactoe John X`  
`python test.py --tictactoe John X Kevin`  
`python test.py --tictactoe highscores`

### timetrack
A useful tool to track what you're doing with your time.  
With one command you can tell it what you're doing, and the tool will keep track of your times.  
You can also review your activities and generate reports.  
Quite useful if you're working on multiple different projects and want to know how much time you spend on each one.  
Call with "help" argument to get detailled usage instructions.

Example:  
`python test.py --timetrack add Programming "Fixing bugs today"`  
`python test.py --timetrack list`  
`python test.py --timetrack help`

### waves
Calculates folded waveforms on the basis of sine waves modulating each other.

This module is dependend on the *colorama* library!  
Get it here: https://pypi.org/project/colorama/#files  
Or install via pip: `sudo pip install colorama`

Examples:  
`python test.py --waves`  
`python test.py --waves 20.0 15.0 0.5 20.0`  
`python text.py --waves speed=30 scale1=12.5 scale2=0.7 fold=30`

## Luxury setup
How to make using the scripts even easier...
### Mac OS Terminal usage
* Open Terminal:  
    Press `CMD+SPACE`  
    Type `Terminal`
* Navigate to your home folder:  
    Type `cd ~`
* Edit your bash profile:  
    Type `nano .bash_profile`
* Add an alias to the test.py call:  
    Add line: `alias [ALIASNAME]="python [PATH TO TEST.PY]"`  
    Example: `alias ftools="python ~/Documents/_Projects/Python\ Tests/test.py"`
* Exit NANO editor and save changes
* Reload bash profile:  
    Type `source ~/.bash_profile`
* Now you can run the script form anywhere like this:  
    Type `ftools --hash md5 "Hello World"`

### Mac OS call via shell script on double-click
* Create a file with extension ".sh"
* Edit the file, and add the following lines:  
    `#!/bin/bash` 
    `python "/Users/somebody/Documents/Python Tests/test.py" --sortfiles /Users/somebody/Pictures pattern=images`
* In the Terminal, make the file executable with:  
    `chmod a+x myfile.sh`
* Open the file's Information and set "Terminal" as the default application
