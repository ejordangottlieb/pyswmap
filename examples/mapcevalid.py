#!/usr/bin/env python
import sys
sys.path.append('..')

from pyswmap import MapCalc

# This allows a user to validate that a MAP CE address and source port is
# valid given a particular mapping rule.  This script ensures that the MAP
# CE address is valid.  This script does not suport IPv6 user prefix
# lengths of greater than 64-bits.  I see not reason as it is not adviseable
# to assign a user prefix smaller than a /64.

# Syntax is as follows:
#  ./mapcevalid.py [Rule IPv6] [Rule IPv4] [ratio] [CE address] [port]

# Define MAP domain characteristics.  The values may be changed to suite
# a alternate MAP domain configurations.

v6arg = sys.argv[1]
v4arg = sys.argv[2]
ratioarg = int(sys.argv[3])
ceaddr = sys.argv[4]
port = int(sys.argv[5])

m = MapCalc( rulev6=v6arg,
             rulev4=v4arg,
             #psidoffset=6,
             ratio=ratioarg,
             #ealen=14,      
                             )

bmr = m.get_mapce_bmr(ceaddr) 

if (bmr != None):
    for addr in bmr.keys():
        portlist = m.port_list(bmr[addr])
        if ( port not in portlist ):
            print('{} is not a port assigned to {}'.format(port, ceaddr))
        else:
            print('Port {} is valid for {}'.format(port, ceaddr))
            print('IPv4 Address {} PSID {}'.format(addr, bmr[addr]))
else:
    print('Invalid MAP CE Address {}'.format(ceaddr))

