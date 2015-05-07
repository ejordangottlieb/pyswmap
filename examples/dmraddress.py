#!/usr/bin/env python3

import sys
from pyswmap import DmrCalc

# This script takes a IPv4 address and embeds it RFC6052 style
# into an IPv6 prefix

# Syntax is as follows:
#  ./dmraddress.py [BR prefix] [IPv4 address]


# Supply BR Prefix
dmrprefix = sys.argv[1]
# supply IPv4 in dotted decimal notation (192.0.0.1)
ipv4 = sys.argv[2]

m = DmrCalc(dmrprefix)
print(m.embed_6052addr(ipv4))
