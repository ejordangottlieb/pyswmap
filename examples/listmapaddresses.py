#!/usr/bin/env python3

from pyswmap import MapCalc

# This prints out a list of all possible MAP end-user IPv6 prefixes, 
# applicable MAP IPv6 addresses, and PSIDs for a particular domain.
# PSID will always equal 0 for a sharing ratio of 1:1.

# Syntax is as follows:
#  ./listmapaddresses.py 

# Define MAP domain characteristics.  The values may be changed to suite
# a alternate MAP domain configurations.

m = MapCalc( rulev6='fd80::/48',
             rulev4='24.50.100.0/24',
             #psidoffset=6,
             ratio=64,
             #ealen=14,
                   )
# The attribute rulev4object is the object returned for a particular
# instance of the ip_address class from module Python ipaddress.
for y in range(m.rulev4object.num_addresses):
    for w in range(2**m.psidbits):
        m.gen_mapaddr(m.rulev4object[y],w)
        #print(m.pd)
        print("User prefix: {}  MAP address: {}  PSID: {}".format(
              m.pd,
              m.mapce,
              w,
                                                                 )
             )

    
