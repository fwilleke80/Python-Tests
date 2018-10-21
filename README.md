# Python-Tests
Some test scripts to get to like Python mode

## Usage
python test.py [options]

### Examples

* `python test.py --primenumbers 100000`

 Calculates prime numbers up to 10000

* `python test.py --primenumbers 100000 -o`

 Calculates prime numbers up to 10000 and prints them out

* `python test.py --waves 15.0 10.0 0.1 30.0`

 Draws some beautiful folded waveforms

* `python test.py --xor "This is just some text" "Passphrase1234"`

 Encrypts "This is just some text" with key "Passphrase1234"

## Modules

### primenumbers
Calculates all prime numbers up to a given limit

### waves
Calculates folded waveforms on the basis of sine waves modulating each other.

This module is dependend on the *colorama* library!    
Get it here: https://pypi.org/project/colorama/#files  
Or install via pip: `sudo pip install colorama`

### encrypt_xor
Simple implementation of an XOR string encryption  
