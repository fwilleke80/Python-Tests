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

* `python test.py --location`

 Prints out information about current location

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
