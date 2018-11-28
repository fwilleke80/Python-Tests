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

### artworkprice
Calculate a suitable price if you want to sell a painting you made

Examples:  
`python test.py --artworkprice --dimensions A4`  
`python test.py --artworkprice --dimensions 46x60 --artfactor 5`

### asciiart
Generate ASCII art from image files

This module is dependend on the *Pillow* library!  
Get it here: https://python-pillow.org  
Or install via pip: `sudo pip install Pillow`

Example:  
`python test.py --asciiart /Users/somebody/Desktop/my_portrait.jpg`

### benchmarks
Perform different benchmarks single- and multithreaded, get results, see multiprocessing speedup factor.

Examples:  
`python test.py --benchmarks`  
`python test.py --benchmarks --testintensity=50000 --timelimit=10 --tests=sin,matrix`

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
`python test.py -headsortails`

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
`python test.py --namegen --gender female --namecount 20`

### primenumbers
Calculates all prime numbers up to a given limit

Example:  
`python test.py --primenumbers 100000 -v`

### pwgen
Generates a pronouncable password of variable length

Example:  
`python test.py --pwgen`

### readability
Analyzes a plain text file and computes some statistics about it, including different readability indices.

Example:
`python test.py --readability /Users/somebody/Desktop/haensel_und_gretel.txt`

### waves
Calculates folded waveforms on the basis of sine waves modulating each other.

This module is dependend on the *colorama* library!  
Get it here: https://pypi.org/project/colorama/#files  
Or install via pip: `sudo pip install colorama`

Examples:  
`python test.py --waves`  
`python test.py --waves --wavesparams 20.0 15.0 0.5 20.0`

## Luxury setup
How to make using the scripts even easier...
### Mac OS
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
