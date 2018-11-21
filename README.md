# Python-Tests
Some test scripts to get me to like Python mode

## Usage
Run it like this:  
`python test.py [options]`

Use this to get help for the command line options:  
`python test.py -h`

### Examples

* `python test.py --primenumbers 100000`

 Calculates prime numbers up to 10000

* `python test.py --primenumbers 100000 -o`

 Calculates prime numbers up to 10000 and prints them out

* `python test.py --waves`

 Draws some beautiful folded waveforms

* `python test.py --waves --wavesparams 20.0 15.0 0.5 20.0`

 Draws waveforms with custom parameters

* `python test.py --xor "This is just some text" "Passphrase1234"`

 Encrypts "This is just some text" with key "Passphrase1234"

* `python test.py --location me`

 Prints out information about my current location

* `python test.py --location 216.58.223.9`
 
 Prints out information about the location of a Google server

* `python test.py --magiceightball "Should I buy a new synthesizer tomorrow?"`

 Ask the Magic Eightball a question!

* `python test.py --namegen`
 
 Generate a funny name of random gender

* `python test.py --namegen --gender female --namecount 20`
 
 Generate 20 funny female names

* `python test.py --benchmarks --testintensity=50000 --timelimit=10 --tests=sin,matrix`
 
 Perform quite intense multithreaded benchmarks with trigonometric calculations and matrix multiplications.

* `python test.py --hash md5 "Hello World"`
 
 Calculate an MD5 hash of the String "Hello World"

* `python test.py --hash sha256 "/Users/somebody/Desktop/testfile.txt"
 
 Calculate an SHA256 hash of the contents of a file.

## Modules
The whole project is grouped into a launcher (test.py) and modules that are wrapped in a Python package (folder "modules"). The launcher script is set up in a way that it does not have to be changed when adding a new module to the package.

Here is a list of the included modules:

### artworkprice
Calculate a suitable price if you want to sell a painting you made

### asciiart
Generate ASCII art from image files

This module is dependend on the *Pillow* library!  
Get it here: https://python-pillow.org  
Or install via pip: `sudo pip install Pillow`

### benchmarks
Perform different benchmarks single- and multithreaded, get results, see multiprocessing speedup factor

### dice
Throw a W6!

### eightball
Ask the Magic Eightball a question!

### encrypt_caesar
Simple implementation of the Caesar string encryption

### encrypt_xor
Simple implementation of an XOR string encryption

### fractiontest
Perform fraction calculations

### hash
Compute different hashes from strings or files.

### headsortails
Throws a coin and tells you whether it's heads or tails.

### location
Retrieves and prints geolocation information based on current IP

This module is dependend on the *geocoder* library!  
Get it here: https://geocoder.readthedocs.io/api.html?highlight=street#installation  
Or install via pip: `sudo pip install geocoder`

### namegen
A funny module that I originally wrote in JS and now ported to Python. It generates interesting and totally unexceptional male and female names.

The names will sound funniest to german ears, I suppose.

### primenumbers
Calculates all prime numbers up to a given limit

### pwgen
Generates a pronouncable password of variable length

### waves
Calculates folded waveforms on the basis of sine waves modulating each other.

This module is dependend on the *colorama* library!  
Get it here: https://pypi.org/project/colorama/#files  
Or install via pip: `sudo pip install colorama`


## Luxury setup
How to make using the scripts even easier...
### OSX
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
