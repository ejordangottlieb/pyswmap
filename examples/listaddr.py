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
# The attribute rulev4object is the object returned for a particular
# instance of the ip_address class from module Python ipaddress.
for y in range(m.rulev4object.num_addresses):
    for w in range(2**m.psidbits):
        mapce = m.get_mapce_addr(m.rulev4object[y],w)
        pd = m.get_mapce_prefix(m.rulev4object[y],w)
        print("User prefix: {}  MAP address: {}  PSID: {} IPv4: {}".format(
              pd,
              mapce,
              w,
              m.get_map_ipv4(mapce),
                                                                 )
             )

    
