# Python-Tests
Some test scripts to get to like Python mode

## Usage
python test.py [options]

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

### location
Retrieves and prints geolocation information based on current IP

This module is dependend on the *geocoder* library!  
Get it here: https://geocoder.readthedocs.io/api.html?highlight=street#installation  
Or install via pip: `sudo pip install geocoder`
