#!/usr/bin/env python3

from pyswmap import MapCalc

m = MapCalc( rulev6='fd80::/48',
             rulev4='24.50.100.0/24',
             #psidoffset=6,
             ratio=64,
             #ealen=14,
                   )
#                  m.psid:       The port-set ID which defines the
#                                algorithmically assigned ports unique to
#                                a particular MAP CE.
#
m.psid=0
print(m.port_list())
