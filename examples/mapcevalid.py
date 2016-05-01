#!/usr/bin/env python
import sys
sys.path.append('..')

from pyswmap import MapCalc

# This prints out a list of all possible MAP end-user IPv6 prefixes, 
# applicable MAP IPv6 addresses, and PSIDs for a particular domain.
# PSID will always equal 0 for a sharing ratio of 1:1.

# Syntax is as follows:
#  ./listmapaddresses.py 

# Define MAP domain characteristics.  The values may be changed to suite
# a alternate MAP domain configurations.

v6arg = sys.argv[1]
v4arg = sys.argv[2]
ratioarg = int(sys.argv[3])

m = MapCalc( rulev6=v6arg,
             rulev4=v4arg,
             #psidoffset=6,
             ratio=ratioarg,
             #ealen=14,
                   )

print(type(test))
if (test != None):
    print(hex(test))
test2 = m.get_map_ipv4(sys.argv[4])
if (test2 != None):
    print(test2)
#print(m.ealen)
#print(m.psidbits)
#print(m.rulev6mask)
