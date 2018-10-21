# Python-Tests
Some test scripts to get to like Python mode

## Usage
python test.py [options]

### Examples

* `python test.py -p 100000`

 Calculates prime numbers up to 10000

* `python test.py -p 100000 -o`

 Calculates prime numbers up to 10000 and prints them out

* `python test.py -w 15.0 10.0 0.1 30.0`

 Draws some beautiful folded waveforms

* `python test.py -x "This is just some text" "Password1234"`

 Encrypts "This is just some text" with key "Password1234"

## Modules

* primenumbers

 Calculates all prime numbers up to a given limit

* waves

 Calculates folded waveforms on the basis of sine waves modulating each other

* encrypt_xor

 Simple implementation of an XOR string encryption
 
 ## Dependencies
 
 * Module *waves*
  This module is dependend on the *colorama* library.
  
  Get it here: https://pypi.org/project/colorama/#files
  
  Or install via pip: `sudo pip install colorama`
  
