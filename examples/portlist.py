#!/usr/bin/env python3

from pyswmap import MapCalc
import sys

# This script calculates the allocated ports for a given Port-Set ID (PSID).
 
# Syntax is as follows:
#  ./portlist.py [psid] 

# Define MAP domain characteristics.  The values may be changed to suite
# a alternate MAP domain configurations.
m = MapCalc( rulev6='fd80::/48',
             rulev4='24.50.100.0/24',
             #psidoffset=6,
             ratio=64,
             #ealen=14,
                   )

# Provide a valid PSID value.  The pyswmap module does not currently validate
# that the PSID can be represented by the length in bits of the  PSID bits.
m.psid=int(sys.argv[1])

# Print out the results
print(m.port_list())
