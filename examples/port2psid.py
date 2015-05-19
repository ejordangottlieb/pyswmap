#!/usr/bin/env python3

from pyswmap import MapCalc
import sys

# This script prints out the PSID for any given port and BMR. 

# Syntax is as follows:
#  ./port2psid.py 

# Define MAP domain characteristics.  The values may be changed to suite
# a alternate MAP domain configurations.

m = MapCalc( rulev6='fd80::/48',
             rulev4='24.50.100.0/24',
             #psidoffset=6,
             ratio=64,
             #ealen=30,
                   )
# Port value is provided as a command line variable.  it is converted to
# an integer before being passed to the gen_psid method.

print(m.gen_psid(int(sys.argv[1])))


    
